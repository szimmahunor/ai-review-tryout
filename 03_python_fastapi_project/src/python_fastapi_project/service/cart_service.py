from typing import Optional
from fastapi import HTTPException

from src.python_fastapi_project.domain.dtos.cart_dto import (
    AddToCartDTO,
    RemoveFromCartDTO,
    CartDTO
)
from src.python_fastapi_project.domain.assembler.cart_assembler import CartAssembler
from src.python_fastapi_project.domain.models.cart import Cart, CartItem
from src.python_fastapi_project.repository.cart.cart_repository import CartRepository
from src.python_fastapi_project.repository.product.product_repository import ProductRepository


class CartService:
    def __init__(self, cart_repository: CartRepository, product_repository: ProductRepository):
        self._cart_repository = cart_repository
        self._product_repository = product_repository

    async def add_to_cart(self, add_dto: AddToCartDTO) -> CartDTO:
        """Add a product to the cart"""
        # Check if product exists and has sufficient stock
        product = await self._product_repository.get_by_id(add_dto.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.stock < add_dto.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock available")

        # Get or create cart
        cart = await self._cart_repository.get_cart_by_session_id(add_dto.session_id)
        if not cart:
            cart = Cart(session_id=add_dto.session_id, created_by="system")
            cart = await self._cart_repository.create_cart(cart)

        # Check if item already exists in cart
        existing_item = await self._cart_repository.get_cart_item(cart.id, add_dto.product_id)

        if existing_item:
            # Check if adding quantity would exceed stock
            new_quantity = existing_item.quantity + add_dto.quantity
            if product.stock < new_quantity:
                raise HTTPException(status_code=400, detail="Insufficient stock available")

            existing_item.quantity = new_quantity
            existing_item.updated_by = "system"
            await self._cart_repository.update_cart_item(existing_item)
        else:
            # Create new cart item
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=add_dto.product_id,
                quantity=add_dto.quantity,
                created_by="system"
            )
            await self._cart_repository.add_item_to_cart(cart_item)

        # Update product stock
        product.stock -= add_dto.quantity
        await self._product_repository.update(product)

        # Return updated cart with explicit fresh retrieval
        # The key issue was that we need to ensure the cart is retrieved
        # with all its items properly loaded after the transaction commits
        updated_cart = await self._cart_repository.get_cart_by_session_id(add_dto.session_id)
        if not updated_cart:
            raise HTTPException(status_code=500, detail="Failed to retrieve updated cart")

        return CartAssembler.to_cart_dto(updated_cart)

    async def remove_from_cart(self, remove_dto: RemoveFromCartDTO) -> CartDTO:
        """Remove a product from the cart"""
        cart = await self._cart_repository.get_cart_by_session_id(remove_dto.session_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        cart_item = await self._cart_repository.get_cart_item(cart.id, remove_dto.product_id)
        if not cart_item:
            raise HTTPException(status_code=404, detail="Product not found in cart")

        # Restore stock
        product = await self._product_repository.get_by_id(remove_dto.product_id)
        if product:
            product.stock += cart_item.quantity
            await self._product_repository.update(product)

        # Remove cart item
        await self._cart_repository.remove_cart_item(cart.id, remove_dto.product_id)

        # Return updated cart
        updated_cart = await self._cart_repository.get_cart_by_session_id(remove_dto.session_id)
        return CartAssembler.to_cart_dto(updated_cart)

    async def get_cart(self, session_id: str) -> CartDTO:
        """Get cart contents by session ID, create if doesn't exist"""
        cart = await self._cart_repository.get_cart_by_session_id(session_id)
        if not cart:
            # Create a new empty cart for this session
            cart = Cart(session_id=session_id, created_by="system")
            cart = await self._cart_repository.create_cart(cart)

        return CartAssembler.to_cart_dto(cart)
