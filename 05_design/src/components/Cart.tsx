import type { Cart as CartType, CartItem } from '../types/Cart';

interface CartProps {
  cart: CartType | null;
  loading: boolean;
  error: string | null;
  onRemoveFromCart: (productId: string) => Promise<void>;
  totalItems: number;
  totalAmount: number;
}

export const Cart: React.FC<CartProps> = ({
  cart,
  loading,
  error,
  onRemoveFromCart,
  totalItems,
  totalAmount
}) => {
  const handleRemoveItem = async (productId: string) => {
    try {
      await onRemoveFromCart(productId);
    } catch (error) {
      console.error('Failed to remove item from cart:', error);
    }
  };

  if (error) {
    return (
      <div className="cart-container">
        <div className="cart-header">
          <h3>Shopping Cart</h3>
        </div>
        <div className="cart-error">
          <p>Error: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="cart-container">
      <div className="cart-header">
        <h3>Shopping Cart</h3>
        {totalItems > 0 && (
          <span className="cart-badge">{totalItems}</span>
        )}
      </div>

      {loading && (
        <div className="cart-loading">
          <p>Loading...</p>
        </div>
      )}

      {!loading && (!cart || cart.items.length === 0) && (
        <div className="cart-empty">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" className="empty-cart-icon">
            <path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17M17 13v4a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2v-4m8 0V9a2 2 0 0 0-2-2H9a2 2 0 0 0-2 2v4" stroke="currentColor" strokeWidth="2"/>
          </svg>
          <p>Your cart is empty</p>
        </div>
      )}

      {!loading && cart && cart.items.length > 0 && (
        <>
          <div className="cart-items">
            {cart.items.map((item: CartItem) => (
              <div key={item.productId} className="cart-item">
                <div className="cart-item-info">
                  <h4 className="cart-item-name">{item.productName}</h4>
                  <div className="cart-item-details">
                    <span className="cart-item-price">${item.productPrice}</span>
                    <span className="cart-item-quantity">Qty: {item.quantity}</span>
                  </div>
                  <div className="cart-item-total">
                    Total: ${item.totalPrice?.toFixed(2) || '0.00'}
                  </div>
                </div>
                <button
                  onClick={() => handleRemoveItem(item.productId)}
                  className="remove-item-button"
                  title="Remove from cart"
                  disabled={loading}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2"/>
                  </svg>
                </button>
              </div>
            ))}
          </div>

          <div className="cart-summary">
            <div className="cart-total">
              <strong>Total: ${totalAmount.toFixed(2)}</strong>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
