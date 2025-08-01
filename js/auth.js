document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    localStorage.setItem('currentUser', username); 
    window.location.href = 'dashboard.html'; 
});


if (window.location.pathname.includes('dashboard.html')) {
    const username = localStorage.getItem('currentUser');
    document.getElementById('welcomeMessage').textContent = `¡Hola, ${username}!`;
}

// Mostrar nombre de usuario al cargar el dashboard
document.addEventListener('DOMContentLoaded', function() {
    const username = localStorage.getItem('currentUser');
    if (username) {
        document.getElementById('welcomeMessage').textContent = `¡Hola, ${username}!`;
    } else {
        window.location.href = 'index.html'; 
    }
});