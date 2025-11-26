<template>
  <nav class="navbar navbar-expand-lg fixed-top">
    <div class="container">
      <router-link to="/" class="navbar-brand logo-text">
        <i class="fas fa-file-invoice"></i> InvoiceGen
      </router-link>

      <!-- Toggler for small screens -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <div class="ms-auto d-flex align-items-center gap-3">
          <div class="theme-toggle" @click="toggleTheme" role="button" tabindex="0"></div>

          <template v-if="isAuthenticated">
            <router-link to="/dashboard" class="btn btn-sm btn-outline-primary rounded-pill px-3">
              Dashboard
            </router-link>
            <router-link to="/profile/edit" class="btn btn-sm btn-outline-secondary rounded-pill px-3">
              Profile
            </router-link>
            <button @click="handleLogout" class="btn btn-sm btn-outline-danger rounded-pill px-3">
              Logout
            </button>
          </template>
          <template v-else>
            <router-link to="/login" class="btn btn-sm btn-outline-primary rounded-pill px-3">
              Login
            </router-link>
            <router-link to="/signup" class="btn btn-primary rounded-pill px-4">
              Get Started
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store'

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    const toggleTheme = () => {
      const html = document.documentElement
      const currentTheme = html.getAttribute('data-theme')
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark'
      html.setAttribute('data-theme', newTheme)
      localStorage.setItem('theme', newTheme)
    }
    
    const handleLogout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    return {
      isAuthenticated,
      toggleTheme,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar {
  backdrop-filter: blur(10px);
  background-color: var(--light) !important;
  transition: all 0.3s ease;
  border-bottom: 1px solid var(--border);
  color: var(--text-primary);
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
}

.theme-toggle {
  width: 50px;
  height: 26px;
  background: var(--border);
  border-radius: 13px;
  cursor: pointer;
  position: relative;
  transition: background 0.3s;
}

.theme-toggle::before {
  content: '🌙';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 22px;
  height: 22px;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

[data-theme="dark"] .theme-toggle {
  background: var(--primary);
}

[data-theme="dark"] .theme-toggle::before {
  content: '☀️';
  transform: translateX(24px);
}
</style>
