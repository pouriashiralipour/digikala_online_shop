document.addEventListener('DOMContentLoaded', function() {
    // فرم ثبت‌نام
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault(); // جلوگیری از ارسال پیش‌فرض فرم

            const formData = new FormData(registerForm);
            const xhr = new XMLHttpRequest();

            xhr.open('POST', registerForm.action);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

            xhr.onload = function() {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        // اضافه کردن تأخیر قبل از هدایت به صفحه تأیید
                        setTimeout(() => {
                            window.location.href = response.redirect_url;
                        }, 2000); // 2000 میلی‌ثانیه (2 ثانیه) تأخیر
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

    // فرم تأیید
    const verifyForm = document.getElementById('verify-form');
    if (verifyForm) {
        verifyForm.addEventListener('submit', function(event) {
            event.preventDefault(); // جلوگیری از ارسال پیش‌فرض فرم

            const formData = new FormData(verifyForm);
            const xhr = new XMLHttpRequest();

            xhr.open('POST', verifyForm.action);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

            xhr.onload = function() {
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
