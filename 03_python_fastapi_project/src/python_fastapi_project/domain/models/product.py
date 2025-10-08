from sqlalchemy import Column, Integer, String, Numeric
from .base import BaseAudit

class Product(BaseAudit):
    __tablename__ = "products"

    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    stock = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
