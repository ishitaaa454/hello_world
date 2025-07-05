// Toggle between login and signup forms
const showSignupLink = document.getElementById('show-signup');
const showLoginLink = document.getElementById('show-login');
const loginContainer = document.querySelector('.container');
const signupContainer = document.getElementById('signup-container');

if (showSignupLink) {
    showSignupLink.addEventListener('click', (e) => {
        e.preventDefault();
        loginContainer.style.display = 'none';
        signupContainer.style.display = 'block';
    });
}

if (showLoginLink) {
    showLoginLink.addEventListener('click', (e) => {
        e.preventDefault();
        signupContainer.style.display = 'none';
        loginContainer.style.display = 'block';
    });
}

// Login form handler
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const res = await fetch('/api/signin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('username', username);
            window.location.href = '/home';
        } else {
            document.getElementById('error').textContent = data.error || 'Sign in failed';
        }
    });
}

// Signup form handler
const signupForm = document.getElementById('signup-form');
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('signup-username').value;
        const password = document.getElementById('signup-password').value;
        const res = await fetch('/api/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            document.getElementById('signup-error').textContent = 'Account created! You can now sign in.';
            document.getElementById('signup-error').style.color = 'green';
            // Clear form
            document.getElementById('signup-username').value = '';
            document.getElementById('signup-password').value = '';
        } else {
            document.getElementById('signup-error').textContent = data.error || 'Sign up failed';
            document.getElementById('signup-error').style.color = 'red';
        }
    });
}

// Sign out handler
const signoutBtn = document.getElementById('signout-btn');
if (signoutBtn) {
    signoutBtn.addEventListener('click', async () => {
        const token = localStorage.getItem('token');
        await fetch('/api/signout', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token
            }
        });
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = '/';
    });
} 