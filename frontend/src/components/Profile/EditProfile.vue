<template>
  <div>
    <Navbar />
    <div class="profile-container">
      <div class="container py-5">
        <div class="row justify-content-center">
          <div class="col-lg-6">
            <div class="profile-card">
              <h2 class="mb-4">Edit Profile</h2>

              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>

              <div v-if="success" class="alert alert-success" role="alert">
                {{ success }}
              </div>

              <form @submit.prevent="handleSubmit">
                <!-- Full Name -->
                <div class="mb-3">
                  <label class="form-label">Full Name</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="form.full_name"
                    placeholder="John Doe"
                  >
                </div>

                <!-- Company Name -->
                <div class="mb-3">
                  <label class="form-label">Company Name (Optional)</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="form.company_name"
                    placeholder="Your Company Inc."
                  >
                </div>

                <!-- Email -->
                <div class="mb-3">
                  <label class="form-label">Email</label>
                  <input
                    type="email"
                    class="form-control"
                    v-model="form.email"
                    placeholder="you@example.com"
                  >
                </div>

                <!-- Address -->
                <div class="mb-3">
                  <label class="form-label">Address (Optional)</label>
                  <textarea
                    class="form-control"
                    v-model="form.address"
                    rows="2"
                    placeholder="123 Business St, City, State ZIP"
                  ></textarea>
                </div>

                <!-- Phone -->
                <div class="mb-3">
                  <label class="form-label">Phone (Optional)</label>
                  <input
                    type="tel"
                    class="form-control"
                    v-model="form.phone"
                    placeholder="+1 (555) 123-4567"
                  >
                </div>

                <!-- Password -->
                <div class="mb-4">
                  <label class="form-label">New Password (Leave blank to keep current)</label>
                  <input
                    type="password"
                    class="form-control"
                    v-model="form.password"
                    placeholder="••••••••"
                    minlength="6"
                  >
                  <small class="text-muted">At least 6 characters if changing password</small>
                </div>

                <!-- Company Logo -->
                <div class="mb-4">
                  <label class="form-label">Company Logo (Optional)</label>
                  <div class="logo-upload-section">
                    <div v-if="currentLogoUrl" class="mb-3">
                      <p class="text-muted small">Current Logo:</p>
                      <img :src="currentLogoUrl" alt="Current Logo" class="current-logo">
                    </div>
                    <input
                      type="file"
                      class="form-control"
                      @change="handleLogoChange"
                      accept="image/*"
                    >
                    <small class="text-muted">Accepted formats: PNG, JPG, JPEG, GIF (Max 5MB)</small>
                    <div v-if="logoPreview" class="mt-3">
                      <p class="text-muted small">Preview:</p>
                      <img :src="logoPreview" alt="Logo Preview" class="logo-preview">
                    </div>
                  </div>
                </div>

                <!-- Actions -->
                <div class="d-flex gap-2">
                  <button
                    type="submit"
                    class="btn btn-primary rounded-pill px-4"
                    :disabled="loading"
                  >
                    {{ loading ? 'Saving...' : 'Save Changes' }}
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store'
import api from '../../services/api'
import Navbar from '../Layout/Navbar.vue'

export default {
  name: 'EditProfile',
  components: { Navbar },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const form = ref({
      full_name: '',
      company_name: '',
      email: '',
      address: '',
      phone: '',
      password: ''
    })

    const logoFile = ref(null)
    const logoPreview = ref('')
    const currentLogoUrl = ref('')
    const loading = ref(false)
    const error = ref('')
    const success = ref('')

    const handleLogoChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        logoFile.value = file
        const reader = new FileReader()
        reader.onload = (e) => {
          logoPreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }

    const handleSubmit = async () => {
      loading.value = true
      error.value = ''
      success.value = ''

      try {
        const formData = new FormData()
        formData.append('full_name', form.value.full_name)
        formData.append('company_name', form.value.company_name)
        formData.append('email', form.value.email)
        formData.append('address', form.value.address)
        formData.append('phone', form.value.phone)
        if (form.value.password) {
          formData.append('password', form.value.password)
        }
        if (logoFile.value) {
          formData.append('logo', logoFile.value)
        }

        const response = await api.updateProfile(formData)
        success.value = 'Profile updated successfully!'
        authStore.user = response.data.user
        localStorage.setItem('user', JSON.stringify(response.data.user))

        setTimeout(() => {
          router.push('/dashboard')
        }, 2000)
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to update profile'
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      if (authStore.user) {
        form.value.full_name = authStore.user.full_name || ''
        form.value.company_name = authStore.user.company_name || ''
        form.value.email = authStore.user.email || ''
        form.value.address = authStore.user.address || ''
        form.value.phone = authStore.user.phone || ''

        if (authStore.user.company_logo) {
          currentLogoUrl.value = `http://localhost:5000/${authStore.user.company_logo}`
        }
      }
    })

    return {
      form,
      loading,
      error,
      success,
      logoPreview,
      currentLogoUrl,
      handleLogoChange,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  padding-top: 100px;
  background-color: var(--light);
  color: var(--text-primary);
}

.profile-card {
  background: white;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  color: var(--text-primary);
}

[data-theme="dark"] .profile-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  color: var(--text-primary);
}

[data-theme="dark"] .profile-card :deep(.form-label),
[data-theme="dark"] .profile-card :deep(.form-control),
[data-theme="dark"] .profile-card :deep(textarea),
[data-theme="dark"] .profile-card :deep(small) {
  color: var(--text-primary);
}

[data-theme="dark"] .profile-card :deep(.form-control),
[data-theme="dark"] .profile-card :deep(textarea) {
  background-color: rgba(255, 255, 255, 0.05);
  border-color: var(--border);
}

[data-theme="dark"] .profile-card :deep(.form-control::placeholder),
[data-theme="dark"] .profile-card :deep(textarea::placeholder) {
  color: var(--text-secondary);
}

.logo-upload-section {
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 2px dashed #e2e8f0;
}

[data-theme="dark"] .logo-upload-section {
  background: rgba(255, 255, 255, 0.03);
  border-color: var(--border);
}

.current-logo,
.logo-preview {
  max-width: 150px;
  max-height: 150px;
  border-radius: 8px;
  object-fit: contain;
  border: 1px solid var(--border);
}
</style>
