document.addEventListener('DOMContentLoaded', function() {
    function clearLoadingState() {
        // Clear loading class on specific buttons on page load
        const registerSubmitButton = document.querySelector('#register-form button[type="submit"]');
        const verifySubmitButton = document.querySelector('#verify-form button[type="submit"]');

        if (registerSubmitButton) {
            registerSubmitButton.classList.remove('loading');
        }

        if (verifySubmitButton) {
            verifySubmitButton.classList.remove('loading');
        }
    }

    // Clear loading state on initial page load
    clearLoadingState();

    // Clear loading state when the page is shown (e.g., when navigating back to it)
    window.addEventListener('pageshow', function(event) {
        clearLoadingState();
    });

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

            // Validate phone number
            if (!isValidPhoneNumber(phoneNumber)) {
                const errorDiv = document.getElementById('phone_number_error');
                if (errorDiv) {
                    errorDiv.textContent = 'شماره موبایل را به درستی وارد کنید';
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

            // Validate OTP
            if (!isValidOTP(otp)) {
                const errorDiv = document.getElementById('otp_error');
                if (errorDiv) {
                    errorDiv.textContent = 'کد تایید را به درستی وارد کنید';
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

        const resendCodeLink = document.getElementById('resend-code-link');
        if (resendCodeLink) {
            resendCodeLink.addEventListener('click', function(event) {
                event.preventDefault();

                // Clear previous errors
                document.querySelectorAll('.error').forEach(function(errorDiv) {
                    errorDiv.textContent = '';
                });

                const resendMessage = document.getElementById('resend_message');
                if (resendMessage) {
                    resendMessage.textContent = '';
                }

                const xhr = new XMLHttpRequest();
                xhr.open('POST', resendCodeLink.href);
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

                xhr.onload = function() {
                    const resendMessage = document.getElementById('resend_message');
                    if (xhr.status === 200) {
                        const response = JSON.parse(xhr.responseText);
                        if (response.success) {
                            resendMessage.textContent = 'کد تایید مجدداً ارسال شد.';
                            setTimeout(() => {
                                resendMessage.textContent = '';
                            }, 3000); // Clear message after 3 seconds
                            resetTimer();
                        } else {
                            resendMessage.textContent = 'ارسال مجدد کد ناموفق بود.';
                        }
                    } else {
                        resendMessage.textContent = 'خطایی رخ داد.';
                    }
                };

                xhr.send();
            });

            const timer = document.getElementById('timer--verify-code');
            if (timer) {
                let minutesLeft = parseInt(timer.getAttribute('data-minutes-left'), 10);
                let endTime = Date.now() + minutesLeft * 60000;

                function updateTimer() {
                    const now = Date.now();
                    const timeLeft = Math.max(0, endTime - now);

                    const minutes = Math.floor(timeLeft / 60000);
                    const seconds = Math.floor((timeLeft % 60000) / 1000);

                    timer.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

                    if (timeLeft > 0) {
                        requestAnimationFrame(updateTimer);
                    } else {
                        timer.style.display = 'none';
                        resendCodeLink.style.display = 'inline';
                    }
                }

                function resetTimer() {
                    minutesLeft = 2; // Set the countdown time in minutes
                    endTime = Date.now() + minutesLeft * 60000;
                    timer.style.display = 'inline';
                    resendCodeLink.style.display = 'none';
                    updateTimer();
                }

                updateTimer();
            }
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to validate phone number (only digits allowed)
    function isValidPhoneNumber(phoneNumber) {
        return /^\d{11}$/.test(phoneNumber); // 11 digits validation
    }

    // Function to validate OTP (only digits allowed)
    function isValidOTP(otp) {
        return /^\d{4}$/.test(otp); // 4 digits validation
    }
});
