// Mostrar nombre de usuario al cargar el dashboard
document.addEventListener('DOMContentLoaded', function() {
    const username = localStorage.getItem('currentUser');
    if (username) {
        document.getElementById('welcomeMessage').textContent = `¡Hola, ${username}!`;
    } else {
        window.location.href = 'index.html'; 
    }
});