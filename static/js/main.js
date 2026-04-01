// Mobile Menu
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navMenu = document.querySelector('.nav-menu');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        mobileMenuBtn.classList.toggle('active');
    });
}

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (!navMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
        navMenu.classList.remove('active');
        mobileMenuBtn.classList.remove('active');
    }
});

// Slider/Carousel
class Slider {
    constructor(container) {
        this.container = container;
        this.slides = container.querySelectorAll('.slider-slide');
        this.prevBtn = container.querySelector('.slider-prev');
        this.nextBtn = container.querySelector('.slider-next');
        this.dotsContainer = container.querySelector('.slider-dots');
        this.currentIndex = 0;
        this.autoPlayInterval = null;
        
        this.init();
    }
    
    init() {
        if (this.slides.length === 0) return;
        
        // Create dots
        this.slides.forEach((_, index) => {
            const dot = document.createElement('button');
            dot.classList.add('slider-dot');
            dot.addEventListener('click', () => this.goToSlide(index));
            this.dotsContainer.appendChild(dot);
        });
        
        this.updateDots();
        
        // Add event listeners
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prevSlide());
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.nextSlide());
        }
        
        // Start autoplay
        this.startAutoPlay();
        
        // Pause autoplay on hover
        this.container.addEventListener('mouseenter', () => this.stopAutoPlay());
        this.container.addEventListener('mouseleave', () => this.startAutoPlay());
    }
    
    goToSlide(index) {
        if (index < 0) index = this.slides.length - 1;
        if (index >= this.slides.length) index = 0;
        
        this.currentIndex = index;
        const offset = -this.currentIndex * 100;
        this.container.querySelector('.slider-container').style.transform = `translateX(${offset}%)`;
        this.updateDots();
    }
    
    prevSlide() {
        this.goToSlide(this.currentIndex - 1);
    }
    
    nextSlide() {
        this.goToSlide(this.currentIndex + 1);
    }
    
    updateDots() {
        const dots = this.dotsContainer.querySelectorAll('.slider-dot');
        dots.forEach((dot, index) => {
            if (index === this.currentIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }
    
    startAutoPlay() {
        if (this.autoPlayInterval) return;
        this.autoPlayInterval = setInterval(() => this.nextSlide(), 5000);
    }
    
    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
}

// Initialize slider if exists
const slider = document.querySelector('.slider');
if (slider) {
    new Slider(slider);
}

// Cart functionality
class Cart {
    constructor() {
        this.init();
    }
    
    init() {
        this.updateCartCount();
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Add to cart buttons
        document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const productId = btn.dataset.productId;
                const quantity = btn.dataset.quantity || 1;
                this.addToCart(productId, quantity);
            });
        });
        
        // Quantity buttons in cart
        document.querySelectorAll('.quantity-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = btn.dataset.action;
                const itemId = btn.dataset.itemId;
                this.updateQuantity(itemId, action);
            });
        });
        
        // Remove from cart
        document.querySelectorAll('.cart-item-remove').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const itemId = btn.dataset.itemId;
                this.removeFromCart(itemId);
            });
        });
    }
    
    async addToCart(productId, quantity) {
        try {
            const response = await fetch(`/ajouter-panier/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ quantity: parseInt(quantity) })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateCartCount(data.total);
                this.showNotification('Produit ajouté au panier', 'success');
            }
        } catch (error) {
            this.showNotification('Erreur lors de l\'ajout au panier', 'error');
        }
    }
    
    async updateQuantity(itemId, action) {
        // Implement quantity update logic
    }
    
    async removeFromCart(itemId) {
        // Implement remove from cart logic
    }
    
    updateCartCount(count) {
        const cartCount = document.getElementById('cartCount');
        if (cartCount) {
            cartCount.textContent = count || '0';
        }
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize cart
const cart = new Cart();

// Promo popup
const promoPopup = document.getElementById('promoPopup');
const closePromoBtn = document.getElementById('closePromoPopup');

if (promoPopup && closePromoBtn) {
    closePromoBtn.addEventListener('click', () => {
        promoPopup.style.display = 'none';
    });
    
    // Close when clicking outside
    promoPopup.addEventListener('click', (e) => {
        if (e.target === promoPopup) {
            promoPopup.style.display = 'none';
        }
    });
}

// Copy promo code
function copyPromoCode() {
    const codeElement = document.querySelector('.promo-code .code');
    if (codeElement) {
        const code = codeElement.textContent;
        navigator.clipboard.writeText(code).then(() => {
            const copyBtn = document.querySelector('.copy-btn');
            const originalText = copyBtn.textContent;
            copyBtn.textContent = 'Copié !';
            setTimeout(() => {
                copyBtn.textContent = originalText;
            }, 2000);
        });
    }
}

// Payment method selection
document.querySelectorAll('.payment-method-card').forEach(card => {
    card.addEventListener('click', () => {
        document.querySelectorAll('.payment-method-card').forEach(c => {
            c.classList.remove('selected');
        });
        card.classList.add('selected');
        
        const method = card.dataset.method;
        document.querySelectorAll('.payment-form').forEach(form => {
            form.style.display = 'none';
        });
        
        const selectedForm = document.getElementById(`payment-${method}`);
        if (selectedForm) {
            selectedForm.style.display = 'block';
        }
    });
});

// Form validation
class FormValidator {
    constructor(form) {
        this.form = form;
        this.init();
    }
    
    init() {
        this.form.addEventListener('submit', (e) => {
            if (!this.validate()) {
                e.preventDefault();
            }
        });
        
        this.form.querySelectorAll('input, textarea, select').forEach(field => {
            field.addEventListener('blur', () => this.validateField(field));
            field.addEventListener('input', () => this.clearFieldError(field));
        });
    }
    
    validate() {
        let isValid = true;
        this.form.querySelectorAll('input, textarea, select').forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });
        return isValid;
    }
    
    validateField(field) {
        this.clearFieldError(field);
        
        if (field.required && !field.value.trim()) {
            this.showFieldError(field, 'Ce champ est requis');
            return false;
        }
        
        if (field.type === 'email' && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                this.showFieldError(field, 'Email invalide');
                return false;
            }
        }
        
        if (field.type === 'tel' && field.value) {
            const phoneRegex = /^[0-9+\-\s]{10,}$/;
            if (!phoneRegex.test(field.value)) {
                this.showFieldError(field, 'Téléphone invalide');
                return false;
            }
        }
        
        return true;
    }
    
    showFieldError(field, message) {
        field.classList.add('error');
        
        const errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        errorElement.textContent = message;
        
        field.parentNode.appendChild(errorElement);
    }
    
    clearFieldError(field) {
        field.classList.remove('error');
        const errorElement = field.parentNode.querySelector('.field-error');
        if (errorElement) {
            errorElement.remove();
        }
    }
}

// Initialize form validation
document.querySelectorAll('form').forEach(form => {
    new FormValidator(form);
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Lazy loading images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Price formatting
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
}

// Date formatting
function formatDate(date) {
    return new Intl.DateTimeFormat('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(date));
}

// Export functions
window.copyPromoCode = copyPromoCode;
window.formatPrice = formatPrice;
window.formatDate = formatDate;