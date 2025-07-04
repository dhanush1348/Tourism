document.addEventListener('DOMContentLoaded', function() {
    // Handle wishlist toggle buttons
    document.querySelectorAll('.wishlist-btn').forEach(button => {
        button.addEventListener('click', function() {
            const tourId = this.dataset.tourId;
            const heartIcon = this.querySelector('i');
            
            // Toggle heart icon
            if (heartIcon.classList.contains('fa-heart-broken')) {
                heartIcon.classList.remove('fa-heart-broken');
                heartIcon.classList.add('fa-heart');
            } else {
                heartIcon.classList.remove('fa-heart');
                heartIcon.classList.add('fa-heart-broken');
            }
            
            // Show toast notification
            const toast = document.createElement('div');
            toast.className = 'toast align-items-center text-white bg-success border-0 position-fixed bottom-0 end-0 m-3';
            toast.setAttribute('role', 'alert');
            toast.setAttribute('aria-live', 'assertive');
            toast.setAttribute('aria-atomic', 'true');
            
            toast.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        ${heartIcon.classList.contains('fa-heart') ? 'Tour added to wishlist!' : 'Tour removed from wishlist!'}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            `;
            
            document.body.appendChild(toast);
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
            
            // Remove toast after it's hidden
            toast.addEventListener('hidden.bs.toast', function() {
                toast.remove();
            });
        });
    });
}); 