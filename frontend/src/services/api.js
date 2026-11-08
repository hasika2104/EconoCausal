// API service client for EconoCausal backend

const API_BASE = import.meta.env.VITE_API_URL || '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Failed to fetch health check');
  return res.json();
}

export async function fetchDashboard(filters = {}) {
  const params = new URLSearchParams();
  if (filters.category && filters.category !== 'All') params.append('category', filters.category);
  if (filters.store && filters.store !== 'All') params.append('store', filters.store);
  if (filters.region && filters.region !== 'All') params.append('region', filters.region);
  if (filters.product && filters.product !== 'All') params.append('product', filters.product);
  if (filters.start_date) params.append('start_date', filters.start_date);
  if (filters.end_date) params.append('end_date', filters.end_date);

  const res = await fetch(`${API_BASE}/dashboard?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch dashboard data');
  return res.json();
}

export async function fetchEDA() {
  const res = await fetch(`${API_BASE}/eda`);
  if (!res.ok) throw new Error('Failed to fetch EDA data');
  return res.json();
}

export async function fetchCausalAnalysis() {
  const res = await fetch(`${API_BASE}/causal-analysis`);
  if (!res.ok) throw new Error('Failed to fetch causal analysis data');
  return res.json();
}

export async function simulatePrice(payload) {
  const res = await fetch(`${API_BASE}/simulate-price`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to run price simulation');
  return res.json();
}

export async function fetchRecommendations(filters = {}) {
  const params = new URLSearchParams();
  if (filters.category && filters.category !== 'All') params.append('category', filters.category);
  if (filters.strategy && filters.strategy !== 'All') params.append('strategy', filters.strategy);
  if (filters.product_id) params.append('product_id', filters.product_id);

  const res = await fetch(`${API_BASE}/recommendations?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch recommendations');
  return res.json();
}

export async function fetchProducts() {
  const res = await fetch(`${API_BASE}/products`);
  if (!res.ok) throw new Error('Failed to fetch products');
  return res.json();
}

export async function fetchDatasetPreview(params = {}) {
  const searchParams = new URLSearchParams();
  if (params.dataset_type) searchParams.append('dataset_type', params.dataset_type);
  if (params.page) searchParams.append('page', params.page);
  if (params.page_size) searchParams.append('page_size', params.page_size);
  if (params.sort_by) searchParams.append('sort_by', params.sort_by);
  if (params.sort_dir) searchParams.append('sort_dir', params.sort_dir);
  if (params.search) searchParams.append('search', params.search);

  const res = await fetch(`${API_BASE}/dataset/preview?${searchParams.toString()}`);
  if (!res.ok) throw new Error('Failed to preview dataset');
  return res.json();
}

export async function uploadDataset(file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/dataset/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Upload failed');
  }
  return res.json();
}
