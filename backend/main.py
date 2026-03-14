import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from pydantic import BaseModel
=======
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
>>>>>>> cc2c69f15bca8feb81e0920aae006fb14d4e3f11
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
async def register_user(payload: UserCreate, db: Session = Depends(get_db)):
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
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail ou senha inválidos")

    access_token = create_access_token({"sub": str(user.id), "is_admin": user.is_admin})
    return Token(access_token=access_token)


@app.post("/auth/google", response_model=Token)
@limiter.limit("30/minute")
async def google_login(payload: GoogleLoginRequest, db: Session = Depends(get_db)):
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
async def read_me(current_user: database.User = Depends(get_current_user)):
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


# Configurações do Mercado Pago (via variáveis de ambiente)
MERCADOPAGO_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
MERCADOPAGO_WEBHOOK_TOKEN = os.getenv("MERCADOPAGO_WEBHOOK_TOKEN")


@app.post("/webhook/mercadopago")
@limiter.limit("60/minute")
async def mercadopago_webhook(request: Request, token: str | None = None):
    """Endpoint de webhook do Mercado Pago.

    Configure a URL de notificação no painel do Mercado Pago como:
    https://sua-api.com/webhook/mercadopago?token=SEU_WEBHOOK_TOKEN

    E defina MERCADOPAGO_WEBHOOK_TOKEN nas variáveis de ambiente.
    """
    expected_token = MERCADOPAGO_WEBHOOK_TOKEN
    if expected_token and token != expected_token:
        logger.warning("Webhook do Mercado Pago com token inválido.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de webhook inválido",
        )

    payload = await request.json()
    logger.info("Webhook do Mercado Pago recebido: %s", payload)

    # TODO: consultar a API do Mercado Pago para confirmar o status do pagamento
    # antes de atualizar o status do pedido no banco de dados.

    return {"received": True}
