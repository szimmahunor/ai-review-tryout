import React, { useState } from 'react';
import type { Product } from '../types/Product';

interface ProductCardProps {
  product: Product;
  onView: (product: Product) => void;
  onEdit: (product: Product) => void;
  onDelete: (product: Product) => void;
  onAddToCart: (productId: string) => Promise<void>;
  loading: boolean;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onView,
  onEdit,
  onDelete,
  onAddToCart,
  loading
}) => {
  const [addingToCart, setAddingToCart] = useState(false);

  const handleAddToCart = async () => {
    try {
      setAddingToCart(true);
      await onAddToCart(product.id);
    } catch (error) {
      // Error handling is done in parent component
    } finally {
      setAddingToCart(false);
    }
  };

  return (
    <div className="product-card">
      <h4 className="product-name">{product.name}</h4>

      <div className="product-content">
        <p className="product-description">
          {product.description || 'No description available.'}
        </p>

        <div className="product-footer">
          <span className="product-stock">Stock: {product.stock}</span>
          <span className="product-price">${product.price}</span>
        </div>
      </div>

      <div className="product-actions">
        <button
          onClick={handleAddToCart}
          className="action-button add-to-cart-button"
          disabled={loading || addingToCart || product.stock === 0}
          title={product.stock === 0 ? "Out of stock" : "Add to cart"}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17M17 13v4a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2v-4m8 0V9a2 2 0 0 0-2-2H9a2 2 0 0 0-2 2v4" stroke="currentColor" strokeWidth="2"/>
          </svg>
          {addingToCart ? '...' : 'Cart'}
        </button>

        <button
          onClick={() => onView(product)}
          className="action-button view-button"
          disabled={loading}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" stroke="currentColor" strokeWidth="2"/>
            <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2"/>
          </svg>
          View
        </button>

        <button
          onClick={() => onEdit(product)}
          className="action-button edit-button"
          disabled={loading}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" strokeWidth="2"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5Z" stroke="currentColor" strokeWidth="2"/>
          </svg>
          Edit
        </button>

        <button
          onClick={() => onDelete(product)}
          className="action-button delete-button"
          disabled={loading}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6" stroke="currentColor" strokeWidth="2"/>
          </svg>
        </button>
      </div>
    </div>
  );
};
