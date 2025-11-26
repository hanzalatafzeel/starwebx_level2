<template>
  <div>
    <Navbar />
    <div class="auth-container">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-12 col-md-8 col-lg-5">
            <div class="auth-card">
              <h2 class="text-center mb-4">Welcome Back</h2>
              <p class="text-center text-muted mb-4">Login to your account</p>
              
              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>
              
              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label class="form-label">Email</label>
                  <input 
                    type="email" 
                    class="form-control" 
                    v-model="email" 
                    required
                    placeholder="you@example.com"
                  >
                </div>
                
                <div class="mb-4">
                  <label class="form-label">Password</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    v-model="password" 
                    required
                    placeholder="••••••••"
                  >
                </div>
                
                <button 
                  type="submit" 
                  class="btn btn-primary w-100 rounded-pill mb-3"
                  :disabled="loading"
                >
                  {{ loading ? 'Logging in...' : 'Login' }}
                </button>
              </form>
              
              <p class="text-center text-muted">
                Don't have an account? 
                <router-link to="/signup" class="text-primary">Sign up</router-link>
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
  name: 'Login',
  components: { Navbar },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const email = ref('')
    const password = ref('')
    const loading = ref(false)
    const error = ref('')
    
    const handleLogin = async () => {
      loading.value = true
      error.value = ''
      
      try {
        await authStore.login({
          email: email.value,
          password: password.value
        })
        router.push('/dashboard')
      } catch (err) {
        error.value = err.error || 'Login failed. Please try again.'
        
      } finally {
        loading.value = false
      }
    }
    
    return {
      email,
      password,
      loading,
      error,
      handleLogin
    }
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  padding-top: 80px;
}

.auth-card {
  background: white;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  color: var(--text-primary);
}

[data-theme="dark"] .auth-card {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border);
}
</style>
