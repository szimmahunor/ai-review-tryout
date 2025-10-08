from typing import List
from fastapi import APIRouter, HTTPException, Depends, status

from ..domain.dtos.product_dto import (
    ProductCreateDTO,
    ProductUpdateDTO,
    ProductOverviewDTO,
    ProductDetailDTO,
)
from ..service.product_service import ProductService
from ..dependencies import get_product_service

# Create router
router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductDetailDTO, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreateDTO,
    product_service: ProductService = Depends(get_product_service)
) -> ProductDetailDTO:
    """
    Create a new product.

    - **name**: Product name (required)
    - **description**: Product description
    - **stock**: Available stock quantity (required)
    - **price**: Product price (required)
    """
    try:
        created_product = await product_service.create_product(product_data)
        return created_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create product: {str(e)}"
        )

@router.get("/", response_model=List[ProductDetailDTO])
async def get_all_products(
    product_service: ProductService = Depends(get_product_service)
) -> List[ProductOverviewDTO]:
    """
    Retrieve all products as overview (basic information).
    """
    try:
        products = await product_service.get_all_products()
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve products: {str(e)}"
        )

@router.get("/{product_id}", response_model=ProductDetailDTO)
async def get_product_by_id(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
) -> ProductDetailDTO:
    """
    Retrieve a specific product by ID with full details.

    - **product_id**: The ID of the product to retrieve
    """
    try:
        product = await product_service.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve product: {str(e)}"
        )

@router.put("/{product_id}", response_model=ProductDetailDTO)
async def update_product(
    product_id: int,
    product_data: ProductUpdateDTO,
    product_service: ProductService = Depends(get_product_service)
) -> ProductDetailDTO:
    """
    Update an existing product.

    - **product_id**: The ID of the product to update
    - **name**: New product name (optional)
    - **description**: New product description (optional)
    - **stock**: New stock quantity (optional)
    - **price**: New product price (optional)
    """
    try:
        updated_product = await product_service.update_product(product_id, product_data)
        if updated_product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        return updated_product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update product: {str(e)}"
        )

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
):
    """
    Delete a product by ID.

    - **product_id**: The ID of the product to delete
    """
    try:
        success = await product_service.delete_product(product_id)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete product: {str(e)}"
        )

@router.get("/search/{name}", response_model=List[ProductOverviewDTO])
async def search_products_by_name(
    name: str,
    product_service: ProductService = Depends(get_product_service)
) -> List[ProductOverviewDTO]:
    """
    Search products by name.

    - **name**: The name or partial name to search for
    """
    try:
        products = await product_service.get_products_by_name(name)
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search products: {str(e)}"
        )
