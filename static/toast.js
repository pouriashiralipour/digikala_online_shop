document.addEventListener('DOMContentLoaded', (event) => {
    showToast();
});

function showToast() {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        toast.classList.add('show');
    });
}

function closeToast() {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        toast.classList.remove('show');
    });
}
