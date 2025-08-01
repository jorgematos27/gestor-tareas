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