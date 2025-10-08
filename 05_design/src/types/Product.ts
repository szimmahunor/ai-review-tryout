export interface Product {
  id: string;
  name: string;
  description: string | null;
  price: number;
  stock: number;
  createdAt: string;
  updatedAt: string;
}

export interface ProductFormData {
  name: string;
  description: string;
  price: string;
  stock: string;
}

export interface CreateProductRequest {
  name: string;
  description: string | null;
  price: number;
  stock: number;
}

export interface UpdateProductRequest {
  name: string;
  description: string | null;
  price: number;
  stock: number;
}
