// Main JavaScript for AI Tools Directory

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Search form auto-submit on filter change
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        const departmentSelect = searchForm.querySelector('select[name="department"]');
        const categorySelect = searchForm.querySelector('select[name="category"]');
        
        if (departmentSelect) {
            departmentSelect.addEventListener('change', function() {
                if (this.value !== '') {
                    searchForm.submit();
                }
            });
        }
        
        if (categorySelect) {
            categorySelect.addEventListener('change', function() {
                if (this.value !== '') {
                    searchForm.submit();
                }
            });
        }
    }
    
    // Search input enhancement
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        // Add search icon animation
        searchInput.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        searchInput.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
        
        // Clear search button
        if (searchInput.value) {
            addClearButton(searchInput);
        }
        
        searchInput.addEventListener('input', function() {
            if (this.value) {
                addClearButton(this);
            } else {
                removeClearButton(this);
            }
        });
    }
    
    // Smooth scrolling for anchor links
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
    
    // External link handling
    document.querySelectorAll('a[target="_blank"]').forEach(link => {
        link.addEventListener('click', function(e) {
            // Add loading state
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Opening...';
            
            // Reset after a short delay
            setTimeout(() => {
                this.innerHTML = originalText;
            }, 1000);
        });
    });
    
    // Card hover effects
    document.querySelectorAll('.tool-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow-lg');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-lg');
        });
    });
    
    // Lazy loading for images (if any are added later)
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Back to top button
    const backToTopBtn = createBackToTopButton();
    document.body.appendChild(backToTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });
    
    // Analytics tracking for external links
    document.querySelectorAll('a[href^="http"]:not([href*="' + window.location.hostname + '"])').forEach(link => {
        link.addEventListener('click', function() {
            // Track external link clicks
            console.log('External link clicked:', this.href);
        });
    });
});

// Helper function to add clear button to search input
function addClearButton(input) {
    if (input.parentElement.querySelector('.clear-search')) return;
    
    const clearBtn = document.createElement('button');
    clearBtn.type = 'button';
    clearBtn.className = 'btn btn-link clear-search';
    clearBtn.innerHTML = '<i class="fas fa-times"></i>';
    clearBtn.style.cssText = 'position: absolute; right: 45px; top: 50%; transform: translateY(-50%); z-index: 10; border: none; background: none; color: #6c757d;';
    
    clearBtn.addEventListener('click', function() {
        input.value = '';
        input.focus();
        this.remove();
    });
    
    input.parentElement.style.position = 'relative';
    input.parentElement.appendChild(clearBtn);
}

// Helper function to remove clear button
function removeClearButton(input) {
    const clearBtn = input.parentElement.querySelector('.clear-search');
    if (clearBtn) {
        clearBtn.remove();
    }
}

// Helper function to create back to top button
function createBackToTopButton() {
    const btn = document.createElement('button');
    btn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    btn.className = 'btn btn-primary back-to-top';
    btn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: none;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    `;
    
    // Add CSS class for show state
    const style = document.createElement('style');
    style.textContent = `
        .back-to-top.show {
            display: block !important;
        }
        .back-to-top:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        }
    `;
    document.head.appendChild(style);
    
    btn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    return btn;
}

// Search suggestions functionality
function initSearchSuggestions() {
    const searchInput = document.querySelector('input[name="q"]');
    if (!searchInput) return;
    
    let suggestionsContainer = document.getElementById('search-suggestions');
    if (!suggestionsContainer) {
        suggestionsContainer = document.createElement('div');
        suggestionsContainer.id = 'search-suggestions';
        suggestionsContainer.className = 'search-suggestions';
        suggestionsContainer.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #dee2e6;
            border-top: none;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            max-height: 200px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
        `;
        searchInput.parentElement.appendChild(suggestionsContainer);
    }
    
    searchInput.addEventListener('input', debounce(function() {
        const query = this.value.trim();
        if (query.length < 2) {
            suggestionsContainer.style.display = 'none';
            return;
        }
        
        // Here you would typically make an API call to get suggestions
        // For now, we'll just show some basic suggestions
        showSuggestions(query, suggestionsContainer);
    }, 300));
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.style.display = 'none';
        }
    });
}

// Show search suggestions
function showSuggestions(query, container) {
    // This is a basic implementation - in a real app, you'd fetch from an API
    const suggestions = [
        'ChatGPT',
        'DALL-E 2',
        'Midjourney',
        'Notion AI',
        'Copy AI'
    ].filter(suggestion => 
        suggestion.toLowerCase().includes(query.toLowerCase())
    );
    
    if (suggestions.length === 0) {
        container.style.display = 'none';
        return;
    }
    
    container.innerHTML = suggestions.map(suggestion => 
        `<div class="suggestion-item" style="padding: 10px; cursor: pointer; border-bottom: 1px solid #f8f9fa;">
            <i class="fas fa-search me-2 text-muted"></i>
            ${suggestion}
        </div>`
    ).join('');
    
    container.style.display = 'block';
    
    // Add click handlers
    container.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('click', function() {
            document.querySelector('input[name="q"]').value = this.textContent.trim();
            container.style.display = 'none';
            document.querySelector('form[action*="search"]').submit();
        });
    });
}

// Debounce function for search input
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

// Initialize search suggestions
document.addEventListener('DOMContentLoaded', initSearchSuggestions);
