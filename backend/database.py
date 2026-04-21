import os

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLite precisa de `check_same_thread=False` quando usado com FastAPI/threads
connect_args = {}
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args) if DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None
Base = declarative_base()


# =========================
# Status possíveis de pedido
# =========================
ORDER_STATUSES = {
    "pending",      # criado, aguardando pagamento
    "paid",         # pagamento aprovado
    "processing",   # separando/embalando
    "shipped",      # enviado
    "delivered",    # entregue
    "cancelled",    # cancelado pelo usuário/admin
    "failed",       # pagamento recusado
}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True, index=True)
    password_hash = Column(Text, nullable=False)
    is_admin = Column(Boolean, default=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50), nullable=False)
    age_range = Column(String(10))
    emoji = Column(Text)
    badge = Column(String(50))
    featured = Column(Boolean, default=False)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(Text)
    discount_percent = Column(Numeric(5, 2))
    discount_value = Column(Numeric(10, 2))
    is_free_shipping = Column(Boolean, default=False)
    min_order_value = Column(Numeric(10, 2))
    active = Column(Boolean, default=True)
    expires_at = Column(DateTime)
    created_at = Column(DateTime)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Valores financeiros
    total_value = Column(Numeric(10, 2), nullable=False)       # subtotal (antes do desconto/frete)
    discount_value = Column(Numeric(10, 2), default=0)         # desconto do cupom
    shipping_cost = Column(Numeric(10, 2), default=0)          # valor do frete cobrado
    final_value = Column(Numeric(10, 2), nullable=False)       # total final (subtotal - desconto + frete)

    # Endereço de entrega (JSON serializado como texto — compat SQLite)
    shipping_address = Column(Text)

    # Status e pagamento
    status = Column(String(30), nullable=False, default="pending", index=True)
    payment_provider = Column(String(30))
    payment_id = Column(Text)

    coupon_id = Column(Integer, ForeignKey("coupons.id"))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    user = relationship("User")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # Snapshot do nome do produto no momento da compra (preserva histórico)
    product_name_snapshot = Column(Text, nullable=False)

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


def get_db():
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL não configurada. Conexão com banco indisponível.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
