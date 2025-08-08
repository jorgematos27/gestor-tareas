from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Ruta a chromedriver.exe
service = Service('C:\\chromedriver\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

test_results = []

try:
    # Prueba 1: Eliminar tarea (camino feliz)
    print("Ejecutando Prueba 1: Eliminar tarea (camino feliz)")
    driver.get('http://localhost:8080/index.html')
    driver.find_element(By.ID, 'username').send_keys('testuser')
    driver.find_element(By.ID, 'password').send_keys('password123')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(2)  # Espera inicial
    driver.find_element(By.ID, 'taskTitle').send_keys('Tarea a Eliminar')
    driver.find_element(By.ID, 'taskDescription').send_keys('Descripción a Eliminar')
    driver.find_element(By.CSS_SELECTOR, '#taskForm button[type="submit"]').click()
    # Esperar a que los botones 'Eliminar' aparezcan
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn-danger')))
    buttons = driver.find_elements(By.CSS_SELECTOR, '.btn-danger')
    if not buttons:
        raise Exception("No se encontraron botones 'Eliminar' después de crear la tarea")
    initial_task_text = driver.find_element(By.ID, 'taskList').text
    assert 'Tarea a Eliminar' in initial_task_text, "La tarea no se creó correctamente"
    buttons[0].click()  # Hacer clic en el primer botón "Eliminar"
    time.sleep(3)  # Aumentar tiempo de espera después de eliminar
    new_task_text = driver.find_element(By.ID, 'taskList').text
    assert 'Tarea a Eliminar' not in new_task_text, "La tarea no se eliminó"
    print("Prueba 1 - Eliminar tarea (camino feliz): PASÓ")
    test_results.append({"test": "Eliminar tarea (camino feliz)", "status": "PASÓ"})

    # Prueba 2: Verificar actualización
    print("Ejecutando Prueba 2: Verificar actualización")
    # Crear otra tarea para verificar la actualización
    driver.find_element(By.ID, 'taskTitle').send_keys('Tarea Nueva')
    driver.find_element(By.ID, 'taskDescription').send_keys('Descripción Nueva')
    driver.find_element(By.CSS_SELECTOR, '#taskForm button[type="submit"]').click()
    # Esperar a que los botones 'Eliminar' aparezcan
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn-danger')))
    buttons = driver.find_elements(By.CSS_SELECTOR, '.btn-danger')
    if not buttons:
        raise Exception("No se encontraron botones 'Eliminar' después de crear la nueva tarea")
    initial_task_text = driver.find_element(By.ID, 'taskList').text
    assert 'Tarea Nueva' in initial_task_text, "La nueva tarea no se creó correctamente"
    buttons[0].click()  # Eliminar la tarea más reciente
    time.sleep(3)  # Aumentar tiempo de espera después de eliminar
    new_task_text = driver.find_element(By.ID, 'taskList').text
    assert 'Tarea Nueva' not in new_task_text, "La nueva tarea no se eliminó"
    # Verificar que no haya más tareas si la lista queda vacía
    task_items = driver.find_elements(By.TAG_NAME, 'li')
    if len(task_items) == 1 and 'No hay tareas para mostrar.' in new_task_text:
        print("La lista está vacía como esperado")
    else:
        assert len(task_items) == 0 or ('No hay tareas para mostrar.' in new_task_text), "La lista no se actualizó correctamente después de eliminar"
    print("Prueba 2 - Verificar actualización: PASÓ")
    test_results.append({"test": "Verificar actualización", "status": "PASÓ"})

except AssertionError as e:
    print(f"Prueba falló: {str(e)}")
    test_results.append({"test": "Eliminar tarea (camino feliz)" if len(test_results) == 0 else "Verificar actualización", "status": "FALLÓ", "error": str(e)})
except Exception as e:
    print(f"Error inesperado: {str(e)}")
    test_results.append({"test": "Eliminar tarea (camino feliz)" if len(test_results) == 0 else "Verificar actualización", "status": "FALLÓ", "error": str(e)})
finally:
    # Generar reporte HTML
    with open('test_results_delete_task.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html lang="es">\n<head>\n')
        f.write('<meta charset="UTF-8">\n<title>Resultado de Pruebas - Eliminar Tarea</title>\n')
        f.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">\n')
        f.write('</head>\n<body class="bg-light">\n')
        f.write('<div class="container mt-5">\n')
        f.write('<h1 class="text-center">Reporte de Pruebas - Eliminar Tarea</h1>\n')
        f.write('<table class="table table-striped">\n<thead><tr><th>Prueba</th><th>Estado</th><th>Detalles</th></tr></thead>\n<tbody>\n')
        for result in test_results:
            status_class = "text-success" if result["status"] == "PASÓ" else "text-danger"
            details = result.get("error", "Sin errores")
            f.write(f'<tr><td>{result["test"]}</td><td class="{status_class}">{result["status"]}</td><td>{details}</td></tr>\n')
        f.write('</tbody>\n</table>\n')
        f.write('</div>\n</body>\n</html>')
    print("Reporte generado in test_results_delete_task.html")
    driver.quit()
    print("Pruebas completadas")