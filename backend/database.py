import os

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) if DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None
Base = declarative_base()


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


def get_db():
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL não configurada. Conexão com banco indisponível." )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
