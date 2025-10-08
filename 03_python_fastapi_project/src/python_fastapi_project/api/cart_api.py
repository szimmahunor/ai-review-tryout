from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated

from ..domain.dtos.cart_dto import (
    AddToCartDTO,
    RemoveFromCartDTO,
    CartDTO
)
from ..service.cart_service import CartService
from ..dependencies import get_cart_service

# Create router
router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add", response_model=CartDTO, status_code=status.HTTP_200_OK)
async def add_to_cart(
    add_dto: AddToCartDTO,
    cart_service: Annotated[CartService, Depends(get_cart_service)]
) -> CartDTO:
    """
    Add a product to the cart.

    - **session_id**: Cart session ID (required)
    - **product_id**: Product ID to add (required)
    - **quantity**: Quantity to add (default: 1)
    """
    try:
        return await cart_service.add_to_cart(add_dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to add product to cart: {e!r}"
        ) from e

@router.delete("/remove", response_model=CartDTO, status_code=status.HTTP_200_OK)
async def remove_from_cart(
    remove_dto: RemoveFromCartDTO,
    cart_service: Annotated[CartService, Depends(get_cart_service)]
) -> CartDTO:
    """
    Remove a product from the cart.

    - **session_id**: Cart session ID (required)
    - **product_id**: Product ID to remove (required)
    """
    try:
        return await cart_service.remove_from_cart(remove_dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to remove product from cart: {e!r}"
        ) from e

@router.get("/{session_id}", response_model=CartDTO)
async def get_cart(
    session_id: str,
    cart_service: Annotated[CartService, Depends(get_cart_service)]
) -> CartDTO:
    """
    Get cart contents by session ID. Creates cart if it doesn't exist.

    - **session_id**: Cart session ID (required)
    """
    try:
        return await cart_service.get_cart(session_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve cart: {e!r}"
        ) from e
