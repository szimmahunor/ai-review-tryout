import { useState, useEffect, useCallback } from 'react';
import type { Cart } from '../types/Cart';
import { CartService } from '../services/CartService';

export const useCart = () => {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCart = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const cartData = await CartService.getCart();
      setCart(cartData); // This can be null if no cart exists, which is fine
    } catch (err) {
      // Only set error for actual failures, not for missing carts
      console.error('Error fetching cart:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch cart');
      // Set cart to null on error to ensure clean state
      setCart(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const addToCart = useCallback(async (productId: string, quantity: number = 1) => {
    try {
      setLoading(true);
      setError(null);
      const updatedCart = await CartService.addToCart(productId, quantity);
      console.log(updatedCart);
      setCart(updatedCart);
      return updatedCart;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to add to cart';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const removeFromCart = useCallback(async (productId: string) => {
    try {
      setLoading(true);
      setError(null);
      const updatedCart = await CartService.removeFromCart(productId);
      setCart(updatedCart);
      return updatedCart;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to remove from cart';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  const totalItems = cart?.totalItems || 0;
  const totalAmount = cart?.totalAmount || 0;

  return {
    cart,
    loading,
    error,
    addToCart,
    removeFromCart,
    fetchCart,
    totalItems,
    totalAmount
  };
};
