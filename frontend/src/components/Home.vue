<template>

  <Navbar/>

  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container position-relative">
        <div class="row align-items-center">
          <div class="col-lg-6 mb-4 mb-lg-0">
            <span class="badge-success">✨ Create Your First Invoice</span>
            <h1 class="display-3 fw-bold mb-4 mt-3">Create Professional Invoices in Seconds</h1>
            <p class="lead mb-4">Generate, customize, and send professional invoices instantly. Built for freelancers, small businesses, and entrepreneurs.</p>
            <button class="btn btn-hero mb-3" @click="handleGetStarted">Start Creating Free</button>
            <p class="small opacity-75">✓ No credit card required &nbsp; ✓ Free forever plan</p>
          </div>
          <div class="col-lg-6">
            <img src="/hero.png" alt="Invoice Dashboard" class="hero-image fade-in">
          </div>
        </div>
      </div>
    </section>

    <!-- Features Grid -->
    <section class="py-5 bg-light">
      <div class="container">
        <div class="row g-4 py-5">
          <div class="col-md-4" v-for="feature in features" :key="feature.title">
            <div class="feature-card fade-in">
              <div class="feature-icon">
                <i :class="feature.icon"></i>
              </div>
              <h3 class="h5 fw-bold mb-3">{{ feature.title }}</h3>
              <p class="mb-0 text-muted">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Ready to Get Started -->
    <section class="content-section">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="display-5 fw-bold mb-3">Ready to get paid, fast?</h2>
          <p class="lead text-muted">Join thousands of professionals who trust InvoiceGen</p>
        </div>
        <div class="row align-items-center">
          <div class="col-lg-6">
            <div class="row text-muted">
              <div class="col-6">
                <ul class="checklist">
                  <li v-for="item in checklistLeft" :key="item">{{ item }}</li>
                </ul>
              </div>
              <div class="col-6">
                <ul class="checklist">
                  <li v-for="item in checklistRight" :key="item">{{ item }}</li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-lg-6 fade-in">
            <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=400&fit=crop" alt="Features" class="content-image">
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="content-section bg-light">
      <div class="container">
        <div class="row align-items-center mb-5">
          <div class="col-lg-6 mb-4 mb-lg-0 fade-in">
            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop" alt="Save Time" class="content-image">
          </div>
          <div class="col-lg-6">
            <span class="section-badge">Save Time</span>
            <h2 class="display-6 fw-bold mb-4">Create invoices in 3 simple steps</h2>
            <div class="mb-4" v-for="step in steps" :key="step.number">
              <h4 class="h5 fw-bold mb-2">{{ step.number }}. {{ step.title }}</h4>
              <p class="text-muted">{{ step.description }}</p>
            </div>
          </div>
        </div>

        <div class="row align-items-center">
          <div class="col-lg-6 order-lg-2 mb-4 mb-lg-0 fade-in">
            <img src="/accept_payment.png" alt="Accept Payments" class="content-image">
          </div>
          <div class="col-lg-6 order-lg-1">
            <span class="section-badge">Get Paid</span>
            <h2 class="display-6 fw-bold mb-4">Accept payments seamlessly</h2>
            <p class="mb-4 text-muted">Integrate with popular payment gateways and get paid faster. Track payment status and send automatic reminders.</p>
            <ul class="checklist text-muted">
              <li v-for="item in paymentFeatures" :key="item">{{ item }}</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="py-5">
      <div class="container">
        <div class="row row-cols-2 row-cols-md-4 g-4 text-center">
          <div class="col" v-for="stat in stats" :key="stat.label">
            <div class="stats-card fade-in h-100 d-flex flex-column justify-content-center">
              <div class="stats-number">{{ stat.value }}</div>
              <div class="text-muted">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing -->
    <section class="content-section bg-light">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="display-5 fw-bold mb-3">Simple, Transparent Pricing</h2>
          <p class="lead text-muted">Choose the plan that works best for you</p>
        </div>
        <div class="row g-4">
          <div class="col-lg-4" v-for="plan in pricingPlans" :key="plan.name">
            <div class="pricing-card fade-in" :class="{ featured: plan.featured }">
              <span v-if="plan.badge" class="badge bg-primary mb-3">{{ plan.badge }}</span>
              <h3 class="h4 fw-bold mb-3">{{ plan.name }}</h3>
              <div class="price mb-4">
                ${{ plan.price }}<span class="h6 text-muted">/mo</span>
              </div>
              <ul class="list-unstyled mb-4 text-muted">
                <li class="mb-3" v-for="feature in plan.features" :key="feature">
                  <i class="fas fa-check text-success me-2"></i> {{ feature }}
                </li>
              </ul>
              <button 
                :class="plan.buttonClass" 
                class="w-100 rounded-pill fw-semibold"
                @click="handlePlanSelect(plan.name)"
              >
                {{ plan.buttonText }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <h2 class="display-5 fw-bold mb-4">Ready to streamline your invoicing?</h2>
        <p class="lead mb-4">Join thousands of businesses using InvoiceGen</p>
        <button class="btn btn-hero" @click="handleGetStarted">Start Creating Invoices Free</button>
      </div>
    </section>
  </div>


</template>

<script>

import Navbar from './Layout/Navbar.vue';

export default {
  name: 'Home',
  components: {
    Navbar
  },
  data() {
    return {
      features: [
        {
          icon: 'fas fa-bolt',
          title: 'Lightning Fast',
          description: 'Create invoices in under 60 seconds. No complicated forms or endless steps.'
        },
        {
          icon: 'fas fa-file-pdf',
          title: 'PDF Export',
          description: 'Download professional PDF invoices ready to send to clients instantly.'
        },
        {
          icon: 'fas fa-users',
          title: 'Client Management',
          description: 'Save and manage client details for faster invoice creation next time.'
        }
      ],
      checklistLeft: [
        'Unlimited invoices',
        'Custom branding',
        'Multiple currencies',
        'Tax calculations',
        'Client portal access'
      ],
      checklistRight: [
        'Payment tracking',
        'Recurring invoices',
        'Mobile app access',
        'Email notifications',
        'Report generation'
      ],
      steps: [
        {
          number: 1,
          title: 'Enter Details',
          description: 'Add your business and client information'
        },
        {
          number: 2,
          title: 'Add Items',
          description: 'List your products or services with pricing'
        },
        {
          number: 3,
          title: 'Download & Send',
          description: 'Export as PDF and send to your client'
        }
      ],
      paymentFeatures: [
        'Multiple payment methods',
        'Automatic payment reminders',
        'Real-time payment tracking',
        'Secure transactions'
      ],
      stats: [
        { value: '50K+', label: 'Active Users' },
        { value: '2M+', label: 'Invoices Created' },
        { value: '180+', label: 'Countries' },
        { value: '4.9★', label: 'User Rating' }
      ],
      pricingPlans: [
        {
          name: 'Free',
          price: 0,
          features: [
            '10 invoices/month',
            'Basic templates',
            'PDF export',
            'Email support'
          ],
          buttonText: 'Get Started',
          buttonClass: 'btn btn-outline-success'
        },
        {
          name: 'Pro',
          price: 12,
          badge: 'Most Popular',
          featured: true,
          features: [
            'Unlimited invoices',
            'Premium templates',
            'Custom branding',
            'Priority support',
            'Payment integration'
          ],
          buttonText: 'Start Free Trial',
          buttonClass: 'btn btn-success'
        },
        {
          name: 'Business',
          price: 29,
          features: [
            'Everything in Pro',
            'Team collaboration',
            'Advanced analytics',
            'API access',
            'Dedicated support'
          ],
          buttonText: 'Contact Sales',
          buttonClass: 'btn btn-outline-success'
        }
      ]
    };
  },
  mounted() {
    this.setupIntersectionObserver();
  },
  methods: {
    setupIntersectionObserver() {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      }, { threshold: 0.1 });

      document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
      });
    },
    handleGetStarted() {
      // Navigate to invoice creation page or show modal
      this.$router.push('/create-invoice');
    },
    handlePlanSelect(planName) {
      console.log(`Selected plan: ${planName}`);
      // Handle plan selection logic
    }
  }
};
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  padding: 120px 0 80px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  width: 600px;
  height: 600px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  top: -300px;
  right: -300px;
  animation: float 8s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(20px); }
}

