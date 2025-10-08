from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseAudit

class Cart(BaseAudit):
    __tablename__ = "carts"

    session_id = Column(String(255), nullable=False, unique=True, index=True)

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
