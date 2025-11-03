/**
 * Museum of Military Glory - Main JavaScript
 * Modern, professional JavaScript with proper error handling
 */

(function() {
    'use strict';

    // =========================================================================
    // CONFIGURATION
    // =========================================================================
    const CONFIG = {
        panorama: {
            autoRotate: true,
            autoRotateSpeed: 0.3,
            controlBar: false,
            autoRotateActivationDuration: 5000,
            textFadeDelay: 5000
        },
        animation: {
            duration: 1000,
            easing: 'ease-out'
        }
    };

    // =========================================================================
    // PANORAMA INITIALIZATION
    // =========================================================================
    class PanoramaViewer {
        constructor(containerSelector, imageUrl) {
            this.container = document.querySelector(containerSelector);
            this.imageUrl = imageUrl;
            this.viewer = null;
            this.autoRotateTimeout = null;
        }

        /**
         * Initialize the panorama viewer
         */
        init() {
            if (!this.container) {
                console.warn('Panorama container not found');
                return;
            }

            if (!PANOLENS) {
                console.error('PANOLENS library not loaded');
                return;
            }

            try {
                // Get image path dynamically
                const imagePath = this.getImagePath();

                // Create panorama
                const panorama = new PANOLENS.ImagePanorama(imagePath);

                // Create viewer
                this.viewer = new PANOLENS.Viewer({
                    container: this.container,
                    autoRotate: CONFIG.panorama.autoRotate,
                    autoRotateSpeed: CONFIG.panorama.autoRotateSpeed,
                    controlBar: CONFIG.panorama.controlBar,
                    autoRotateActivationDuration: CONFIG.panorama.autoRotateActivationDuration,
                });

                this.viewer.add(panorama);

                // Setup event listeners
                this.setupEventListeners();

                console.log('Panorama viewer initialized successfully');
            } catch (error) {
                console.error('Error initializing panorama:', error);
                this.handlePanoramaError();
            }
        }

        /**
         * Get image path from static files
         */
        getImagePath() {
            // Try to get Django's static URL from meta tag or window
            const staticUrl = this.getStaticUrl();
            return `${staticUrl}images/1.jpg`;
        }

        /**
         * Get static URL from Django
         */
        getStaticUrl() {
            // Check for meta tag with static URL
            const metaStatic = document.querySelector('meta[name="static-url"]');
            if (metaStatic) {
                return metaStatic.getAttribute('content');
            }

            // Fallback to relative path
            return '/static/';
        }

        /**
         * Setup event listeners for panorama interaction
         */
        setupEventListeners() {
            if (!this.viewer) return;

            // Pause auto-rotate on interaction
            this.container.addEventListener('mousedown', () => {
                this.pauseAutoRotate();
            });

            this.container.addEventListener('touchstart', () => {
                this.pauseAutoRotate();
            });
        }

        /**
         * Pause auto-rotate and resume after inactivity
         */
        pauseAutoRotate() {
            if (!this.viewer) return;

            this.viewer.autoRotate = false;

            // Clear existing timeout
            if (this.autoRotateTimeout) {
                clearTimeout(this.autoRotateTimeout);
            }

            // Resume auto-rotate after inactivity
            this.autoRotateTimeout = setTimeout(() => {
                this.viewer.autoRotate = true;
            }, CONFIG.panorama.autoRotateActivationDuration);
        }

        /**
         * Handle panorama loading error
         */
        handlePanoramaError() {
            const errorMessage = document.createElement('div');
            errorMessage.className = 'panorama-error';
            errorMessage.style.cssText = `
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 2rem;
                border-radius: 10px;
                text-align: center;
                z-index: 10;
            `;
            errorMessage.innerHTML = `
                <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
                <p>Не удалось загрузить панораму</p>
            `;
            this.container.appendChild(errorMessage);
        }

        /**
         * Destroy the viewer
         */
        destroy() {
            if (this.autoRotateTimeout) {
                clearTimeout(this.autoRotateTimeout);
            }

            if (this.viewer) {
                this.viewer.dispose();
                this.viewer = null;
            }
        }
    }

    // =========================================================================
    // TEXT ANIMATION
    // =========================================================================
    class HeroTextAnimation {
        constructor(selector, delay) {
            this.element = document.querySelector(selector);
            this.delay = delay;
        }

        /**
         * Fade out the text after delay
         */
        init() {
            if (!this.element) return;

            setTimeout(() => {
                this.fadeOut();
            }, this.delay);
        }

        /**
         * Fade out animation
         */
        fadeOut() {
            if (!this.element) return;

            this.element.style.transition = `opacity ${CONFIG.animation.duration}ms ${CONFIG.animation.easing}`;
            this.element.classList.add('fade-out');
        }

        /**
         * Fade in animation
         */
        fadeIn() {
            if (!this.element) return;

            this.element.classList.remove('fade-out');
        }
    }

    // =========================================================================
    // PERFORMANCE MONITORING
    // =========================================================================
    class PerformanceMonitor {
        constructor() {
            this.metrics = {};
        }

        /**
         * Mark start time
         */
        mark(label) {
            this.metrics[label] = performance.now();
        }

        /**
         * Measure and log duration
         */
        measure(label, startLabel) {
            const endTime = performance.now();
            const startTime = this.metrics[startLabel] || 0;
            const duration = endTime - startTime;

            console.log(`${label}: ${duration.toFixed(2)}ms`);
            return duration;
        }
    }

    // =========================================================================
    // INITIALIZATION
    // =========================================================================
    function init() {
        const perfMonitor = new PerformanceMonitor();
        perfMonitor.mark('init-start');

        // Initialize panorama viewer
        const panoramaViewer = new PanoramaViewer('#panorama', 'static/images/1.jpg');
        panoramaViewer.init();

        // Initialize hero text animation
        const heroTextAnimation = new HeroTextAnimation(
            '#heroContent',
            CONFIG.panorama.textFadeDelay
        );
        heroTextAnimation.init();

        perfMonitor.measure('Total initialization time', 'init-start');

        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            panoramaViewer.destroy();
        });
    }

    // =========================================================================
    // DOM READY
    // =========================================================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();

// =========================================================================
// UTILITY FUNCTIONS
// =========================================================================

/**
 * Debounce function to limit rate of function calls
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function to limit rate of function calls
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Check if element is in viewport
 */
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

/**
 * Lazy load images
 */
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading if needed
if ('IntersectionObserver' in window) {
    lazyLoadImages();
}
