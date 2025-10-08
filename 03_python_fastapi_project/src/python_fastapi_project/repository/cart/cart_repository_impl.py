from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .cart_repository import CartRepository
from ...domain.models.cart import Cart, CartItem

class CartRepositoryImpl(CartRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cart(self, cart: Cart) -> Cart:
        self.db.add(cart)
        await self.db.commit()
        await self.db.refresh(cart)
        return cart

    async def get_cart_by_session_id(self, session_id: str) -> Optional[Cart]:
        # Flush any pending changes to ensure database is up to date
        await self.db.flush()

        result = await self.db.execute(
            select(Cart)
            .options(selectinload(Cart.items).selectinload(CartItem.product))
            .where(Cart.session_id == session_id)
        )
        cart = result.scalar_one_or_none()

        if cart:
            # Refresh the cart to ensure we have the latest data including items
            await self.db.refresh(cart, ['items'])

        return cart

    async def add_item_to_cart(self, cart_item: CartItem) -> CartItem:
        self.db.add(cart_item)
        await self.db.commit()
        await self.db.refresh(cart_item)
        return cart_item

    async def get_cart_item(self, cart_id: int, product_id: int) -> Optional[CartItem]:
        result = await self.db.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.cart_id == cart_id)
            .where(CartItem.product_id == product_id)
        )
        return result.scalar_one_or_none()

    async def update_cart_item(self, cart_item: CartItem) -> CartItem:
        await self.db.commit()
        await self.db.refresh(cart_item)
        return cart_item

    async def remove_cart_item(self, cart_id: int, product_id: int) -> bool:
        cart_item = await self.get_cart_item(cart_id, product_id)
        if cart_item:
            await self.db.delete(cart_item)
            await self.db.commit()
            return True
        return False

    async def clear_cart(self, cart_id: int) -> bool:
        result = await self.db.execute(
            select(CartItem).where(CartItem.cart_id == cart_id)
        )
        cart_items = result.scalars().all()
        for item in cart_items:
            await self.db.delete(item)
        await self.db.commit()
        return True
