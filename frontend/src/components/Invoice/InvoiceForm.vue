<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="container py-5">
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <div class="form-card">
              <h2 class="mb-4">{{ isEdit ? 'Edit Invoice' : 'New Invoice' }}</h2>

              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>

              <form @submit.prevent="handleSubmit">
                <!-- Client Information -->
                 
                <h5 class="mb-3">Client Information</h5>
                <div class="row g-3 mb-4">
                  <div class="col-md-6">
                    <label class="form-label">Client Name *</label>
                    <input type="text" class="form-control" v-model="form.client_name" required>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label">Client Email</label>
                    <input type="email" class="form-control" v-model="form.client_email">
                  </div>
                  <div class="col-12">
                    <label class="form-label">Client Address</label>
                    <textarea class="form-control" rows="2" v-model="form.client_address"></textarea>
                  </div>
                </div>

                <!-- Invoice Details -->
                <h5 class="mb-3">Invoice Details</h5>
                <div class="row g-3 mb-4">
                  <div class="col-md-4">
                    <label class="form-label">Invoice Date *</label>
                    <input type="date" class="form-control" v-model="form.invoice_date" required>
                  </div>
                  <div class="col-md-4">
                    <label class="form-label">Due Date</label>
                    <input type="date" class="form-control" v-model="form.due_date">
                  </div>
                  <div class="col-md-4">
                    <label class="form-label">Tax Rate (%)</label>
                    <input type="number" class="form-control" v-model.number="form.tax_rate" min="0" step="0.01">
                  </div>
                  <div class="col-md-4">
                    <label class="form-label">Status</label>
                    <select class="form-select" v-model="form.status">
                      <option value="draft">Draft</option>
                      <option value="sent">Sent</option>
                      <option value="paid">Paid</option>
                    </select>
                  </div>
                </div>


                <!-- Items -->
                <h5 class="mb-3">Items</h5>
                <!-- Header Row for Item Fields
                <div class="row g-2 mb-1 fw-semibold text-secondary" style="font-size: 0.95rem;">
                  <div class="col-md-5 px-3">Item</div>
                  <div class="col-md-2 px-3">Qty</div>
                  <div class="col-md-2 px-3">Price</div>
                  <div class="col-md-2 px-3">Total</div>
                  <div class="col-md-1 px-3"></div>
                </div> -->
                <div v-for="(item, index) in form.items" :key="index" class="item-row mb-3">
                  <div class="row g-2">
                    <div class="col-md-5">
                      <input type="text" class="form-control" placeholder="Description" v-model="item.description"
                        required>
                    </div>
                    <div class="col-md-2">
                      <input type="number" class="form-control" placeholder="Qty" v-model.number="item.quantity" min="1"
                        required>
                    </div>
                    <div class="col-md-2">
                      <input type="number" class="form-control" placeholder="Price" v-model.number="item.unit_price"
                        min="0" step="0.01" required>
                    </div>
                    <div class="col-md-2">
                      <input type="text" class="form-control" :value="(item.quantity * item.unit_price).toFixed(2)"
                        readonly>
                    </div>
                    <div class="col-md-1">
                      <button type="button" class="btn btn-outline-danger w-100" @click="removeItem(index)"
                        :disabled="form.items.length === 1">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>

                <button type="button" class="btn btn-outline-success mb-4" @click="addItem">
                  <i class="fas fa-plus"></i> Add Item
                </button>

                <!-- Totals -->
                <div class="totals-section">
                  <div class="row justify-content-end">
                    <div class="col-md-4">
                      <div class="d-flex justify-content-between mb-2">
                        <strong>Subtotal:</strong>
                        <span>${{ subtotal.toFixed(2) }}</span>
                      </div>
                      <div class="d-flex justify-content-between mb-2">
                        <strong>Tax ({{ form.tax_rate }}%):</strong>
                        <span>${{ taxAmount.toFixed(2) }}</span>
                      </div>
                      <div class="d-flex justify-content-between total-row">
                        <strong>Total:</strong>
                        <strong>${{ total.toFixed(2) }}</strong>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Notes -->
                <div class="mb-4">
                  <label class="form-label">Notes</label>
                  <textarea class="form-control" rows="3" v-model="form.notes"
                    placeholder="Payment terms, thank you message, etc."></textarea>
                </div>

                <!-- Actions -->
                <div class="d-flex gap-2">
                  <button type="submit" class="btn btn-success rounded-pill px-4" :disabled="loading">
                    {{ loading ? 'Saving...' : (isEdit ? 'Update Invoice' : 'Create Invoice') }}
                  </button>
                  <router-link to="/dashboard" class="btn btn-outline-secondary rounded-pill px-4">
                    Cancel
                  </router-link>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useInvoiceStore } from '../../store'
