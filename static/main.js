document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();

            // Clear previous errors
            document.querySelectorAll('.error').forEach(function(errorDiv) {
                errorDiv.textContent = '';
            });

            const phoneNumberInput = registerForm.querySelector('input[name="phone_number"]');
            const phoneNumber = phoneNumberInput.value.trim();

            if (phoneNumber.length > 11) {
                const errorDiv = document.getElementById('phone_number_error');
                if (errorDiv) {
                    errorDiv.textContent = 'شماره موبایل یا ایمیل نباید بیشتر از 11 کاراکتر باشد.';
                }
                return; // Prevent form submission
            }

            const button = event.target.querySelector('button[type="submit"]');
            button.classList.add('loading');
            
            const formData = new FormData(registerForm);
            const xhr = new XMLHttpRequest();

            xhr.open('POST', registerForm.action);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

            xhr.onload = function() {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);

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

            // Clear previous errors
            document.querySelectorAll('.error').forEach(function(errorDiv) {
                errorDiv.textContent = '';
            });

            const otpInput = verifyForm.querySelector('input[name="otp"]');
            const otp = otpInput.value.trim();

            if (!otp) {
                const errorDiv = document.getElementById('otp_error');
                if (errorDiv) {
                    errorDiv.textContent = 'لطفا کد تایید را وارد کنید.';
                }
                button.classList.remove('loading');
                return; // Prevent form submission
            }

            if (otp.length > 4) {
                const errorDiv = document.getElementById('otp_error');
                if (errorDiv) {
                    errorDiv.textContent = 'کد تایید نباید بیشتر از 4 کاراکتر باشد.';
                }
                button.classList.remove('loading');
                return; // Prevent form submission
            }

            const formData = new FormData(verifyForm);
            const xhr = new XMLHttpRequest();

            xhr.open('POST', verifyForm.action);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

            xhr.onload = function() {
                button.classList.remove('loading');

                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        window.location.href = response.redirect_url;
                    } else {
                        const errorDiv = document.getElementById('otp_error');
                        if (errorDiv) {
                            if (response.message === 'کد تایید اشتباه است.') {
                                errorDiv.textContent = 'کد تایید اشتباه است.';
                            } else if (response.message === 'کد تایید منقضی شده است.') {
                                errorDiv.textContent = 'کد تایید منقضی شده است.';
                            } else {
                                errorDiv.textContent = response.message;
                            }
                        }
                    }
                } else {
                    const errorDiv = document.getElementById('otp_error');
                    if (errorDiv) {
                        errorDiv.textContent = 'خطایی رخ داد. لطفا مجددا تلاش کنید.';
                    }
                }
            };

            xhr.send(formData);
        });
    }
});
