// Task Machine Pro - Interactive UI Enhancements

// Wait for the page to load
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
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

    // Add hover effects to custom cards
    const cards = document.querySelectorAll('.custom-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
            this.style.boxShadow = '0 15px 35px rgba(59, 130, 246, 0.3)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 4px 15px rgba(59, 130, 246, 0.2)';
        });
    });

    // Add typing animation to headers
    const headers = document.querySelectorAll('h1');
    headers.forEach(header => {
        if (header.textContent.includes('MyMenuBase')) {
            const text = header.textContent;
            header.textContent = '';
            let i = 0;
            
            function typeWriter() {
                if (i < text.length) {
                    header.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, 100);
                }
            }
            
            // Start typing animation after a delay
            setTimeout(typeWriter, 1000);
        }
    });

    // Add particle effect to the background
    createParticles();

    // Add smooth transitions to buttons
    const buttons = document.querySelectorAll('.stButton button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // Add loading animation
    showLoadingAnimation();
});

// Create floating particles effect
function createParticles() {
    const particleContainer = document.createElement('div');
    particleContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    `;
    document.body.appendChild(particleContainer);

    const colors = ['#FF6B35', '#3B82F6', '#10B981', '#60A5FA'];
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            border-radius: 50%;
            opacity: ${Math.random() * 0.5 + 0.2};
            animation: float ${Math.random() * 10 + 10}s linear infinite;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
        `;
        particleContainer.appendChild(particle);
    }
}

// Add floating animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 5px rgba(59, 130, 246, 0.3);
        }
        50% {
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
        }
    }
`;
document.head.appendChild(style);

// Show loading animation
function showLoadingAnimation() {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loading-animation';
    loadingDiv.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        transition: opacity 0.5s ease-out;
    `;
    
    const spinner = document.createElement('div');
    spinner.style.cssText = `
        width: 50px;
        height: 50px;
        border: 3px solid rgba(59, 130, 246, 0.3);
        border-top: 3px solid #60A5FA;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    `;
    
    const text = document.createElement('div');
    text.textContent = 'MyMenuBase';
    text.style.cssText = `
        color: #60A5FA;
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1rem;
        text-align: center;
    `;
    
    const container = document.createElement('div');
    container.style.cssText = `
        display: flex;
        flex-direction: column;
        align-items: center;
    `;
    
    container.appendChild(spinner);
    container.appendChild(text);
    loadingDiv.appendChild(container);
    document.body.appendChild(loadingDiv);
    
    // Remove loading animation after 2 seconds
    setTimeout(() => {
        loadingDiv.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(loadingDiv);
        }, 500);
    }, 2000);
}

// Add smooth reveal animation to elements
function revealOnScroll() {
    const elements = document.querySelectorAll('.custom-card, .stMetric, .stButton');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    elements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(element);
    });
}

// Initialize reveal on scroll when page loads
window.addEventListener('load', revealOnScroll);

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="text"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to clear focus
    if (e.key === 'Escape') {
        document.activeElement.blur();
    }
});

// Add tooltip functionality
function addTooltips() {
    const elements = document.querySelectorAll('[data-tooltip]');
    elements.forEach(element => {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = element.getAttribute('data-tooltip');
        tooltip.style.cssText = `
            position: absolute;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 0.5rem;
            border-radius: 5px;
            font-size: 0.8rem;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 1000;
        `;
        
        element.addEventListener('mouseenter', function(e) {
            tooltip.style.opacity = '1';
            tooltip.style.left = e.pageX + 10 + 'px';
            tooltip.style.top = e.pageY - 30 + 'px';
            document.body.appendChild(tooltip);
        });
        
        element.addEventListener('mouseleave', function() {
            tooltip.style.opacity = '0';
            setTimeout(() => {
                if (tooltip.parentNode) {
                    tooltip.parentNode.removeChild(tooltip);
                }
            }, 300);
        });
    });
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', addTooltips);

// Add notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    // Set background based on type
    switch(type) {
        case 'success':
            notification.style.background = 'linear-gradient(135deg, #10B981, #059669)';
            break;
        case 'error':
            notification.style.background = 'linear-gradient(135deg, #EF4444, #DC2626)';
            break;
        case 'warning':
            notification.style.background = 'linear-gradient(135deg, #F59E0B, #D97706)';
            break;
        default:
            notification.style.background = 'linear-gradient(135deg, #3B82F6, #2563EB)';
    }
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Export functions for global use
window.TaskMachinePro = {
    showNotification,
    revealOnScroll,
    createParticles
};
