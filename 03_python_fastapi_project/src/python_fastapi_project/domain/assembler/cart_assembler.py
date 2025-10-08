from typing import List
from ..models.cart import Cart, CartItem
from ..dtos.cart_dto import CartDTO, CartItemDTO

class CartAssembler:

    @staticmethod
    def to_cart_dto(cart: Cart) -> CartDTO:
        items = [CartAssembler.to_cart_item_dto(item) for item in cart.items]
        total_items = sum(item.quantity for item in items)
        total_amount = round(sum(item.total_price for item in items), 2)

        return CartDTO(
            id=cart.id,
            created_by=cart.created_by,
            created_at=cart.created_at,
            updated_by=cart.updated_by,
            updated_at=cart.updated_at,
            session_id=cart.session_id,
            items=items,
            total_items=total_items,
            total_amount=total_amount
        )

    @staticmethod
    def to_cart_item_dto(cart_item: CartItem) -> CartItemDTO:
        total_price = round(float(cart_item.product.price) * cart_item.quantity, 2)

        return CartItemDTO(
            id=cart_item.id,
            created_by=cart_item.created_by,
            created_at=cart_item.created_at,
            updated_by=cart_item.updated_by,
            updated_at=cart_item.updated_at,
            cart_id=cart_item.cart_id,
            product_id=cart_item.product_id,
            product_name=cart_item.product.name,
            product_price=float(cart_item.product.price),
            quantity=cart_item.quantity,
            total_price=total_price
        )
