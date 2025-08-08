document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    // Validar campos vacíos
    if (!username || !password) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'text-danger text-center mt-3';
        errorDiv.textContent = 'Por favor, completa todos los campos.';
        document.querySelector('#loginForm').appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 3000); // Elimina el mensaje después de 3 segundos
        return;
    }

    localStorage.setItem('currentUser', username);
    window.location.href = 'dashboard.html';
});