import { useState } from 'react'
import './App.css'
import { useProducts } from './hooks/useProducts'
import { useProductModals } from './hooks/useProductModals'
import { ProductCard } from './components/ProductCard'
import { AddProductModal } from './components/AddProductModal'
import { EditProductModal } from './components/EditProductModal'
import { ViewProductModal } from './components/ViewProductModal'
import { DeleteProductModal } from './components/DeleteProductModal'

function App() {
  const [searchTerm, setSearchTerm] = useState('');

  // Use custom hooks for cleaner state management
  const { products, loading, error, createProduct, updateProduct, deleteProduct } = useProducts();
  const {
    isAddModalOpen,
    isEditModalOpen,
    isViewModalOpen,
    isDeleteModalOpen,
    selectedProduct,
    formData,
    openAddModal,
    closeAddModal,
    openEditModal,
    closeEditModal,
    openViewModal,
    closeViewModal,
    openDeleteModal,
    closeDeleteModal,
    updateFormData
  } = useProductModals();

  // Handle form submissions with error handling
  const handleAddProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createProduct(formData);
      closeAddModal();
    } catch (error) {
      // Error is already handled by the hook, could add toast notification here
    }
  };

  const handleEditProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedProduct) return;

    try {
      await updateProduct(selectedProduct.id, formData);
      closeEditModal();
    } catch (error) {
      // Error is already handled by the hook, could add toast notification here
    }
  };

  const handleDeleteProduct = async () => {
    if (!selectedProduct) return;

    try {
      await deleteProduct(selectedProduct.id);
      closeDeleteModal();
    } catch (error) {
      // Error is already handled by the hook, could add toast notification here
    }
  };

  // Filter products based on search term
  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (product.description && product.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  // Show loading state
  if (loading && products.length === 0) {
    return (
      <div className="app">
        <div className="container">
          <div style={{ textAlign: 'center', padding: '2rem' }}>Loading products...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">Product Management</h1>

        {/* Show error message if any */}
        {error && (
          <div style={{ color: 'red', marginBottom: '1rem', padding: '0.5rem', background: '#ffebee', borderRadius: '4px' }}>
            Error: {error}
          </div>
        )}

        <div className="header-controls">
          <div className="search-container">
            <div className="search-input-wrapper">
              <svg className="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none">
                <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2"/>
                <path d="M21 21l-4.35-4.35" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <input
                type="text"
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>
          </div>

          <button onClick={openAddModal} className="add-button" disabled={loading}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M12 5v14M5 12h14" stroke="currentColor" strokeWidth="2"/>
            </svg>
            Add Product
          </button>
        </div>

        <div className="products-grid">
          {filteredProducts.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onView={openViewModal}
              onEdit={openEditModal}
              onDelete={openDeleteModal}
              loading={loading}
            />
          ))}
        </div>

        {/* Modal Components */}
        <AddProductModal
          isOpen={isAddModalOpen}
          onClose={closeAddModal}
          onSubmit={handleAddProduct}
          formData={formData}
          updateFormData={updateFormData}
          loading={loading}
        />

        <EditProductModal
          isOpen={isEditModalOpen}
          onClose={closeEditModal}
          onSubmit={handleEditProduct}
          product={selectedProduct}
          formData={formData}
          updateFormData={updateFormData}
          loading={loading}
        />

        <ViewProductModal
          isOpen={isViewModalOpen}
          onClose={closeViewModal}
          product={selectedProduct}
        />

        <DeleteProductModal
          isOpen={isDeleteModalOpen}
          onClose={closeDeleteModal}
          onConfirm={handleDeleteProduct}
          product={selectedProduct}
          loading={loading}
        />
      </div>
    </div>
  )
}

export default App
