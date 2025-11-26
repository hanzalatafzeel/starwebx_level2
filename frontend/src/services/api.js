import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // Auth
  signup(data) {
    return api.post('/auth/signup', data)
  },
  login(data) {
    return api.post('/auth/login', data)
  },
  getCurrentUser() {
    return api.get('/auth/me')
  },
  updateProfile(data) {
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    return api.put('/auth/profile', data, config)
  },

  // Invoices
  getInvoices() {
    return api.get('/invoices')
  },
  getInvoice(id) {
    return api.get(`/invoices/${id}`)
  },
  createInvoice(data) {
    return api.post('/invoices', data)
  },
  updateInvoice(id, data) {
    return api.put(`/invoices/${id}`, data)
  },
  deleteInvoice(id) {
    return api.delete(`/invoices/${id}`)
  },
  downloadPDF(id) {
    return api.get(`/invoices/${id}/pdf`, {
      responseType: 'blob'
    })
  }
}
