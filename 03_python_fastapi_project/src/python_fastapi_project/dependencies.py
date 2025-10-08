"""
Dependency injection container for the FastAPI application.
This module centralizes the creation and management of service and repository instances.

TODO: use a lib to do this, as this is not scalable
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.python_fastapi_project.repository.database import create_db_session
from src.python_fastapi_project.repository.product.product_repository_impl import ProductRepositoryImpl
from src.python_fastapi_project.repository.product.product_repository import ProductRepository
from src.python_fastapi_project.repository.cart.cart_repository_impl import CartRepositoryImpl
from src.python_fastapi_project.repository.cart.cart_repository import CartRepository
from src.python_fastapi_project.service.product_service import ProductService
from src.python_fastapi_project.service.cart_service import CartService


# Repository Layer Dependencies
async def get_product_repository(db: AsyncSession = Depends(create_db_session)) -> ProductRepository:
    """Create and return a ProductRepository instance with database session"""
    return ProductRepositoryImpl(db)


async def get_cart_repository(db: AsyncSession = Depends(create_db_session)) -> CartRepository:
    """Create and return a CartRepository instance with database session"""
    return CartRepositoryImpl(db)


# Service Layer Dependencies
async def get_product_service(
    product_repository: ProductRepository = Depends(get_product_repository)
) -> ProductService:
    """Create and return a ProductService instance with injected repository"""
    return ProductService(product_repository)


async def get_cart_service(
    cart_repository: CartRepository = Depends(get_cart_repository),
    product_repository: ProductRepository = Depends(get_product_repository)
) -> CartService:
    """Create and return a CartService instance with injected repositories"""
    return CartService(cart_repository, product_repository)
