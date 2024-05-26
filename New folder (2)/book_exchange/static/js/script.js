/* static/js/script.js */
document.addEventListener('DOMContentLoaded', () => {
    const bookForm = document.getElementById('book-form');
    if (bookForm) {
        bookForm.addEventListener('submit', addBook);
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', loginUser);
    }

    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', processPayment);
    }
});

function addBook(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    fetch('/catalog', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Failed to add book');
        }
    });
}

function loginUser(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    fetch('/login', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            window.location.href = '/catalog';
        } else {
            alert('Login failed');
        }
    });
}

function processPayment(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    fetch('/payment', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            alert('Payment successful!');
            window.location.href = '/';
        } else {
            alert('Payment failed');
        }
    });
}
