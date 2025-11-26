<template>
  <div id="app" :data-theme="theme">
    <router-view />
    <Footer />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import Footer from './components/Layout/Footer.vue'

export default {
  name: 'App',
  components: { Footer },
  setup() {
    const theme = ref('light')

    onMounted(() => {
      const savedTheme = localStorage.getItem('theme') || 'light'
      theme.value = savedTheme
      document.documentElement.setAttribute('data-theme', savedTheme)
    })

    return { theme }
  }
}
</script>

<style>
:root {
  --primary: #10b981;
  --primary-dark: #059669;
  --secondary: #667eea;
  --dark: #0f172a;
  --light: #f8fafc;
  --gray: #64748b;
  --border: #e2e8f0;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --bg-secondary: #f1f5f9;
}

[data-theme="dark"] {
  --light: #020617;
  --dark: #020617;
  --gray: #94a3b8;
  --border: #1f2937;
  --text-primary: #f1f5f9;
  --text-secondary: #cbd5e1;
  --bg-secondary: #1e293b;
}

* {
  scroll-behavior: smooth;
}

body {
  background-color: var(--light);
  color: var(--dark);
  transition: background-color 0.3s ease, color 0.3s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  margin: 0;
  padding: 0;
}
</style>
