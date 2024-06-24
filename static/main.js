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
                // Remove loading class after a delay matching your desired delay time
                setTimeout(() => {
                    button.classList.remove('loading');
                }, 2000); // 2000 milliseconds (2 seconds) delay (adjust as needed)

                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        setTimeout(() => {
                            window.location.href = response.redirect_url;
                        }, 2000); // 2 second delay before redirect (adjust as needed)
                    } else {
                        alert(response.message);
                    }
                } else {
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

            xhr.onload = function() {
                setTimeout(() => {
                    button.classList.remove('loading');
                }, 1000);

                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        window.location.href = response.redirect_url;
                    } else {
                        alert(response.message);
                    }
                } else {
                    alert('خطایی رخ داد.');
                }
            };

            xhr.send(formData);
        });
    }
});
