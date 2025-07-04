document.addEventListener('DOMContentLoaded', function() {
    const tourPackageSelect = document.getElementById('tour_package');
    const numPeopleInput = document.getElementById('num_people');
    const totalAmountInput = document.getElementById('total_amount');
    const paymentMethodSelect = document.getElementById('payment_method');
    const creditCardDetails = document.getElementById('credit-card-details');

    // Function to calculate total amount
    function calculateTotal() {
        const selectedOption = tourPackageSelect.options[tourPackageSelect.selectedIndex];
        const price = parseFloat(selectedOption.getAttribute('data-price')) || 0;
        const numPeople = parseInt(numPeopleInput.value) || 0;
        const total = price * numPeople;
        totalAmountInput.value = total.toFixed(2);
    }

    // Function to toggle credit card details
    function toggleCreditCardDetails() {
        if (paymentMethodSelect.value === 'credit_card') {
            creditCardDetails.style.display = 'block';
        } else {
            creditCardDetails.style.display = 'none';
        }
    }

    // Event listeners
    tourPackageSelect.addEventListener('change', calculateTotal);
    numPeopleInput.addEventListener('input', calculateTotal);
    paymentMethodSelect.addEventListener('change', toggleCreditCardDetails);

    // Initial calculations
    calculateTotal();
    toggleCreditCardDetails();

    // Form validation
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('is-invalid');
            } else {
                field.classList.remove('is-invalid');
            }
        });

        if (!isValid) {
            event.preventDefault();
            alert('Please fill in all required fields.');
        }
    });
}); 