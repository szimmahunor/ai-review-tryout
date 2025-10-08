from typing import List, Optional

from src.python_fastapi_project.domain.dtos import (
    ProductCreateDTO,
    ProductUpdateDTO,
    ProductOverviewDTO,
    ProductDetailDTO,
)
from src.python_fastapi_project.domain.assembler.product_assembler import ProductAssembler
from src.python_fastapi_project.repository.product.product_repository import ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository

    async def create_product(self, create_dto: ProductCreateDTO) -> ProductDetailDTO:
        """Create a new product"""
        product = ProductAssembler.from_create_dto(create_dto, "system")
        created_product = await self._product_repository.create(product)
        return ProductAssembler.to_detail_dto(created_product)

    async def get_product_by_id(self, product_id: int) -> Optional[ProductDetailDTO]:
        """Get a product by its ID"""
        product = await self._product_repository.get_by_id(product_id)
        if product is None:
            return None
        return ProductAssembler.to_detail_dto(product)

    async def get_all_products(self) -> List[ProductDetailDTO]:
        """Get all products as overview DTOs"""
        products = await self._product_repository.get_all()
        return ProductAssembler.to_detail_dtos(products)

    async def update_product(self, product_id: int, update_dto: ProductUpdateDTO) -> Optional[ProductDetailDTO]:
        """Update an existing product"""
        product = await self._product_repository.get_by_id(product_id)
        if product is None:
            return None

        updated_product = ProductAssembler.update_from_dto(product, update_dto, "system")
        saved_product = await self._product_repository.update(updated_product)
        return ProductAssembler.to_detail_dto(saved_product)

    async def delete_product(self, product_id: int) -> bool:
        """Delete a product by its ID"""
        return await self._product_repository.delete(product_id)

    async def get_products_by_name(self, name: str) -> List[ProductOverviewDTO]:
        """Get products filtered by name (if repository supports it)"""
        # This would require additional repository method, for now return all and filter
        all_products = await self._product_repository.get_all()
        filtered_products = [p for p in all_products if name.lower() in p.name.lower()]
        return ProductAssembler.to_detail_dtos(filtered_products)

    async def check_product_availability(self, product_id: int, required_quantity: int) -> bool:
        """Check if a product has sufficient stock"""
        product = await self._product_repository.get_by_id(product_id)
        if product is None:
            return False
        return product.stock >= required_quantity

    async def update_product_stock(self, product_id: int, new_stock: int) -> Optional[ProductDetailDTO]:
        """Update only the stock of a product"""
        product = await self._product_repository.get_by_id(product_id)
        if product is None:
            return None

        update_dto = ProductUpdateDTO()
        update_dto.stock = new_stock

        updated_product = ProductAssembler.update_from_dto(product, update_dto, "system")
        saved_product = await self._product_repository.update(updated_product)
        return ProductAssembler.to_detail_dto(saved_product)