import Navbar from '../Layout/Navbar.vue'

export default {
  name: 'InvoiceForm',
  components: { Navbar },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const invoiceStore = useInvoiceStore()

    const isEdit = computed(() => !!route.params.id)
    const loading = ref(false)
    const error = ref('')

    const form = ref({
      client_name: '',
      client_email: '',
      client_address: '',
      invoice_date: new Date().toISOString().split('T')[0],
      due_date: '',
      tax_rate: 0,
      status: 'draft',
      notes: '',
      items: [
        { description: '', quantity: 1, unit_price: 0 }
      ]
    })

    const subtotal = computed(() => {
      return form.value.items.reduce((sum, item) => {
        return sum + (item.quantity * item.unit_price)
      }, 0)
    })

    const taxAmount = computed(() => {
      return subtotal.value * (form.value.tax_rate / 100)
    })

    const total = computed(() => {
      return subtotal.value + taxAmount.value
    })

    const addItem = () => {
      form.value.items.push({
        description: '',
        quantity: 1,
        unit_price: 0
      })
    }

    const removeItem = (index) => {
      if (form.value.items.length > 1) {
        form.value.items.splice(index, 1)
      }
    }

    const handleSubmit = async () => {
      loading.value = true
      error.value = ''

      try {
        const data = {
          ...form.value,
          items: form.value.items.map(item => ({
            description: item.description,
            quantity: parseInt(item.quantity),
            unit_price: parseFloat(item.unit_price)
          }))
        }

        console.log("Submitting invoice data:", data)

        if (isEdit.value) {
          await invoiceStore.updateInvoice(route.params.id, data)
          console.log("Invoice updated:", route.params.id, data)
        } else {
          await invoiceStore.createInvoice(data)
        }

        router.push('/dashboard')
      } catch (err) {
        error.value = err.error || 'Failed to save invoice'
      } finally {
        loading.value = false
      }
    }

    onMounted(async () => {
      if (isEdit.value) {
        try {
          const invoice = await invoiceStore.fetchInvoice(route.params.id)
          form.value = {
            client_name: invoice.client_name,
            client_email: invoice.client_email || '',
            client_address: invoice.client_address || '',
            invoice_date: invoice.invoice_date,
            due_date: invoice.due_date || '',
            tax_rate: invoice.tax_rate,
            status: invoice.status,
            notes: invoice.notes || '',
            items: invoice.items.map(item => ({
              description: item.description,
              quantity: item.quantity,
              unit_price: item.unit_price
            }))
          }
        } catch (err) {
          error.value = 'Failed to load invoice'
        }
      }
    })

    return {
      isEdit,
      loading,
      error,
      form,
      subtotal,
      taxAmount,
      total,
      addItem,
      removeItem,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.form-container {
  min-height: 100vh;
  padding-top: 100px;
  background-color: var(--light);
  color: var(--text-primary);
}

.form-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  color: var(--text-primary);
}

[data-theme="dark"] .form-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  color: var(--text-primary);
}

[data-theme="dark"] .form-card :deep(.form-label),
[data-theme="dark"] .form-card :deep(.form-control),
[data-theme="dark"] .form-card :deep(.form-select),
[data-theme="dark"] .form-card :deep(textarea),
[data-theme="dark"] .form-card :deep(h5) {
  color: var(--text-primary);
}

[data-theme="dark"] .form-card :deep(.form-control),
[data-theme="dark"] .form-card :deep(.form-select),
[data-theme="dark"] .form-card :deep(textarea) {
  background-color: rgba(255, 255, 255, 0.05);
  border-color: var(--border);
}

[data-theme="dark"] .form-card :deep(.form-control::placeholder),
[data-theme="dark"] .form-card :deep(textarea::placeholder) {
  color: var(--text-secondary);
}

.item-row {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
}

[data-theme="dark"] .item-row {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.totals-section {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  color: var(--text-primary);
}

[data-theme="dark"] .totals-section {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.total-row {
  padding-top: 0.75rem;
  border-top: 2px solid var(--primary);
  font-size: 1.25rem;
  color: var(--primary);
}
</style>
