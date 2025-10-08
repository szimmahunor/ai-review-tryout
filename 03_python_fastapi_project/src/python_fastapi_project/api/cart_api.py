from fastapi import APIRouter, HTTPException, Depends, status

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
    cart_service: CartService = Depends(get_cart_service)
) -> CartDTO:
    """
    Add a product to the cart.

    - **session_id**: Cart session ID (required)
    - **product_id**: Product ID to add (required)
    - **quantity**: Quantity to add (default: 1)
    """
    try:
        updated_cart = await cart_service.add_to_cart(add_dto)
        return updated_cart
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to add product to cart: {str(e)}"
        )

@router.delete("/remove", response_model=CartDTO, status_code=status.HTTP_200_OK)
async def remove_from_cart(
    remove_dto: RemoveFromCartDTO,
    cart_service: CartService = Depends(get_cart_service)
) -> CartDTO:
    """
    Remove a product from the cart.

    - **session_id**: Cart session ID (required)
    - **product_id**: Product ID to remove (required)
    """
    try:
        updated_cart = await cart_service.remove_from_cart(remove_dto)
        return updated_cart
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to remove product from cart: {str(e)}"
        )

@router.get("/{session_id}", response_model=CartDTO)
async def get_cart(
    session_id: str,
    cart_service: CartService = Depends(get_cart_service)
) -> CartDTO:
    """
    Get cart contents by session ID. Creates cart if it doesn't exist.

    - **session_id**: Cart session ID (required)
    """
    try:
        cart = await cart_service.get_cart(session_id)
        return cart
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve cart: {str(e)}"
        )
