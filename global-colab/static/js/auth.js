// Authentication JavaScript

function showLogin() {
    document.getElementById('loginForm').classList.add('active');
    document.getElementById('registerForm').classList.remove('active');
    document.querySelectorAll('.tab-btn')[0].classList.add('active');
    document.querySelectorAll('.tab-btn')[1].classList.remove('active');
}

function showRegister() {
    document.getElementById('registerForm').classList.add('active');
    document.getElementById('loginForm').classList.remove('active');
    document.querySelectorAll('.tab-btn')[1].classList.add('active');
    document.querySelectorAll('.tab-btn')[0].classList.remove('active');
}

async function handleLogin(event) {
    event.preventDefault();
    
    const formData = {
        email: document.getElementById('loginEmail').value,
        password: document.getElementById('loginPassword').value
    };
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Redirect to dashboard
            window.location.href = '/dashboard';
        } else {
            showAlert('error', data.error || 'Login failed');
        }
    } catch (error) {
        showAlert('error', 'An error occurred. Please try again.');
        console.error('Login error:', error);
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const formData = {
        username: document.getElementById('regUsername').value,
        email: document.getElementById('regEmail').value,
        full_name: document.getElementById('regFullName').value,
        password: document.getElementById('regPassword').value,
        country: document.getElementById('regCountry').value,
        language: document.getElementById('regLanguage').value,
        skills: document.getElementById('regSkills').value,
        interests: document.getElementById('regInterests').value
    };
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('success', 'Registration successful! Redirecting...');
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1500);
        } else {
            showAlert('error', data.error || 'Registration failed');
        }
    } catch (error) {
        showAlert('error', 'An error occurred. Please try again.');
        console.error('Registration error:', error);
    }
}

function showAlert(type, message) {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    // Insert alert
    const authContainer = document.getElementById('authContainer');
    authContainer.insertBefore(alertDiv, authContainer.firstChild);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

