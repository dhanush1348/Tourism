// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Initialize Tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize all popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle booking form submission
    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', handleBookingSubmit);
    }

    // Handle dynamic price calculation
    const participantsInput = document.getElementById('participants');
    if (participantsInput) {
        participantsInput.addEventListener('change', updateTotalPrice);
    }
});

// Booking Form Handler
async function handleBookingSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    const formData = new FormData(form);

    try {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';

        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });

        const data = await response.json();

        if (response.ok) {
            if (data.stripe_session_id) {
                // Redirect to Stripe Checkout
                stripe.redirectToCheckout({
                    sessionId: data.stripe_session_id
                });
            } else {
                window.location.href = data.redirect_url;
            }
        } else {
            throw new Error(data.error || 'Something went wrong');
        }
    } catch (error) {
        showAlert('error', error.message);
    } finally {
        submitButton.disabled = false;
        submitButton.innerHTML = 'Book Now';
    }
}

// Price Calculator
function updateTotalPrice() {
    const participants = parseInt(document.getElementById('participants').value) || 0;
    const basePrice = parseFloat(document.getElementById('tour-price').dataset.price) || 0;
    const totalPrice = participants * basePrice;
    
    document.getElementById('total-price').textContent = formatCurrency(totalPrice);
}

// Alert System
function showAlert(type, message) {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.querySelector('.container').insertAdjacentElement('afterbegin', alertContainer);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        const alert = bootstrap.Alert.getOrCreateInstance(alertContainer);
        alert.close();
    }, 5000);
}

// Image Gallery
function initializeGallery(galleryId) {
    const gallery = document.getElementById(galleryId);
    if (!gallery) return;

    const mainImage = gallery.querySelector('.main-image img');
    const thumbnails = gallery.querySelectorAll('.thumbnails img');

    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', () => {
            mainImage.src = thumb.dataset.large;
            thumbnails.forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');
        });
    });
}

// Review System
function initializeRating(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const stars = container.querySelectorAll('.star');
    const ratingInput = container.querySelector('input[name="rating"]');

    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            const rating = index + 1;
            ratingInput.value = rating;
            updateStars(stars, rating);
        });

        star.addEventListener('mouseover', () => {
            updateStars(stars, index + 1);
        });

        star.addEventListener('mouseout', () => {
            updateStars(stars, parseInt(ratingInput.value) || 0);
        });
    });
}

function updateStars(stars, rating) {
    stars.forEach((star, index) => {
        star.classList.toggle('active', index < rating);
    });
}

// WebSocket Chat
class ChatManager {
    constructor(roomName) {
        this.roomName = roomName;
        this.messageContainer = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('chat-input');
        this.socket = null;
        
        this.initialize();
    }

    initialize() {
        this.socket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/' + this.roomName + '/'
        );

        this.socket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            this.addMessage(data);
        };

        this.socket.onclose = () => {
            console.error('Chat socket closed unexpectedly');
        };

        document.getElementById('chat-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
    }

    sendMessage() {
        const message = this.messageInput.value.trim();
        if (message) {
            this.socket.send(JSON.stringify({
                'message': message
            }));
            this.messageInput.value = '';
        }
    }

    addMessage(data) {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message';
        messageElement.innerHTML = `
            <strong>${data.user}</strong>
            <span class="message-time">${formatDate(data.timestamp)}</span>
            <p>${data.message}</p>
        `;
        this.messageContainer.appendChild(messageElement);
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
}

// Animation on scroll
function initScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    });
    
    elements.forEach(element => {
        observer.observe(element);
    });
}

// Initialize all functionality
document.addEventListener('DOMContentLoaded', function() {
    initImageGallery('image-gallery');
    initReviewSystem('rating-container');
    initScrollAnimations();
    
    // Initialize chat if chat container exists
    if (document.querySelector('.chat-container')) {
        window.chatManager = new ChatManager('general');
    }
});

// Export utilities for use in other scripts
window.utils = {
    formatCurrency,
    formatDate,
    showAlert,
    initializeGallery,
    initializeRating,
    ChatManager
}; 