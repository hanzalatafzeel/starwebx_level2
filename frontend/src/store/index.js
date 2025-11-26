// stores/index.js
import { defineStore } from 'pinia'
import api from '../services/api'   // your existing api wrapper (used for auth/invoice endpoints)
import axios from 'axios'

/**
 * Auth store
 * - Holds user + token
 * - Provides login/signup/logout
 * - Provides uploadLogo(file, onProgress) to upload company logo and update user
 */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    // ----- auth actions -----
    async login(credentials) {
      try {
        const response = await api.login(credentials)
        this.token = response.data.access_token
        this.user = response.data.user

        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))

        return response.data
      } catch (error) {
        throw error.response?.data || error
      }
    },

    async signup(userData) {
      try {
        const response = await api.signup(userData)
        this.token = response.data.access_token
        this.user = response.data.user

        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))

        return response.data
      } catch (error) {
        throw error.response?.data || error
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    // ----- file upload for company logo -----
    /**
     * Upload a logo file to backend.
     * @param {File} file - image file from input
     * @param {function} onProgress - optional callback(progressPercent) for upload progress
     * @returns server JSON response (expects { logo_path: "uploads/logos/..." })
     */
    async uploadLogo(file, onProgress = null) {
      if (!file) throw new Error('No file supplied for upload')

      const form = new FormData()
      form.append('logo', file)

      const token = this.token // token from store

      try {
        // Use axios directly for multipart upload so we can support onUploadProgress.
        const response = await axios.post('/api/upload/logo', form, {
          headers: {
            'Content-Type': 'multipart/form-data',
            ...(token ? { Authorization: `Bearer ${token}` } : {})
          },
          onUploadProgress: (ev) => {
            if (ev.lengthComputable && typeof onProgress === 'function') {
              const percent = Math.round((ev.loaded * 100) / ev.total)
              onProgress(percent)
            }
          }
        })

        const data = response.data || {}
        if (data.logo_path) {
          // Update store + localStorage
          if (!this.user) this.user = {}
          this.user.company_logo = data.logo_path
          localStorage.setItem('user', JSON.stringify(this.user))
        }

        return data
      } catch (err) {
        // normalize error and rethrow
        throw err.response?.data || err
      }
    },

    /**
     * Optional: request backend to remove logo (if you implement an endpoint).
     * If you don't have a backend delete endpoint, you can just clear locally.
     */
    async removeLogo() {
      try {
        // Example: if you have a delete endpoint:
        // await axios.delete('/api/upload/logo', { headers: { Authorization: `Bearer ${this.token}` } })
        if (this.user) {
          this.user.company_logo = null
          localStorage.setItem('user', JSON.stringify(this.user))
        }
        return { ok: true }
      } catch (err) {
        throw err.response?.data || err
      }
    }
  }
})

/**
 * Invoice store
 * - Fetch invoices, fetch single invoice, create/update/delete, download PDF
 * - Keeps mostly the same logic you provided
 */
export const useInvoiceStore = defineStore('invoice', {
  state: () => ({
    invoices: [],
    currentInvoice: null,
    loading: false
  }),

  actions: {
    async fetchInvoices() {
      this.loading = true
      try {
        const response = await api.getInvoices()
        this.invoices = response.data.invoices
      } catch (error) {
        throw error.response?.data || error
      } finally {
        this.loading = false
      }
    },

    async fetchInvoice(id) {
      this.loading = true
      try {
        const response = await api.getInvoice(id)
        this.currentInvoice = response.data.invoice
        return response.data.invoice
      } catch (error) {
        throw error.response?.data || error
      } finally {
        this.loading = false
      }
    },

    async createInvoice(data) {
      try {
        const response = await api.createInvoice(data)
        this.invoices.unshift(response.data.invoice)
        return response.data.invoice
      } catch (error) {
        throw error.response?.data || error
      }
    },

    async updateInvoice(id, data) {
      try {
        const response = await api.updateInvoice(id, data)
        const index = this.invoices.findIndex(inv => inv.id === id)
        if (index !== -1) {
          this.invoices[index] = response.data.invoice
        }
        return response.data.invoice
      } catch (error) {
        throw error.response?.data || error
      }
    },

    async deleteInvoice(id) {
      try {
        await api.deleteInvoice(id)
        this.invoices = this.invoices.filter(inv => inv.id !== id)
      } catch (error) {
        throw error.response?.data || error
      }
    },

    // download PDF using your existing api wrapper - expect responseType handled in api.downloadPDF
    async downloadPDF(id, invoiceNumber) {
      try {
        const response = await api.downloadPDF(id) // ensure api.downloadPDF sets responseType: 'blob'
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `${invoiceNumber || 'invoice'}.pdf`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
      } catch (error) {
        throw error.response?.data || error
      }
    }
  }
})
