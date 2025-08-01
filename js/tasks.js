let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function renderTasks(filter = '') {
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';
    const filteredTasks = tasks.filter(task => 
        task.title.toLowerCase().includes(filter.toLowerCase()) ||
        task.description.toLowerCase().includes(filter.toLowerCase())
    );
    filteredTasks.forEach(task => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.innerHTML = `
            <h5>${task.title}</h5>
            <p>${task.description}</p>
            <button onclick="editTask(${task.id})" class="btn btn-sm btn-warning">Editar</button>
            <button onclick="deleteTask(${task.id})" class="btn btn-sm btn-danger">Eliminar</button>
        `;
        taskList.appendChild(li);
    });
}

// Añadir/Editar tarea
document.getElementById('taskForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const taskId = document.getElementById('taskId').value;
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;

    if (taskId) {
        // Editar
        const index = tasks.findIndex(task => task.id == taskId);
        tasks[index] = { id: taskId, title, description };
    } else {
        // Añadir
        tasks.push({ id: Date.now(), title, description });
    }
    saveTasks();
    renderTasks();
    this.reset();
});

// Función para buscar tareas
document.getElementById('searchInput').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const filteredTasks = tasks.filter(task => 
        task.title.toLowerCase().includes(searchTerm) || 
        task.description.toLowerCase().includes(searchTerm)
    );
    renderFilteredTasks(filteredTasks); // Llama a una función para mostrar resultados
});

// Muestra las tareas filtradas
function renderFilteredTasks(filteredTasks) {
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';
    filteredTasks.forEach(task => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        // Antes (en renderTasks):
li.innerHTML = `
    <h5>${task.title}</h5>
    <p>${task.description}</p>
`;

// Después (con fecha "arreglada"):
li.innerHTML = `
    <h5>${task.title}</h5>
    <p>${task.description}</p>
    <small>Fecha: ${new Date().toLocaleDateString()}</small>  // ¡Hotfix aplicado!
`;
        taskList.appendChild(li);
    });
}



function editTask(id) {
    const task = tasks.find(task => task.id == id);
    document.getElementById('taskId').value = task.id;
    document.getElementById('taskTitle').value = task.title;
    document.getElementById('taskDescription').value = task.description;
}

function deleteTask(id) {
    tasks = tasks.filter(task => task.id != id);
    saveTasks();
    renderTasks();
}

// Inicializar
renderTasks();