import type { Cart } from '../types/Cart';

const API_BASE_URL = 'http://localhost:8000/api';
const CART_SESSION_KEY = 'cart_session_id';

// Transform backend response to frontend format
const transformCartResponse = (backendCart: any): Cart => {
  return {
    id: backendCart.id?.toString() || '',
    sessionId: backendCart.session_id,
    items: backendCart.items?.map((item: any) => ({
      id: item.id?.toString() || '',
      cartId: item.cart_id?.toString() || '',
      productId: item.product_id?.toString() || '',
      productName: item.product_name,
      productPrice: item.product_price,
      quantity: item.quantity,
      totalPrice: item.total_price,
      createdAt: item.created_at,
      updatedAt: item.updated_at
    })) || [],
    totalItems: backendCart.total_items || 0,
    totalAmount: backendCart.total_amount || 0,
    createdAt: backendCart.created_at || '',
    updatedAt: backendCart.updated_at || ''
  };
};

export class CartService {
  private static generateSessionId(): string {
    // Generate a more robust session ID with timestamp and random components
    const timestamp = Date.now().toString(36);
    const randomPart = Math.random().toString(36).substr(2, 9);
    return `session_${timestamp}_${randomPart}`;
  }

  private static getOrCreateSessionId(): string {
    // Try to get existing session ID from localStorage
    let sessionId = localStorage.getItem(CART_SESSION_KEY);

    if (!sessionId) {
      // Generate new session ID and save to localStorage
      sessionId = this.generateSessionId();
      localStorage.setItem(CART_SESSION_KEY, sessionId);
      console.log('Created new cart session:', sessionId);
    }

    return sessionId;
  }

  static clearSession(): void {
    // Method to clear the cart session (useful for logout, etc.)
    localStorage.removeItem(CART_SESSION_KEY);
  }

  static async addToCart(productId: string, quantity: number = 1): Promise<Cart> {
    const sessionId = this.getOrCreateSessionId();
    const request = {
      session_id: sessionId,
      product_id: productId,
      quantity
    };

    const response = await fetch(`${API_BASE_URL}/cart/add`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to add item to cart');
    }

    const backendCart = await response.json();
    return transformCartResponse(backendCart);
  }

  static async removeFromCart(productId: string): Promise<Cart> {
    const sessionId = this.getOrCreateSessionId();
    const request = {
      session_id: sessionId,
      product_id: productId
    };

    const response = await fetch(`${API_BASE_URL}/cart/remove`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to remove item from cart');
    }

    const backendCart = await response.json();
    return transformCartResponse(backendCart);
  }

  static async getCart(): Promise<Cart | null> {
    const sessionId = this.getOrCreateSessionId();

    const response = await fetch(`${API_BASE_URL}/cart/${sessionId}`);

    if (!response.ok) {
      // If cart doesn't exist (404), return null instead of throwing error
      if (response.status === 404) {
        return null;
      }
      // For other errors, still throw
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch cart');
    }

    const backendCart = await response.json();
    return transformCartResponse(backendCart);
  }
}
