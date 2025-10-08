import React from 'react';
import type { Product } from '../types/Product';

interface ViewProductModalProps {
  isOpen: boolean;
  onClose: () => void;
  product: Product | null;
}

export const ViewProductModal: React.FC<ViewProductModalProps> = ({
  isOpen,
  onClose,
  product
}) => {
  if (!isOpen || !product) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Product Details</h2>
          <button onClick={onClose} className="close-button">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2"/>
            </svg>
          </button>
        </div>

        <div className="product-details">
          <h3>{product.name}</h3>
          <p className="details-description">
            {product.description || 'No description available.'}
          </p>

          <hr className="separator" />

          <div className="details-row">
            <span className="details-label">Price:</span>
            <span className="details-price">${product.price}</span>
          </div>

          <div className="details-row">
            <span className="details-label">Stock:</span>
            <span className="details-value">{product.stock} units</span>
          </div>

          <div className="details-row">
            <span className="details-label">Product ID:</span>
            <span className="details-value">{product.id}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
