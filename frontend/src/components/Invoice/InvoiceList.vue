<template>
  <div>
    <Navbar />
    <div class="dashboard-container">
      <div class="container py-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <div>
            <h2 class="mb-1">My Invoices</h2>
            <p class="text-muted">Manage and track all your invoices</p>
          </div>
          <router-link to="/invoices/new" class="btn btn-primary rounded-pill px-4">
            <i class="fas fa-plus"></i> New Invoice
          </router-link>
        </div>
        
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        
        <div v-else-if="invoices.length === 0" class="text-center py-5">
          <i class="fas fa-file-invoice fa-4x text-muted mb-3"></i>
          <h4>No invoices yet</h4>
          <p class="text-muted">Create your first invoice to get started</p>
          <router-link to="/invoices/new" class="btn btn-primary rounded-pill px-4 mt-3">
            Create Invoice
          </router-link>
        </div>
        
        <div v-else class="row g-4">
          <div v-for="invoice in invoices" :key="invoice.id" class="col-md-6 col-lg-4">
            <div class="invoice-card">
              <div class="invoice-header">
                <h5 class="invoice-number">{{ invoice.invoice_number }}</h5>
                <span :class="['status-badge', `status-${invoice.status}`]">
                  {{ invoice.status }}
                </span>
              </div>
              
              <div class="invoice-body">
                <p class="client-name">
                  <i class="fas fa-user"></i> {{ invoice.client_name }}
                </p>
                <p class="invoice-date text-muted">
                  <i class="fas fa-calendar"></i> {{ formatDate(invoice.invoice_date) }}
                </p>
                <p class="invoice-total">
                  <strong>${{ invoice.total.toFixed(2) }}</strong>
                </p>
              </div>
              
              <div class="invoice-actions">
                <router-link 
                  :to="`/invoices/${invoice.id}`" 
                  class="btn btn-sm btn-outline-primary"
                >
                  View
                </router-link>
                <router-link 
                  :to="`/invoices/${invoice.id}/edit`" 
                  class="btn btn-sm btn-outline-secondary"
                >
                  Edit
                </router-link>
                <button 
                  @click="handleDownloadPDF(invoice)" 
                  class="btn btn-sm btn-outline-success"
                >
                  PDF
                </button>
                <button 
                  @click="handleDelete(invoice)" 
                  class="btn btn-sm btn-outline-danger"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useInvoiceStore } from '../../store'
import Navbar from '../Layout/Navbar.vue'

export default {
  name: 'InvoiceList',
  components: { Navbar },
  setup() {
    const invoiceStore = useInvoiceStore()
    
    const invoices = computed(() => invoiceStore.invoices)
    const loading = computed(() => invoiceStore.loading)
    
    onMounted(() => {
      invoiceStore.fetchInvoices()
    })
    
    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
    
    const handleDownloadPDF = async (invoice) => {
      try {
        await invoiceStore.downloadPDF(invoice.id, invoice.invoice_number)
      } catch (error) {
        alert('Failed to download PDF')
      }
    }
    
    const handleDelete = async (invoice) => {
      if (confirm(`Delete invoice ${invoice.invoice_number}?`)) {
        try {
          await invoiceStore.deleteInvoice(invoice.id)
        } catch (error) {
          alert('Failed to delete invoice')
        }
      }
    }
    
    return {
      invoices,
      loading,
      formatDate,
      handleDownloadPDF,
      handleDelete
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  padding-top: 100px;
  background-color: var(--light);
  color: var(--text-primary);
}

.invoice-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  color: var(--text-primary);
}

.invoice-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

[data-theme="dark"] .invoice-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  color: var(--text-primary);
}

.invoice-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.invoice-number {
  margin: 0;
  color: var(--primary);
  font-weight: 600;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-draft {
  background: #f3f4f6;
  color: #6b7280;
}

.status-sent {
  background: #dbeafe;
  color: #1e40af;
}

.status-paid {
  background: #d1fae5;
  color: #065f46;
}

.invoice-body {
  margin-bottom: 1rem;
}

.client-name {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.invoice-date {
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.invoice-total {
  font-size: 1.5rem;
  color: var(--primary);
  margin: 0;
}

.invoice-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
</style>