.badge-success {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-weight: 600;
}

.btn-hero {
  background: white;
  color: #10b981;
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-weight: 700;
  border: none;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.btn-hero:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
}

.hero-image {
  max-width: 100%;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* Feature Cards */
.feature-card {
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  background: white;
  transition: all 0.3s ease;
  height: 100%;
  color: var(--text-primary);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] .feature-card {
  background: var(--bg-secondary);
  border-color: var(--border);
  color: var(--text-primary);
}

.feature-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  margin-bottom: 1rem;
}

/* Content Section */
.content-section {
  padding: 100px 0;
  color: var(--text-primary);
}

[data-theme="dark"] .content-section {
  background-color: var(--light);
}

.section-badge {
  background: #e0f2fe;
  color: #0369a1;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  display: inline-block;
  margin-bottom: 1rem;
}

.content-image {
  max-width: 100%;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

/* Checklist */
.checklist {
  list-style: none;
  padding: 0;
  color: var(--text-primary);
}

.checklist li {
  padding: 0.75rem 0;
  display: flex;
  align-items: center;
  color: var(--text-primary);
}

.checklist li::before {
  content: '✓';
  color: #10b981;
  font-weight: bold;
  margin-right: 1rem;
  font-size: 1.25rem;
}

/* Stats Section */
.stats-card {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  color: var(--text-primary);
}

[data-theme="dark"] .stats-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
}

