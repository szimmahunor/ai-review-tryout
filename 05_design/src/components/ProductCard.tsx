import React from 'react';
import type { Product } from '../types/Product';

interface ProductCardProps {
  product: Product;
  onView: (product: Product) => void;
  onEdit: (product: Product) => void;
  onDelete: (product: Product) => void;
  loading: boolean;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onView,
  onEdit,
  onDelete,
  loading
}) => {
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
