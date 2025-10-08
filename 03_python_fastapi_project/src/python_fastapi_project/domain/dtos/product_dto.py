from pydantic import BaseModel, Field
from typing import Optional
from .base_dto import BaseAuditDTO

class ProductCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    stock: int = Field(..., ge=0, description="Available stock quantity")
    price: float = Field(..., gt=0, description="Product price")

class ProductUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    stock: Optional[int] = Field(None, ge=0, description="Available stock quantity")
    price: Optional[float] = Field(None, gt=0, description="Product price")

class ProductOverviewDTO(BaseAuditDTO):
    name: str
    price: float
    stock: int

class ProductDetailDTO(BaseAuditDTO):
    name: str
    description: Optional[str]
    stock: int
    price: float
