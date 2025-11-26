<template>
  <div>
    <Navbar />
    <div class="auth-container">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-12 col-md-8 col-lg-5">
            <div class="auth-card">
              <h2 class="text-center mb-4">Create Account</h2>
              <p class="text-center text-muted mb-4">Start creating invoices today</p>
              
              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>
              
  <form @submit.prevent="handleSignup">
    <!-- Full Name & Company Name Row -->
    <div class="row g-3 mb-3">
      <div class="col-12 col-md-6">
        <label class="form-label">Full Name</label>
        <input 
          type="text" 
          class="form-control" 
          v-model="fullName"
          placeholder="John Doe"
        >
      </div>
      
      <div class="col-12 col-md-6">
        <label class="form-label">Company Name (Optional)</label>
        <input 
          type="text" 
          class="form-control" 
          v-model="companyName"
          placeholder="Your Company Inc."
        >
      </div>
    </div>

    <!-- Email & Phone Row -->
    <div class="row g-3 mb-3">
      <div class="col-12 col-md-6">
        <label class="form-label">Email</label>
        <input 
          type="email" 
          class="form-control" 
          v-model="email" 
          required
          placeholder="you@example.com"
        >
      </div>
      
      <div class="col-12 col-md-6">
        <label class="form-label">Phone (Optional)</label>
        <input 
          type="tel" 
          class="form-control" 
          v-model="phone"
          placeholder="+1 (555) 123-4567"
        >
      </div>
    </div>

    <!-- Address Row (Full Width) -->
    <div class="mb-3">
      <label class="form-label">Address (Optional)</label>
      <textarea 
        class="form-control" 
        v-model="address"
        rows="2"
        placeholder="123 Business St, City, State ZIP"
      ></textarea>
    </div>

    <!-- Password Row (Full Width) -->
    <div class="mb-3">
      <label class="form-label">Password</label>
      <input 
        type="password" 
        class="form-control" 
        v-model="password" 
        required
        placeholder="••••••••"
        minlength="6"
      >
      <small class="text-muted">At least 6 characters</small>
    </div>

    <!-- Company Logo Row (Full Width) -->
    <div class="mb-3">
      <label class="form-label">Company Logo (Optional)</label>
      <input 
        type="file" 
        class="form-control" 
        @change="handleLogoChange"
        accept="image/png,image/jpg,image/jpeg,image/gif"
      >
      <small class="text-muted">Accepted formats: PNG, JPG, JPEG, GIF</small>
      <div v-if="logoPreview" class="mt-3">
        <p class="text-muted small mb-2">Preview:</p>
        <img :src="logoPreview" alt="Logo Preview" class="logo-preview">
      </div>
    </div>
    
    <!-- Submit Button (Full Width) -->
    <button 
      type="submit" 
      class="btn btn-primary w-100 rounded-pill mb-3"
      :disabled="loading"
    >
      {{ loading ? 'Creating account...' : 'Sign Up' }}
    </button>
  </form>
              <p class="text-center text-muted">
                Already have an account? 
                <router-link to="/login" class="text-primary">Login</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store'
import Navbar from '../Layout/Navbar.vue'

export default {
  name: 'Signup',
  components: { Navbar },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const email = ref('')
    const password = ref('')
    const fullName = ref('')
    const companyName = ref('')
    const address = ref('')
    const phone = ref('')
    const logoFile = ref(null)
    const logoPreview = ref('')
    const loading = ref(false)
    const error = ref('')
    
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
    
    const handleSignup = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const formData = new FormData()
        formData.append('email', email.value)
        formData.append('password', password.value)
        formData.append('full_name', fullName.value)
        formData.append('company_name', companyName.value)
        formData.append('address', address.value)
        formData.append('phone', phone.value)
        if (logoFile.value) {
          formData.append('logo', logoFile.value)
        }

        const response = await fetch('http://localhost:5000/api/auth/signup', {
          method: 'POST',
          body: formData
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || 'Signup failed')
        }

        authStore.user = data.user
        authStore.token = data.access_token
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))

        router.push('/dashboard')
      } catch (err) {
        error.value = err.message || 'Signup failed. Please try again.'
      } finally {
        loading.value = false
      }
    }
    
    return {
      email,
      password,
      fullName,
      companyName,
      address,
      phone,
      logoFile,
      logoPreview,
      loading,
      error,
      handleLogoChange,
      handleSignup
    }
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  /* use CSS variable so theme can override the background for dark mode */
  background: var(--auth-bg-gradient, linear-gradient(135deg, #10b981 0%, #059669 100%));
  padding-top: 80px;
  padding-bottom: 2rem;
}

.auth-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  color: var(--text-primary);
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
}

[data-theme="dark"] .auth-card {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border);
}

.logo-preview {
  max-width: 150px;
  max-height: 150px;
  /* use theme-aware border variable with a sensible fallback */
  border: 1px solid var(--border, #dee2e6);
  border-radius: 8px;
  padding: 8px;
  object-fit: contain;
}

/* Dark-theme override for the auth background gradient */
[data-theme="dark"] .auth-container {
  --auth-bg-gradient: linear-gradient(135deg, #064e3b 0%, #0f766e 100%);
}

/* Responsive padding for different screen sizes */
@media (max-width: 576px) {
  .auth-container {
    padding-top: 60px;
  }
  
  .auth-card {
    padding: 1.5rem;
    margin: 1rem;
  }
  
  .col-12 {
    margin-bottom: 0.5rem;
  }
}

@media (min-width: 577px) and (max-width: 767px) {
  .auth-card {
    padding: 2rem;
  }
}

@media (min-width: 768px) {
  .auth-card {
    padding: 3rem;
  }
  
  .row {
    display: flex;
  }
  
  .col-md-6 {
    flex: 0 0 50%;
  }
}
</style>