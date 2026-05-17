document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(msg) {
        setTimeout(function() {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity = '0';
            setTimeout(function() {
                if (msg.parentNode) {
                    msg.parentNode.removeChild(msg);
                }
            }, 500);
        }, 5000);

        msg.addEventListener('click', function() {
            msg.style.transition = 'opacity 0.2s';
            msg.style.opacity = '0';
            setTimeout(function() {
                if (msg.parentNode) {
                    msg.parentNode.removeChild(msg);
                }
            }, 200);
        });
    });

    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!validateForm(form)) {
                event.preventDefault();
                return false;
            }
        });
    });

    function validateForm(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(function(input) {
            const errorEl = input.parentNode.querySelector('.form-error');
            if (errorEl) {
                errorEl.parentNode.removeChild(errorEl);
            }
            input.classList.remove('input-error');

            if (input.hasAttribute('required') && !input.value.trim()) {
                showError(input, 'This field is required');
                isValid = false;
            }
        });
        return isValid;
    }

    function showError(input, message) {
        input.classList.add('input-error');
        const error = document.createElement('div');
        error.className = 'form-error';
        error.textContent = message;
        input.parentNode.appendChild(error);
    }
});