from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json

# Ruta a chromedriver.exe
service = Service('C:\\chromedriver\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

test_results = []

try:
    print("Ejecutando pruebas de mostrar tareas...")
    driver.get('http://localhost:8080/index.html')
    time.sleep(1)

    # Iniciar sesión
    driver.find_element(By.ID, 'username').send_keys('testuser')
    driver.find_element(By.ID, 'password').send_keys('password123')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(1)

    # Limpiar localStorage antes de continuar
    driver.execute_script("localStorage.setItem('tasks', '[]');")
    time.sleep(0.5)
    driver.refresh()
    time.sleep(1)

    # Crear tarea
    driver.find_element(By.ID, 'taskTitle').send_keys('Tarea a Mostrar')
    driver.find_element(By.ID, 'taskDescription').send_keys('Descripción a Mostrar')
    driver.find_element(By.CSS_SELECTOR, '#taskForm button[type="submit"]').click()
    time.sleep(1)

    # Verificar que la tarea esté en la lista
    task_list = driver.find_element(By.ID, 'taskList')
    assert 'Tarea a Mostrar' in task_list.text, "La tarea no se mostró correctamente"
    print("✅ Prueba 1 - Mostrar tareas: PASÓ")
    test_results.append({"test": "Mostrar tarea (camino feliz)", "status": "PASÓ"})

    # Eliminar solo la tarea específica
    task_items = driver.find_elements(By.CSS_SELECTOR, '#taskList li')
    for item in task_items:
        if 'Tarea a Mostrar' in item.text:
            item.find_element(By.CSS_SELECTOR, '.btn-danger').click()
            time.sleep(0.5)
            break

    time.sleep(1)

    # Verificar que aparezca el mensaje de lista vacía
    task_list = driver.find_element(By.ID, 'taskList')
    assert 'No hay tareas para mostrar.' in task_list.text, "No se mostró el mensaje de lista vacía"
    print("✅ Prueba 2 - Lista vacía: PASÓ")
    test_results.append({"test": "Lista vacía", "status": "PASÓ"})

except AssertionError as e:
    print(f"❌ Prueba falló: {str(e)}")
    test_results.append({"test": "Error de prueba", "status": "FALLÓ", "error": str(e)})
except Exception as e:
    print(f"❌ Error inesperado: {str(e)}")
    test_results.append({"test": "Error inesperado", "status": "FALLÓ", "error": str(e)})
finally:
    # Generar reporte
    with open('test_results_show_tasks.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html lang="es">\n<head>\n')
        f.write('<meta charset="UTF-8">\n<title>Resultado de Pruebas - Mostrar Tareas</title>\n')
        f.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">\n')
        f.write('</head>\n<body class="bg-light">\n')
        f.write('<div class="container mt-5">\n')
        f.write('<h1 class="text-center">Reporte de Pruebas - Mostrar Tareas</h1>\n')
        f.write('<table class="table table-striped">\n<thead><tr><th>Prueba</th><th>Estado</th><th>Detalles</th></tr></thead>\n<tbody>\n')
        for result in test_results:
            status_class = "text-success" if result["status"] == "PASÓ" else "text-danger"
            details = result.get("error", "Sin errores")
            f.write(f'<tr><td>{result["test"]}</td><td class="{status_class}">{result["status"]}</td><td>{details}</td></tr>\n')
        f.write('</tbody>\n</table>\n')
        f.write('</div>\n</body>\n</html>')
    print("📄 Reporte generado en test_results_show_tasks.html")
    driver.quit()
    print("✅ Pruebas completadas")
