<template>
  <div>
    <Navbar />
    <div class="detail-container">
      <div class="container py-5">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        
        <div v-else-if="invoice" class="row justify-content-center">
          <div class="col-lg-8">
            <div class="detail-card">
              <div class="d-flex justify-content-between align-items-start mb-4">
                <div>
                  <h2 class="invoice-number">{{ invoice.invoice_number }}</h2>
                  <span :class="['status-badge', `status-${invoice.status}`]">
                    {{ invoice.status }}
                  </span>
                </div>
                <div class="d-flex gap-2">
                  <router-link 
                    :to="`/invoices/${invoice.id}/edit`" 
                    class="btn btn-outline-primary"
                  >
                    Edit
                  </router-link>
                  <button 
                    @click="handleDownloadPDF" 
                    class="btn btn-primary"
                  >
                    <i class="fas fa-download"></i> Download PDF
                  </button>
                </div>
              </div>
              
              <div class="row mb-4">
                <div class="col-md-6">
                  <h6 class="text-muted mb-3">Bill To:</h6>
                  <p class="mb-1"><strong>{{ invoice.client_name }}</strong></p>
                  <p class="mb-1" v-if="invoice.client_email">{{ invoice.client_email }}</p>
                  <p class="mb-0" v-if="invoice.client_address">{{ invoice.client_address }}</p>
                </div>
                <div class="col-md-6 text-md-end">
                  <p class="mb-1"><strong>Invoice Date:</strong> {{ formatDate(invoice.invoice_date) }}</p>
                  <p class="mb-1" v-if="invoice.due_date"><strong>Due Date:</strong> {{ formatDate(invoice.due_date) }}</p>
                </div>
              </div>
              
              <div class="table-responsive mb-4">
                <table class="table">
                  <thead>
                    <tr>
                      <th>Description</th>
                      <th class="text-center">Quantity</th>
                      <th class="text-end">Unit Price</th>
                      <th class="text-end">Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in invoice.items" :key="item.id">
                      <td>{{ item.description }}</td>
                      <td class="text-center">{{ item.quantity }}</td>
                      <td class="text-end">${{ item.unit_price.toFixed(2) }}</td>
                      <td class="text-end">${{ item.total.toFixed(2) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <div class="row justify-content-end">
                <div class="col-md-4">
                  <div class="totals-section">
                    <div class="d-flex justify-content-between mb-2">
                      <strong>Subtotal:</strong>
                      <span>${{ invoice.subtotal.toFixed(2) }}</span>
                    </div>
                    <div class="d-flex justify-content-between mb-2" v-if="invoice.tax_rate > 0">
                      <strong>Tax ({{ invoice.tax_rate }}%):</strong>
                      <span>${{ invoice.tax_amount.toFixed(2) }}</span>
                    </div>
                    <div class="d-flex justify-content-between total-row">
                      <strong>Total:</strong>
                      <strong>${{ invoice.total.toFixed(2) }}</strong>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="invoice.notes" class="notes-section mt-4">
                <h6 class="text-muted mb-2">Notes:</h6>
                <p>{{ invoice.notes }}</p>
              </div>
              
              <div class="mt-4">
                <router-link to="/dashboard" class="btn btn-outline-secondary">
                  <i class="fas fa-arrow-left"></i> Back to Invoices
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useInvoiceStore } from '../../store'
import Navbar from '../Layout/Navbar.vue'

export default {
  name: 'InvoiceDetail',
  components: { Navbar },
  setup() {
    const route = useRoute()
    const invoiceStore = useInvoiceStore()
    
    const invoice = ref(null)
    const loading = ref(true)
    
    onMounted(async () => {
      try {
        invoice.value = await invoiceStore.fetchInvoice(route.params.id)
      } catch (error) {
        console.error('Failed to load invoice:', error)
      } finally {
        loading.value = false
      }
    })
    
    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    const handleDownloadPDF = async () => {
      try {
        await invoiceStore.downloadPDF(invoice.value.id, invoice.value.invoice_number)
      } catch (error) {
        alert('Failed to download PDF')
      }
    }
    
    return {
      invoice,
      loading,
      formatDate,
      handleDownloadPDF
    }
  }
}
</script>

<style scoped>
.detail-container {
  min-height: 100vh;
  padding-top: 100px;
  background-color: var(--light);
}

.detail-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

[data-theme="dark"] .detail-card {
  background: var(--dark);
  border: 1px solid var(--border);
}

.invoice-number {
  color: var(--primary);
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  display: inline-block;
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

.table {
  margin-bottom: 0;
}

.table thead {
  background: #f8fafc;
}

[data-theme="dark"] .table thead {
  background: rgba(255,255,255,0.05);
}

.totals-section {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
}

[data-theme="dark"] .totals-section {
  background: rgba(255,255,255,0.05);
}

.total-row {
  padding-top: 0.75rem;
  border-top: 2px solid var(--primary);
  font-size: 1.25rem;
  color: var(--primary);
}

.notes-section {
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}
</style>
