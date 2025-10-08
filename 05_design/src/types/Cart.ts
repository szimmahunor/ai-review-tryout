export interface CartItem {
  id: string;
  cartId: string;
  productId: string;
  productName: string;
  productPrice: number;
  quantity: number;
  totalPrice: number;
  createdAt: string;
  updatedAt: string;
}

export interface Cart {
  id: string;
  sessionId: string;
  items: CartItem[];
  totalItems: number;
  totalAmount: number;
  createdAt: string;
  updatedAt: string;
}

export interface AddToCartRequest {
  sessionId: string;
  productId: string;
  quantity: number;
}

export interface RemoveFromCartRequest {
  sessionId: string;
  productId: string;
}