.stats-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #10b981;
  margin-bottom: 0.5rem;
}

/* Pricing Table */
.pricing-card {
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 2.5rem;
  height: 100%;
  transition: all 0.3s ease;
  background: white;
  color: var(--text-primary);
}

.pricing-card:hover {
  border-color: #10b981;
  box-shadow: 0 20px 40px rgba(16, 185, 129, 0.1);
}

.pricing-card.featured {
  border-color: #10b981;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.05), rgba(5, 150, 105, 0.05));
}

[data-theme="dark"] .pricing-card {
  background: var(--bg-secondary);
  border-color: var(--border);
  color: var(--text-primary);
}

[data-theme="dark"] .pricing-card.featured {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
  border-color: #10b981;
}

.price {
  font-size: 3rem;
  font-weight: 700;
  color: #10b981;
}

/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  padding: 80px 0;
  color: white;
  text-align: center;
}

/* Animations */
.fade-in {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Responsive */
@media (max-width: 768px) {
  .hero-section {
    padding: 80px 0 60px;
  }
  
  .hero-section h1 {
    font-size: 2rem;
  }
  
  .content-section {
    padding: 60px 0;
  }
}
</style>
<style>
/* Fix Bootstrap .bg-light and .text-muted for dark mode */
[data-theme="dark"] .bg-light {
  background-color: var(--bg-secondary) !important;
}
[data-theme="dark"] .text-muted {
  color: var(--text-secondary) !important;
}

/* Ensure all .content-section and .feature-card text is visible in dark mode */
[data-theme="dark"] .content-section,
[data-theme="dark"] .feature-card,
[data-theme="dark"] .stats-card,
[data-theme="dark"] .pricing-card {
  color: var(--text-primary) !important;
}

/* Checklist and section badge contrast in dark mode */
[data-theme="dark"] .checklist li {
  color: var(--text-primary);
}
[data-theme="dark"] .section-badge {
  background: #334155;
  color: #38bdf8;
}
</style>