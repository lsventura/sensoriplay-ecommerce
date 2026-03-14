import logging
import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

import database

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
