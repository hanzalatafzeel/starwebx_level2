// src/services/api.js
import axios from 'axios'

// Use Vite env for production (Vercel). Local dev fallback is localhost:5173 (Vite dev server).
const BASE = import.meta.env.VITE_API_URL || 'http://localhost:5173'

const api = axios.create({
  baseURL: BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Attach Bearer token if present
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Global auth error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // redirect to login - adjust path if your router uses something else
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // Auth (note: /api prefix is required by backend blueprint)
  signup(data) {
    return api.post('/api/auth/signup', data)
  },
  login(data) {
    return api.post('/api/auth/login', data)
  },
  getCurrentUser() {
    return api.get('/api/auth/me')
  },
  updateProfile(data) {
    const config = { headers: { 'Content-Type': 'multipart/form-data' } }
    return api.put('/api/auth/profile', data, config)
  },

  // Invoices
  getInvoices() {
    return api.get('/api/invoices')
  },
  getInvoice(id) {
    return api.get(`/api/invoices/${id}`)
  },
  createInvoice(data) {
    return api.post('/api/invoices', data)
  },
  updateInvoice(id, data) {
    return api.put(`/api/invoices/${id}`, data)
  },
  deleteInvoice(id) {
    return api.delete(`/api/invoices/${id}`)
  },
  // PDF download (ensure backend route matches this)
  downloadPDF(id) {
    return api.get(`/api/invoices/${id}/download`, { responseType: 'blob' })
  }
}
