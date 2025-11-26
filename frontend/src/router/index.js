import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../components/Auth/Login.vue'
import Signup from '../components/Auth/Signup.vue'
import InvoiceList from '../components/Invoice/InvoiceList.vue'
import InvoiceForm from '../components/Invoice/InvoiceForm.vue'
import InvoiceDetail from '../components/Invoice/InvoiceDetail.vue'
import EditProfile from '../components/Profile/EditProfile.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: InvoiceList,
    meta: { requiresAuth: true }
  },
  {
    path: '/invoices/new',
    name: 'NewInvoice',
    component: InvoiceForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/invoices/:id/edit',
    name: 'EditInvoice',
    component: InvoiceForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/invoices/:id',
    name: 'InvoiceDetail',
    component: InvoiceDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile/edit',
    name: 'EditProfile',
    component: EditProfile,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if ((to.name === 'Login' || to.name === 'Signup') && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
