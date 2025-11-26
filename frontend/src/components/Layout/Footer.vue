<template>
        <footer>
        <div class="container">
            <div class="row g-4 mb-4">
                <div class="col-lg-4">
                    <h5><i class="fas fa-file-invoice"></i> InvoiceGen</h5>
                    <p class="mb-3">Professional invoicing made simple for businesses of all sizes.</p>
                    <div>
                        <a href="#" class="social-icon"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="social-icon"><i class="fab fa-facebook"></i></a>
                        <a href="#" class="social-icon"><i class="fab fa-linkedin"></i></a>
                        <a href="#" class="social-icon"><i class="fab fa-instagram"></i></a>
                    </div>
                </div>
                <div class="col-lg-2 col-6">
                    <h5>Product</h5>
                    <ul class="list-unstyled">
                        <li class="mb-2"><a href="#">Features</a></li>
                        <li class="mb-2"><a href="#">Pricing</a></li>
                        <li class="mb-2"><a href="#">Templates</a></li>
                        <li class="mb-2"><a href="#">Integrations</a></li>
                    </ul>
                </div>
                <div class="col-lg-2 col-6">
                    <h5>Company</h5>
                    <ul class="list-unstyled">
                        <li class="mb-2"><a href="#">About</a></li>
                        <li class="mb-2"><a href="#">Blog</a></li>
                        <li class="mb-2"><a href="#">Careers</a></li>
                        <li class="mb-2"><a href="#">Contact</a></li>
                    </ul>
                </div>
                <div class="col-lg-2 col-6">
                    <h5>Resources</h5>
                    <ul class="list-unstyled">
                        <li class="mb-2"><a href="#">Help Center</a></li>
                        <li class="mb-2"><a href="#">Guides</a></li>
                        <li class="mb-2"><a href="#">API Docs</a></li>
                        <li class="mb-2"><a href="#">Status</a></li>
                    </ul>
                </div>
                <div class="col-lg-2 col-6">
                    <h5>Legal</h5>
                    <ul class="list-unstyled">
                        <li class="mb-2"><a href="#">Privacy</a></li>
                        <li class="mb-2"><a href="#">Terms</a></li>
                        <li class="mb-2"><a href="#">Security</a></li>
                        <li class="mb-2"><a href="#">Cookies</a></li>
                    </ul>
                </div>
            </div>
            <div class="text-center pt-4 border-top" style="border-color: var(--border) !important;">
                <p class="mb-0">&copy; 2025 StarwebX InvoiceGen. All rights reserved.</p>
            </div>
        </div>
    </footer>
</template>

<style>

        /* Footer */


        footer {
            background: var(--dark);
            color: #fff;
            padding: 4rem 0 2rem;
        }

        [data-theme="dark"] footer {
            color: var(--text-secondary);
        }

        [data-theme="dark"] footer {
            color: var(--text-secondary);
        }

        footer h5 {
            color: #fff;
            font-weight: 600;
            margin-bottom: 1.5rem;
        }


        footer a {
            color: inherit;
            text-decoration: none;
            transition: color 0.3s;
        }

        footer a:hover {
            color: var(--primary);
        }

        .social-icon {
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-right: 0.5rem;
            transition: all 0.3s;
        }

        .social-icon:hover {
            background: var(--primary);
            color: white;
            transform: translateY(-3px);
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
</style>

<script>
export default {
  name: 'Footer',
}
</script>