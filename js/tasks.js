let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function renderTaskItems(tasksToRender) {
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';
    if (tasksToRender.length === 0) {
        const li = document.createElement('li');
        li.className = 'list-group-item text-muted';
        li.textContent = 'No hay tareas para mostrar.';
        taskList.appendChild(li);
    } else {
        tasksToRender.forEach(task => {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.innerHTML = `
                <h5>${task.title}</h5>
                <p>${task.description}</p>
                <small>Fecha: ${new Date(task.createdAt).toLocaleDateString()}</small>
                <button onclick="editTask(${task.id})" class="btn btn-sm btn-warning ms-2">Editar</button>
                <button onclick="deleteTask(${task.id})" class="btn btn-sm btn-danger ms-2">Eliminar</button>
            `;
            taskList.appendChild(li);
        });
    }
}

function renderTasks(filter = '') {
    const filteredTasks = tasks.filter(task => 
        task.title.toLowerCase().includes(filter.toLowerCase()) ||
        task.description.toLowerCase().includes(filter.toLowerCase())
    );
    renderTaskItems(filteredTasks);
}

// Añadir/Editar tarea
document.getElementById('taskForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const taskId = document.getElementById('taskId').value;
    const title = document.getElementById('taskTitle').value.trim();
    const description = document.getElementById('taskDescription').value.trim();

    // Validar título vacío
    if (!title) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'text-danger text-center mt-3';
        errorDiv.textContent = 'El título no puede estar vacío.';
        document.querySelector('#taskForm').appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 3000);
        return;
    }

    if (taskId) {
        // Editar
        const index = tasks.findIndex(task => task.id == taskId);
        tasks[index] = { id: taskId, title, description, createdAt: tasks[index].createdAt };
    } else {
        // Añadir
        tasks.push({ id: Date.now(), title, description, createdAt: Date.now() });
    }
    saveTasks();
    renderTasks(document.getElementById('searchInput').value);
    this.reset();
    document.getElementById('taskId').value = '';
});

// Función para buscar tareas
document.getElementById('searchInput').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    renderTasks(searchTerm);
});

// Funciones de edición y eliminación
function editTask(id) {
    const task = tasks.find(task => task.id == id);
    document.getElementById('taskId').value = task.id;
    document.getElementById('taskTitle').value = task.title;
    document.getElementById('taskDescription').value = task.description;
}

function deleteTask(id) {
    tasks = tasks.filter(task => task.id != id);
    saveTasks();
    renderTasks(document.getElementById('searchInput').value);
}

// Inicializar y mostrar nombre de usuario
document.addEventListener('DOMContentLoaded', function() {
    const username = localStorage.getItem('currentUser');
    if (username) {
        document.getElementById('welcomeMessage').textContent = `¡Hola, ${username}!`;
    } else {
        window.location.href = 'index.html'; 
    }
    renderTasks(); // Renderizar tareas al cargar
});