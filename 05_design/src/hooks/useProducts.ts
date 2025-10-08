import { useState, useEffect } from 'react';
import type { Product, ProductFormData, CreateProductRequest, UpdateProductRequest } from '../types/Product';
import { ProductService } from '../services/ProductService';

export const useProducts = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await ProductService.getAllProducts();
      setProducts(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const createProduct = async (formData: ProductFormData) => {
    try {
      setLoading(true);
      setError(null);

      const productData: CreateProductRequest = {
        name: formData.name,
        description: formData.description || null,
        price: parseFloat(formData.price),
        stock: parseInt(formData.stock)
      };

      await ProductService.createProduct(productData);
      await fetchProducts(); // Refresh the list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create product');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateProduct = async (id: string, formData: ProductFormData) => {
    try {
      setLoading(true);
      setError(null);

      const productData: UpdateProductRequest = {
        name: formData.name,
        description: formData.description || null,
        price: parseFloat(formData.price),
        stock: parseInt(formData.stock)
      };

      await ProductService.updateProduct(id, productData);
      await fetchProducts(); // Refresh the list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update product');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteProduct = async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await ProductService.deleteProduct(id);
      await fetchProducts(); // Refresh the list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete product');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return {
    products,
    loading,
    error,
    fetchProducts,
    createProduct,
    updateProduct,
    deleteProduct
  };
};
