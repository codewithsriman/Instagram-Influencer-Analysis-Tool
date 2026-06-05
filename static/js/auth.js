// Check authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    loadUserInfo();
});

function checkAuth() {
    const token = localStorage.getItem('token');
    
    if (!token && window.location.pathname === '/dashboard') {
        window.location.href = '/';
    }
}

function loadUserInfo() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (user.full_name) {
        document.getElementById('userName').textContent = user.full_name;
        document.getElementById('userEmail').textContent = user.email;
        
        // Set avatar initial
        const initial = user.full_name.charAt(0).toUpperCase();
        document.getElementById('userAvatar').textContent = initial;
    }
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/';
    }
}

function viewProfile() {
    alert('Profile page coming soon!');
    // In production, redirect to profile page
    // window.location.href = '/profile';
}

// Get auth token for API requests
function getAuthToken() {
    return localStorage.getItem('token');
}

// Add token to fetch requests
async function authenticatedFetch(url, options = {}) {
    const token = getAuthToken();
    
    if (!token) {
        window.location.href = '/';
        return;
    }
    
    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };
    
    const response = await fetch(url, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        alert('Session expired. Please login again.');
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/';
        return null;
    }
    
    return response;
}