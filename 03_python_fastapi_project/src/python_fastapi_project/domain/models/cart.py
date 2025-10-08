from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from .base import BaseAudit

class Cart(BaseAudit):
    __tablename__ = "carts"

    session_id = Column(String(255), nullable=False, unique=True)

    # Relationship to access cart items
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(BaseAudit):
    __tablename__ = "cart_items"

    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    # Relationships
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")

    # Table constraints
    __table_args__ = (
        UniqueConstraint('cart_id', 'product_id', name='uq_cart_product'),
        CheckConstraint('quantity > 0', name='ck_positive_quantity'),
    )
