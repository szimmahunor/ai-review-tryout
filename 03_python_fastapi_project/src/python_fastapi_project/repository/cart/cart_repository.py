from abc import ABC, abstractmethod
from typing import List, Optional

from src.python_fastapi_project.domain.models.cart import Cart, CartItem


class CartRepository(ABC):
    @abstractmethod
    async def create_cart(self, cart: Cart) -> Cart:
        pass

    @abstractmethod
    async def get_cart_by_session_id(self, session_id: str) -> Optional[Cart]:
        pass

    @abstractmethod
    async def add_item_to_cart(self, cart_item: CartItem) -> CartItem:
        pass

    @abstractmethod
    async def get_cart_item(self, cart_id: int, product_id: int) -> Optional[CartItem]:
        pass

    @abstractmethod
    async def update_cart_item(self, cart_item: CartItem) -> CartItem:
        pass

    @abstractmethod
    async def remove_cart_item(self, cart_id: int, product_id: int) -> bool:
        pass

    @abstractmethod
    async def clear_cart(self, cart_id: int) -> bool:
        pass
