import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

import database
from database import get_db

# Configuração básica de logging
logger = logging.getLogger("sensoriplay")
logging.basicConfig(level=logging.INFO)

# Rate limiting (proteção contra abuso)
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="SensoriPlay API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Configuração de CORS
origins_env = os.getenv("FRONTEND_ORIGINS")
if origins_env:
    allowed_origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]
else:
    allowed_origins = ["*"]
    logger.warning(
        "FRONTEND_ORIGINS não configurado. CORS liberado para qualquer origem (apenas recomendável em desenvolvimento).",
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Autenticação e usuários
# =========================

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class GoogleLoginRequest(BaseModel):
    id_token: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_email(db: Session, email: str) -> Optional[database.User]:
    return db.query(database.User).filter(database.User.email == email).first()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> database.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(database.User).filter(database.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_admin(current_user: database.User = Depends(get_current_user)) -> database.User:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores")
    return current_user


@app.post("/auth/register", response_model=UserOut)
@limiter.limit("20/minute")
async def register_user(request: Request, payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = database.User(
        name=payload.name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(id=user.id, name=user.name, email=user.email, is_admin=user.is_admin)


@app.post("/auth/login", response_model=Token)
@limiter.limit("30/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail ou senha inválidos")

    access_token = create_access_token({"sub": str(user.id), "is_admin": user.is_admin})
    return Token(access_token=access_token)


@app.post("/auth/google", response_model=Token)
@limiter.limit("30/minute")
async def google_login(request: Request, payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="GOOGLE_CLIENT_ID não configurado no servidor")

    try:
        idinfo = google_id_token.verify_oauth2_token(
            payload.id_token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except Exception:
        raise HTTPException(status_code=400, detail="ID token do Google inválido")

    email = idinfo.get("email")
    name = idinfo.get("name") or email.split("@")[0]
    if not email:
        raise HTTPException(status_code=400, detail="Não foi possível obter e-mail do Google")

    user = get_user_by_email(db, email)
    if not user:
        user = database.User(
            name=name,
            email=email,
            password_hash=get_password_hash(os.urandom(16).hex()),
            is_admin=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": str(user.id), "is_admin": user.is_admin})
    return Token(access_token=access_token)


@app.get("/auth/me", response_model=UserOut)
@limiter.limit("60/minute")
async def read_me(request: Request, current_user: database.User = Depends(get_current_user)):
    return UserOut(id=current_user.id, name=current_user.name, email=current_user.email, is_admin=current_user.is_admin)


# =========================
# Produtos
# =========================


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    age_range: str
    description: str
    emoji: str
    badge: str | None = None
    featured: bool = False


class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    age_range: str
    description: str
    emoji: str = "🎁"
    badge: str | None = None
    featured: bool = False
    stock: int = 0


class ProductUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    price: float | None = None
    age_range: str | None = None
    description: str | None = None
    emoji: str | None = None
    badge: str | None = None
    featured: bool | None = None
    stock: int | None = None


# Mock de produtos (fallback quando não há banco configurado)
PRODUCTS: List[Product] = [
    Product(
        id=1,
        name="Cubo Sensorial Fidget",
        category="sensorial",
        price=45.90,
        age_range="3-5",
        description="Cubo multi-textura com diferentes estímulos táteis",
        emoji="🎲",
        badge="Novo",
        featured=True,
    ),
    Product(
        id=2,
        name="Quebra-Cabeça 3D Animais",
        category="cognitivo",
        price=62.90,
        age_range="6-8",
        description="Quebra-cabeça tridimensional para desenvolvimento cognitivo",
        emoji="🦁",
        badge="Destaque",
        featured=True,
    ),
]


@app.get("/health")
@limiter.limit("10/second")
async def health_check(request: Request):
    return {"status": "ok"}


@app.get("/products", response_model=List[Product])
@limiter.limit("60/minute")
async def list_products(request: Request):
    """Lista produtos.

    Se DATABASE_URL estiver configurada, lê do PostgreSQL via SQLAlchemy.
    Caso contrário, usa a lista mockada em memória.
    """
    if database.SessionLocal is None:
        return PRODUCTS

    db = database.SessionLocal()
    try:
        db_products = db.query(database.Product).all()
        if not db_products:
            # Se o banco estiver vazio, ainda assim usamos o fallback em memória
            return PRODUCTS

        return [
            Product(
                id=p.id,
                name=p.name,
                category=p.category,
                price=float(p.price),
                age_range=p.age_range or "",
                description=p.description or "",
                emoji=p.emoji or "🎁",
                badge=p.badge,
                featured=p.featured,
            )
            for p in db_products
        ]
    finally:
        db.close()


@app.get("/admin/products", response_model=List[Product])
@limiter.limit("60/minute")
async def admin_list_products(
    request: Request,
    db: Session = Depends(get_db),
    _: database.User = Depends(get_current_admin),
):
    """Lista produtos para uso em telas administrativas (apenas admin)."""
    if database.SessionLocal is None:
        return PRODUCTS

    db_products = db.query(database.Product).order_by(database.Product.id).all()
    if not db_products:
        return PRODUCTS

    return [
        Product(
            id=p.id,
            name=p.name,
            category=p.category,
            price=float(p.price),
            age_range=p.age_range or "",
            description=p.description or "",
            emoji=p.emoji or "🎁",
            badge=p.badge,
            featured=p.featured,
        )
        for p in db_products
    ]


@app.post("/admin/products", response_model=Product, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def create_product(
    request: Request,
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _: database.User = Depends(get_current_admin),
):
    """Cria um novo produto (apenas admin)."""
    db_product = database.Product(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        category=payload.category,
        age_range=payload.age_range,
        emoji=payload.emoji,
        badge=payload.badge,
        featured=payload.featured,
        stock=payload.stock,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return Product(
        id=db_product.id,
        name=db_product.name,
        category=db_product.category,
        price=float(db_product.price),
        age_range=db_product.age_range or "",
        description=db_product.description or "",
        emoji=db_product.emoji or "🎁",
        badge=db_product.badge,
        featured=db_product.featured,
    )


@app.put("/admin/products/{product_id}", response_model=Product)
@limiter.limit("30/minute")
async def update_product(
    request: Request,
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _: database.User = Depends(get_current_admin),
):
    """Atualiza um produto existente (apenas admin)."""
    db_product = db.query(database.Product).filter(database.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)

    db_product.updated_at = datetime.utcnow()
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return Product(
        id=db_product.id,
        name=db_product.name,
        category=db_product.category,
        price=float(db_product.price),
        age_range=db_product.age_range or "",
        description=db_product.description or "",
        emoji=db_product.emoji or "🎁",
        badge=db_product.badge,
        featured=db_product.featured,
    )


@app.delete("/admin/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("30/minute")
async def delete_product(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db),
    _: database.User = Depends(get_current_admin),
):
    """Remove um produto (apenas admin)."""
    db_product = db.query(database.Product).filter(database.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(db_product)
    db.commit()
    return None


# =========================
# Cupons
# =========================


class Coupon(BaseModel):
    code: str
    discount_percent: float | None = None
    discount_value: float | None = None
    is_free_shipping: bool = False


COUPONS = {
    "SENSORI10": Coupon(code="SENSORI10", discount_percent=10.0),
    "BEMVINDO": Coupon(code="BEMVINDO", discount_value=20.0),
}


@app.get("/coupons/{code}", response_model=Coupon)
@limiter.limit("60/minute")
async def get_coupon(request: Request, code: str):
    """Busca cupom por código.

    Com DATABASE_URL configurada, busca no banco (considerando active/validade).
    Sem banco, usa o dicionário mockado em memória.
    """
    code_normalized = code.upper()

    if database.SessionLocal is None:
        coupon = COUPONS.get(code_normalized)
        if not coupon:
            raise HTTPException(status_code=404, detail="Cupom não encontrado")
        return coupon

    db = database.SessionLocal()
    try:
        db_coupon = (
            db.query(database.Coupon)
            .filter(database.Coupon.code == code_normalized)
            .first()
        )

        if not db_coupon or not db_coupon.active:
            raise HTTPException(status_code=404, detail="Cupom não encontrado")

        if db_coupon.expires_at and db_coupon.expires_at < datetime.utcnow():
            raise HTTPException(status_code=404, detail="Cupom expirado")

        return Coupon(
            code=db_coupon.code,
            discount_percent=float(db_coupon.discount_percent)
            if db_coupon.discount_percent is not None
            else None,
            discount_value=float(db_coupon.discount_value)
            if db_coupon.discount_value is not None
            else None,
            is_free_shipping=db_coupon.is_free_shipping,
        )
    finally:
        db.close()


# Configuração de conexão com o banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.warning(
        "DATABASE_URL não configurada. A API ainda está usando dados mockados em memória; "
        "configure a conexão real com PostgreSQL em produção.",
    )


# =========================
# Pedidos (Orders)
# =========================

import json

try:
    import mercadopago  # type: ignore
except ImportError:  # SDK é opcional em dev
    mercadopago = None  # type: ignore


# Configurações do Mercado Pago (via variáveis de ambiente)
MERCADOPAGO_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
MERCADOPAGO_PUBLIC_KEY = os.getenv("MERCADOPAGO_PUBLIC_KEY")
MERCADOPAGO_WEBHOOK_TOKEN = os.getenv("MERCADOPAGO_WEBHOOK_TOKEN")

# Frete: fixo, com frete grátis acima do threshold
SHIPPING_FLAT_COST = float(os.getenv("SHIPPING_FLAT_COST", "19.90"))
SHIPPING_FREE_THRESHOLD = float(os.getenv("SHIPPING_FREE_THRESHOLD", "199.00"))

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:8090")

# Status possíveis — espelha ORDER_STATUSES em database.py
VALID_ORDER_STATUSES = {
    "pending", "paid", "processing", "shipped", "delivered", "cancelled", "failed",
}

# Map de status do Mercado Pago -> status interno do pedido
MP_STATUS_MAP = {
    "approved": "paid",
    "authorized": "paid",
    "in_process": "pending",
    "pending": "pending",
    "in_mediation": "pending",
    "rejected": "failed",
    "cancelled": "cancelled",
    "refunded": "cancelled",
    "charged_back": "cancelled",
}


# -------- Schemas Pydantic --------


class ShippingAddress(BaseModel):
    name: str
    street: str
    number: str
    complement: str | None = None
    neighborhood: str
    city: str
    state: str
    zip_code: str
    phone: str | None = None


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemIn]
    coupon_code: str | None = None
    shipping_address: ShippingAddress


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    total_price: float


class OrderOut(BaseModel):
    id: int
    user_id: int
    total: float
    discount: float
    shipping_cost: float
    final_value: float
    shipping_address: dict | None = None
    status: str
    payment_provider: str | None = None
    payment_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    items: List[OrderItemOut] = []


class OrderStatusUpdate(BaseModel):
    status: str


class PayResponse(BaseModel):
    order_id: int
    init_point: str
    preference_id: str
    public_key: str | None = None


# -------- Helpers --------


def _calculate_shipping(subtotal: float, free_shipping_coupon: bool) -> float:
    if free_shipping_coupon:
        return 0.0
    if subtotal >= SHIPPING_FREE_THRESHOLD:
        return 0.0
    return SHIPPING_FLAT_COST


def _apply_coupon(db: Session, subtotal: float, code: str | None):
    """Retorna (discount, is_free_shipping, coupon_db_obj)."""
    if not code:
        return 0.0, False, None

    code_normalized = code.upper()
    coupon = (
        db.query(database.Coupon)
        .filter(database.Coupon.code == code_normalized)
        .first()
    )
    if not coupon or not coupon.active:
        raise HTTPException(status_code=400, detail="Cupom inválido")
    if coupon.expires_at and coupon.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Cupom expirado")
    if coupon.min_order_value and subtotal < float(coupon.min_order_value):
        raise HTTPException(
            status_code=400,
            detail=f"Cupom requer pedido mínimo de R$ {float(coupon.min_order_value):.2f}",
        )

    discount = 0.0
    if coupon.discount_percent:
        discount += subtotal * float(coupon.discount_percent) / 100.0
    if coupon.discount_value:
        discount += float(coupon.discount_value)

    discount = min(discount, subtotal)  # nunca deixar desconto maior que subtotal
    return discount, bool(coupon.is_free_shipping), coupon


def _order_to_out(order: database.Order) -> OrderOut:
    shipping_addr = None
    if order.shipping_address:
        try:
            shipping_addr = json.loads(order.shipping_address)
        except (ValueError, TypeError):
            shipping_addr = None

    return OrderOut(
        id=order.id,
        user_id=order.user_id,
        total=float(order.total_value or 0),
        discount=float(order.discount_value or 0),
        shipping_cost=float(order.shipping_cost or 0),
        final_value=float(order.final_value or 0),
        shipping_address=shipping_addr,
        status=order.status,
        payment_provider=order.payment_provider,
        payment_id=order.payment_id,
        created_at=order.created_at,
        updated_at=order.updated_at,
        items=[
            OrderItemOut(
                id=it.id,
                product_id=it.product_id,
                product_name=it.product_name_snapshot,
                quantity=it.quantity,
                unit_price=float(it.unit_price),
                total_price=float(it.total_price),
            )
            for it in order.items
        ],
    )


def _restock_order(db: Session, order: database.Order) -> None:
    """Devolve estoque reservado pelos itens do pedido."""
    for item in order.items:
        product = db.query(database.Product).filter(
            database.Product.id == item.product_id
        ).first()
        if product:
            product.stock = (product.stock or 0) + item.quantity
            db.add(product)


def create_mp_preference(order: database.Order) -> dict:
    """Cria uma preference no Mercado Pago e retorna o dict de response.

    Requer MERCADOPAGO_ACCESS_TOKEN e a lib `mercadopago` instalada.
    """
    if mercadopago is None:
        raise HTTPException(
            status_code=500,
            detail="SDK do Mercado Pago não instalada no servidor (pip install mercadopago)",
        )
    if not MERCADOPAGO_ACCESS_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="MERCADOPAGO_ACCESS_TOKEN não configurado",
        )

    sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)

    items_payload = [
        {
            "id": str(item.product_id),
            "title": item.product_name_snapshot,
            "quantity": item.quantity,
            "unit_price": float(item.unit_price),
            "currency_id": "BRL",
        }
        for item in order.items
    ]

    # Adiciona frete como item separado (se houver)
    if order.shipping_cost and float(order.shipping_cost) > 0:
        items_payload.append({
            "id": "shipping",
            "title": "Frete",
            "quantity": 1,
            "unit_price": float(order.shipping_cost),
            "currency_id": "BRL",
        })

    # Desconto do cupom: Mercado Pago não aceita valor negativo em item; ajustamos
    # manualmente os unit_prices proporcionalmente para bater com o final_value.
    if order.discount_value and float(order.discount_value) > 0 and items_payload:
        total_sem_desconto = sum(i["quantity"] * i["unit_price"] for i in items_payload)
        final = float(order.final_value)
        if total_sem_desconto > 0 and final > 0:
            ratio = final / total_sem_desconto
            for it in items_payload:
                it["unit_price"] = round(it["unit_price"] * ratio, 2)

    webhook_url = f"{os.getenv('BACKEND_BASE_URL', FRONTEND_BASE_URL)}/webhook/mercadopago"
    if MERCADOPAGO_WEBHOOK_TOKEN:
        webhook_url += f"?token={MERCADOPAGO_WEBHOOK_TOKEN}"

    preference_data = {
        "items": items_payload,
        "external_reference": str(order.id),
        "notification_url": webhook_url,
        "back_urls": {
            "success": f"{FRONTEND_BASE_URL}/pages/checkout-success.html?order_id={order.id}",
            "failure": f"{FRONTEND_BASE_URL}/pages/checkout-failed.html?order_id={order.id}",
            "pending": f"{FRONTEND_BASE_URL}/pages/checkout-pending.html?order_id={order.id}",
        },
        "auto_return": "approved",
    }

    result = sdk.preference().create(preference_data)
    if result.get("status") not in (200, 201):
        logger.error("Falha ao criar preference no MP: %s", result)
        raise HTTPException(status_code=502, detail="Falha ao criar preferência de pagamento")

    return result["response"]


# -------- Endpoints --------


@app.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
async def create_order(
    request: Request,
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Cria um novo pedido para o usuário logado.

    - Calcula subtotal a partir dos preços atuais dos produtos
    - Aplica cupom (se informado)
    - Calcula frete (fixo ou grátis)
    - Reserva estoque (decrementa) — se falhar, rollback
    - Status inicial = pending
    """
    if not payload.items:
        raise HTTPException(status_code=400, detail="Pedido precisa ter ao menos 1 item")

    # Consolidar itens duplicados
    consolidated: dict[int, int] = {}
    for item in payload.items:
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")
        consolidated[item.product_id] = consolidated.get(item.product_id, 0) + item.quantity

    # Buscar produtos e validar estoque
    product_ids = list(consolidated.keys())
    products = (
        db.query(database.Product)
        .filter(database.Product.id.in_(product_ids))
        .all()
    )
    product_by_id = {p.id: p for p in products}

    for pid, qty in consolidated.items():
        prod = product_by_id.get(pid)
        if not prod:
            raise HTTPException(status_code=404, detail=f"Produto {pid} não encontrado")
        if (prod.stock or 0) < qty:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente para '{prod.name}' (disponível: {prod.stock or 0})",
            )

    # Calcular totais
    subtotal = 0.0
    order_items_data = []
    for pid, qty in consolidated.items():
        prod = product_by_id[pid]
        unit_price = float(prod.price)
        line_total = unit_price * qty
        subtotal += line_total
        order_items_data.append({
            "product": prod,
            "quantity": qty,
            "unit_price": unit_price,
            "total_price": line_total,
        })

    discount, free_shipping, coupon = _apply_coupon(db, subtotal, payload.coupon_code)
    shipping = _calculate_shipping(subtotal, free_shipping)
    final_value = max(subtotal - discount + shipping, 0.0)

    now = datetime.utcnow()

    # Criar pedido
    order = database.Order(
        user_id=current_user.id,
        total_value=round(subtotal, 2),
        discount_value=round(discount, 2),
        shipping_cost=round(shipping, 2),
        final_value=round(final_value, 2),
        shipping_address=json.dumps(payload.shipping_address.model_dump()),
        status="pending",
        payment_provider=None,
        payment_id=None,
        coupon_id=coupon.id if coupon else None,
        created_at=now,
        updated_at=now,
    )
    db.add(order)
    db.flush()  # garantir order.id

    # Criar itens + reservar estoque
    for data in order_items_data:
        prod: database.Product = data["product"]
        item = database.OrderItem(
            order_id=order.id,
            product_id=prod.id,
            product_name_snapshot=prod.name,
            quantity=data["quantity"],
            unit_price=data["unit_price"],
            total_price=data["total_price"],
        )
        db.add(item)
        prod.stock = (prod.stock or 0) - data["quantity"]
        db.add(prod)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar pedido")

    db.refresh(order)
    return _order_to_out(order)


@app.get("/orders", response_model=List[OrderOut])
@limiter.limit("60/minute")
async def list_my_orders(
    request: Request,
    db: Session = Depends(get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Lista pedidos do usuário logado."""
    orders = (
        db.query(database.Order)
        .filter(database.Order.user_id == current_user.id)
        .order_by(database.Order.id.desc())
        .all()
    )
    return [_order_to_out(o) for o in orders]


@app.get("/orders/{order_id}", response_model=OrderOut)
@limiter.limit("60/minute")
async def get_order(
    request: Request,
    order_id: int,
    db: Session = Depends(get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Detalha um pedido. Acesso apenas para o dono ou admin."""
    order = db.query(database.Order).filter(database.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return _order_to_out(order)


@app.get("/admin/orders", response_model=List[OrderOut])
@limiter.limit("60/minute")
async def admin_list_orders(
    request: Request,
    status_filter: str | None = None,
    db: Session = Depends(get_db),
    _: database.User = Depends(get_current_admin),
):
    """Lista todos os pedidos (admin), com filtro opcional por status."""
    query = db.query(database.Order)
    if status_filter:
        if status_filter not in VALID_ORDER_STATUSES:
            raise HTTPException(status_code=400, detail="Status inválido")
        query = query.filter(database.Order.status == status_filter)
    orders = query.order_by(database.Order.id.desc()).all()
    return [_order_to_out(o) for o in orders]


@app.put("/admin/orders/{order_id}/status", response_model=OrderOut)
@limiter.limit("30/minute")
async def admin_update_order_status(
    request: Request,
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _: database.User = Depends(get_current_admin),
):
    """Admin atualiza status do pedido manualmente."""
    if payload.status not in VALID_ORDER_STATUSES:
        raise HTTPException(status_code=400, detail="Status inválido")

    order = db.query(database.Order).filter(database.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    old_status = order.status
    order.status = payload.status
    order.updated_at = datetime.utcnow()

    # Se admin cancela/falha um pedido que estava pendente, devolve estoque
    if payload.status in ("cancelled", "failed") and old_status == "pending":
        _restock_order(db, order)

    db.add(order)
    db.commit()
    db.refresh(order)
    return _order_to_out(order)


@app.post("/orders/{order_id}/pay", response_model=PayResponse)
@limiter.limit("20/minute")
async def pay_order(
    request: Request,
    order_id: int,
    db: Session = Depends(get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Cria uma preference no Mercado Pago e retorna o init_point (URL de checkout)."""
    order = db.query(database.Order).filter(database.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    if order.status not in ("pending",):
        raise HTTPException(
            status_code=400,
            detail=f"Pedido em status '{order.status}' não pode iniciar pagamento",
        )

    mp_response = create_mp_preference(order)

    preference_id = mp_response.get("id")
    init_point = mp_response.get("init_point") or mp_response.get("sandbox_init_point")

    if not init_point or not preference_id:
        raise HTTPException(status_code=502, detail="Resposta inválida do Mercado Pago")

    order.payment_provider = "mercadopago"
    order.payment_id = preference_id  # guardamos o preference_id; o payment_id real virá via webhook
    order.updated_at = datetime.utcnow()
    db.add(order)
    db.commit()

    return PayResponse(
        order_id=order.id,
        init_point=init_point,
        preference_id=preference_id,
        public_key=MERCADOPAGO_PUBLIC_KEY,
    )


@app.post("/webhook/mercadopago")
@limiter.limit("120/minute")
async def mercadopago_webhook(request: Request, token: str | None = None, db: Session = Depends(get_db)):
    """Webhook do Mercado Pago.

    Fluxo:
    1. Valida token de segurança (query param ?token=)
    2. Lê o body da notificação
    3. Se tipo=payment, consulta API do MP para obter status real
    4. Resolve o pedido via external_reference e atualiza status
    5. Se rejeitado/cancelado a partir de pending, devolve o estoque
    """
    expected_token = MERCADOPAGO_WEBHOOK_TOKEN
    if expected_token and token != expected_token:
        logger.warning("Webhook do Mercado Pago com token inválido.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de webhook inválido",
        )

    try:
        payload = await request.json()
    except Exception:
        payload = {}

    logger.info("Webhook do Mercado Pago recebido: %s", payload)

    notif_type = payload.get("type") or payload.get("topic")
    data = payload.get("data") or {}
    resource_id = data.get("id") or payload.get("resource") or payload.get("id")

    # Só tratamos notificações de pagamento (ignora merchant_order etc por ora)
    if notif_type not in ("payment", "payment.created", "payment.updated"):
        return {"received": True, "ignored": True, "type": notif_type}

    if not resource_id:
        logger.warning("Webhook sem resource id; ignorando.")
        return {"received": True, "ignored": True}

    if mercadopago is None or not MERCADOPAGO_ACCESS_TOKEN:
        logger.warning("Webhook recebido mas SDK/token do MP não disponível.")
        return {"received": True, "warning": "mp_sdk_unavailable"}

    # Consulta API do MP para obter o status real
    sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
    try:
        payment_response = sdk.payment().get(resource_id)
    except Exception as e:  # noqa: BLE001
        logger.exception("Erro ao consultar pagamento %s no MP: %s", resource_id, e)
        raise HTTPException(status_code=502, detail="Erro ao consultar MP")

    if payment_response.get("status") not in (200, 201):
        logger.warning("Pagamento %s não encontrado no MP: %s", resource_id, payment_response)
        return {"received": True, "not_found": True}

    payment_data = payment_response.get("response", {})
    mp_status = payment_data.get("status")
    external_reference = payment_data.get("external_reference")

    if not external_reference:
        logger.warning("Pagamento %s sem external_reference.", resource_id)
        return {"received": True, "no_reference": True}

    try:
        order_id_int = int(external_reference)
    except (TypeError, ValueError):
        logger.warning("external_reference inválido: %s", external_reference)
        return {"received": True, "invalid_reference": True}

    order = db.query(database.Order).filter(database.Order.id == order_id_int).first()
    if not order:
        logger.warning("Pedido %s do webhook não encontrado.", order_id_int)
        return {"received": True, "order_not_found": True}

    new_status = MP_STATUS_MAP.get(mp_status, order.status)
    old_status = order.status

    if new_status != old_status:
        order.status = new_status
        order.updated_at = datetime.utcnow()
        order.payment_id = str(resource_id)

        # Devolver estoque se pagamento foi recusado/cancelado a partir de pending
        if new_status in ("failed", "cancelled") and old_status == "pending":
            _restock_order(db, order)

        db.add(order)
        db.commit()

    return {
        "received": True,
        "order_id": order.id,
        "mp_status": mp_status,
        "order_status": order.status,
    }
