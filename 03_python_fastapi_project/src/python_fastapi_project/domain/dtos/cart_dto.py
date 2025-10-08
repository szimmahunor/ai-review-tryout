from pydantic import BaseModel, Field
from typing import List, Optional
from .base_dto import BaseAuditDTO

class AddToCartDTO(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=255, description="Cart session ID")
    product_id: int = Field(..., gt=0, description="Product ID to add to cart")
    quantity: int = Field(1, gt=0, description="Quantity to add")

class RemoveFromCartDTO(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=255, description="Cart session ID")
    product_id: int = Field(..., gt=0, description="Product ID to remove from cart")

class CartItemDTO(BaseAuditDTO):
    cart_id: int
    product_id: int
    product_name: str
    product_price: float
    quantity: int
    total_price: float

class CartDTO(BaseAuditDTO):
    session_id: str
    items: List[CartItemDTO]
    total_items: int
    total_amount: float

