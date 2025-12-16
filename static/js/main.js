/**
 * Ejeh Ankpa Palace Platform
 * Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================
    // Back to Top Button
    // ============================================
    const backToTopBtn = document.getElementById('backToTop');
    
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });
        
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // ============================================
    // Navbar Scroll Effect
    // ============================================
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // ============================================
    // Event Countdown Timer
    // ============================================
    function initCountdown() {
        const countdowns = document.querySelectorAll('[data-countdown]');
        
        countdowns.forEach(function(countdown) {
            const targetDate = new Date(countdown.dataset.countdown).getTime();
            
            const timer = setInterval(function() {
                const now = new Date().getTime();
                const distance = targetDate - now;
                
                if (distance < 0) {
                    clearInterval(timer);
                    countdown.innerHTML = '<span class="text-muted">Event has started</span>';
                    return;
                }
                
                const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                
                countdown.innerHTML = `
                    <div class="countdown-timer">
                        <div class="countdown-item">
                            <span class="number">${days}</span>
                            <span class="label">Days</span>
                        </div>
                        <div class="countdown-item">
                            <span class="number">${hours}</span>
                            <span class="label">Hours</span>
                        </div>
                        <div class="countdown-item">
                            <span class="number">${minutes}</span>
                            <span class="label">Minutes</span>
                        </div>
                        <div class="countdown-item">
                            <span class="number">${seconds}</span>
                            <span class="label">Seconds</span>
                        </div>
                    </div>
                `;
            }, 1000);
        });
    }
    
    initCountdown();
    
    // ============================================
    // Gallery Lightbox
    // ============================================
    function initLightbox() {
        const galleryItems = document.querySelectorAll('.gallery-item[data-lightbox]');
        
        galleryItems.forEach(function(item) {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                
                const imgSrc = this.dataset.lightbox;
                const title = this.dataset.title || '';
                
                // Create lightbox
                const lightbox = document.createElement('div');
                lightbox.className = 'lightbox';
                lightbox.innerHTML = `
                    <div class="lightbox-content">
                        <button class="lightbox-close">&times;</button>
                        <img src="${imgSrc}" alt="${title}">
                        ${title ? `<div class="lightbox-caption">${title}</div>` : ''}
                    </div>
                `;
                
                document.body.appendChild(lightbox);
                document.body.style.overflow = 'hidden';
                
                // Close lightbox
                lightbox.addEventListener('click', function(e) {
                    if (e.target === lightbox || e.target.classList.contains('lightbox-close')) {
                        lightbox.remove();
                        document.body.style.overflow = '';
                    }
                });
                
                // Close on escape
                document.addEventListener('keydown', function(e) {
                    if (e.key === 'Escape') {
                        lightbox.remove();
                        document.body.style.overflow = '';
                    }
                });
            });
        });
    }
    
    initLightbox();
    
    // ============================================
    // Newsletter Form AJAX
    // ============================================
    const newsletterForm = document.querySelector('form[action*="newsletter"]');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            // Let the form submit normally if AJAX is not needed
            // Or handle via AJAX if required
        });
    }
    
    // ============================================
    // Smooth Scroll for Anchor Links
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // ============================================
    // Image Preview for File Inputs
    // ============================================
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const file = this.files[0];
            
            if (file) {
                const reader = new FileReader();
                const preview = document.getElementById(this.dataset.preview);
                
                reader.onload = function(e) {
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                
                reader.readAsDataURL(file);
            }
        });
    });
    
    // ============================================
    // Form Validation Enhancement
    // ============================================
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        });
    });
    
    // ============================================
    // Toast Notifications
    // ============================================
    window.showToast = function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(container);
        }
        
        container.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    };
    
    // ============================================
    // Auto-dismiss Alerts
    // ============================================
    const alerts = document.querySelectorAll('.alert-dismissible');
    
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // ============================================
    // Character Counter for Textareas
    // ============================================
    const textareas = document.querySelectorAll('textarea[maxlength]');
    
    textareas.forEach(function(textarea) {
        const maxLength = textarea.getAttribute('maxlength');
        
        // Create counter element
        const counter = document.createElement('small');
        counter.className = 'text-muted d-block text-end';
        counter.textContent = `0 / ${maxLength}`;
        
        textarea.parentNode.appendChild(counter);
        
        textarea.addEventListener('input', function() {
            counter.textContent = `${this.value.length} / ${maxLength}`;
            
            if (this.value.length >= maxLength * 0.9) {
                counter.classList.add('text-warning');
            } else {
                counter.classList.remove('text-warning');
            }
        });
    });
    
    // ============================================
    // Print Button
    // ============================================
    const printButtons = document.querySelectorAll('[data-print]');
    
    printButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // ============================================
    // Share Functionality
    // ============================================
    const shareButtons = document.querySelectorAll('[data-share]');
    
    shareButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const url = this.dataset.share || window.location.href;
            const title = this.dataset.title || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                });
            } else {
                // Fallback: copy to clipboard
                navigator.clipboard.writeText(url).then(function() {
                    window.showToast('Link copied to clipboard!', 'success');
                });
            }
        });
    });
    
});

// ============================================
// Lightbox Styles (injected)
// ============================================
const lightboxStyles = document.createElement('style');
lightboxStyles.textContent = `
    .lightbox {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeIn 0.3s ease;
    }
    
    .lightbox-content {
        position: relative;
        max-width: 90%;
        max-height: 90%;
    }
    
    .lightbox-content img {
        max-width: 100%;
        max-height: 85vh;
        object-fit: contain;
        border-radius: 4px;
    }
    
    .lightbox-close {
        position: absolute;
        top: -40px;
        right: 0;
        background: none;
        border: none;
        color: white;
        font-size: 2rem;
        cursor: pointer;
        opacity: 0.8;
        transition: opacity 0.3s;
    }
    
    .lightbox-close:hover {
        opacity: 1;
    }
    
    .lightbox-caption {
        text-align: center;
        color: white;
        padding: 1rem;
        font-size: 1rem;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(lightboxStyles);
