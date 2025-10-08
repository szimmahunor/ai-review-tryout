from datetime import datetime
from ..models import Product
from ..dtos import (
    ProductCreateDTO,
    ProductUpdateDTO,
    ProductOverviewDTO,
    ProductDetailDTO,
)

class ProductAssembler:

    @staticmethod
    def to_overview_dto(product: Product) -> ProductOverviewDTO:
        """Convert Product model to ProductOverviewDTO"""
        return ProductOverviewDTO(
            id=product.id,
            created_by=product.created_by,
            created_at=product.created_at,
            updated_by=product.updated_by,
            updated_at=product.updated_at,
            name=product.name,
            price=float(product.price),
            stock=product.stock
        )

    @staticmethod
    def to_detail_dto(product: Product) -> ProductDetailDTO:
        """Convert Product model to ProductDetailDTO"""
        return ProductDetailDTO(
            id=product.id,
            created_by=product.created_by,
            created_at=product.created_at,
            updated_by=product.updated_by,
            updated_at=product.updated_at,
            name=product.name,
            description=product.description,
            stock=product.stock,
            price=float(product.price)
        )

    @staticmethod
    def to_detail_dtos(products: list[Product]) -> list[ProductDetailDTO]:
        """Convert list of Product models to list of ProductDetailDTO"""
        return [ProductAssembler.to_detail_dto(product) for product in products]

    @staticmethod
    def from_create_dto(create_dto: ProductCreateDTO, created_by: str) -> Product:
        """Convert ProductCreateDTO to Product model"""
        now = datetime.now()
        product = Product()
        product.name = create_dto.name
        product.description = create_dto.description
        product.stock = create_dto.stock
        product.price = create_dto.price
        product.created_by = created_by
        product.created_at = now
        product.updated_by = created_by
        product.updated_at = now
        return product

    @staticmethod
    def update_from_dto(product: Product, update_dto: ProductUpdateDTO, updated_by: str) -> Product:
        """Update Product model from ProductUpdateDTO"""
        if update_dto.name is not None:
            product.name = update_dto.name
        if update_dto.description is not None:
            product.description = update_dto.description
        if update_dto.stock is not None:
            product.stock = update_dto.stock
        if update_dto.price is not None:
            product.price = update_dto.price

        product.updated_by = updated_by
        product.updated_at = datetime.now()
        return product
