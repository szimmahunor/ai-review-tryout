import axios from 'axios';
import type { Product, CreateProductRequest, UpdateProductRequest } from '../types/Product';

const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export class ProductService {
  static async getAllProducts(): Promise<Product[]> {
    try {
      const response = await apiClient.get<Product[]>('/products');
      return response.data;
    } catch (error) {
      console.error('Error fetching products:', error);
      throw new Error('Failed to fetch products');
    }
  }

  static async createProduct(productData: CreateProductRequest): Promise<Product> {
    try {
      const response = await apiClient.post<Product>('/products', productData);
      return response.data;
    } catch (error) {
      console.error('Error creating product:', error);
      throw new Error('Failed to create product');
    }
  }

  static async updateProduct(id: string, productData: UpdateProductRequest): Promise<Product> {
    try {
      const response = await apiClient.put<Product>(`/products/${id}`, productData);
      return response.data;
    } catch (error) {
      console.error('Error updating product:', error);
      throw new Error('Failed to update product');
    }
  }

  static async deleteProduct(id: string): Promise<void> {
    try {
      await apiClient.delete(`/products/${id}`);
    } catch (error) {
      console.error('Error deleting product:', error);
      throw new Error('Failed to delete product');
    }
  }

  static async getProductById(id: string): Promise<Product> {
    try {
      const response = await apiClient.get<Product>(`/products/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching product:', error);
      throw new Error('Failed to fetch product');
    }
  }
}
