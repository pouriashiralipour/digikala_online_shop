document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const button = event.target.querySelector('button[type="submit"]');
            button.classList.add('loading');
            
            const formData = new FormData(registerForm);
            const xhr = new XMLHttpRequest();

            xhr.open('POST', registerForm.action);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

            xhr.onload = function() {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);

                    // پاک کردن ارورهای قبلی
                    document.querySelectorAll('.error').forEach(function(errorDiv) {
                        errorDiv.textContent = '';
                    });

                    if (response.success) {
                        setTimeout(() => {
                            window.location.href = response.redirect_url;
                        }, 2000); // 2 second delay before redirect (adjust as needed)
                    } else {
                        button.classList.remove('loading');
                        if (response.errors) {
                            for (const [field, messages] of Object.entries(response.errors)) {
                                const errorDiv = document.getElementById(`${field}_error`);
                                if (errorDiv) {
                                    errorDiv.textContent = messages.join(', ');
                                }
                            }
                        } else {
                            alert(response.message);
                        }
                    }
                } else {
                    button.classList.remove('loading');
                    alert('خطایی رخ داد.');
                }
            };

            xhr.send(formData);
        });
    }

    const verifyForm = document.getElementById('verify-form');
    if (verifyForm) {
        verifyForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const button = event.target.querySelector('button[type="submit"]');
            button.classList.add('loading');

            const formData = new FormData(verifyForm);
            const xhr = new XMLHttpRequest();

            xhr.open('POST', verifyForm.action);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

            // Clear previous errors
            const errorContainer = verifyForm.querySelector('.error-message');
            if (errorContainer) {
                errorContainer.remove();
            }

            xhr.onload = function() {
                button.classList.remove('loading');

                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        window.location.href = response.redirect_url;
                    } else {
                        const errorMessage = document.createElement('div');
                        errorMessage.classList.add('error-message');
                        errorMessage.textContent = response.message;
                        verifyForm.querySelector('.form-element-row').appendChild(errorMessage);
                    }
                } else {
                    const errorMessage = document.createElement('div');
                    errorMessage.classList.add('error-message');
                    errorMessage.textContent = 'An error occurred. Please try again.';
                    verifyForm.querySelector('.form-element-row').appendChild(errorMessage);
                }
            };

            xhr.send(formData);
        });
    }
});
