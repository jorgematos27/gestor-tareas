from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Ruta a chromedriver.exe
service = Service('C:\\chromedriver\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

test_results = []

try:
    # Prueba 1: Editar tarea (camino feliz)
    print("Ejecutando Prueba 1: Editar tarea (camino feliz)")
    driver.get('http://localhost:8080/index.html')
    driver.find_element(By.ID, 'username').send_keys('testuser')
    driver.find_element(By.ID, 'password').send_keys('password123')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(2)  # Aumentar tiempo de espera
    driver.find_element(By.ID, 'taskTitle').send_keys('Tarea Inicial')
    driver.find_element(By.ID, 'taskDescription').send_keys('Descripción Inicial')
    driver.find_element(By.CSS_SELECTOR, '#taskForm button[type="submit"]').click()
    time.sleep(2)  # Aumentar tiempo de espera
    buttons = driver.find_elements(By.CSS_SELECTOR, '.btn-warning')
    if not buttons:
        raise Exception("No se encontraron botones 'Editar' después de crear la tarea")
    buttons[0].click()  # Hacer clic en el primer botón "Editar"
    time.sleep(2)  # Aumentar tiempo de espera
    driver.find_element(By.ID, 'taskTitle').clear()
    driver.find_element(By.ID, 'taskTitle').send_keys('Tarea Editada')
    driver.find_element(By.ID, 'taskDescription').clear()
    driver.find_element(By.ID, 'taskDescription').send_keys('Descripción Editada')
    driver.find_element(By.CSS_SELECTOR, '#taskForm button[type="submit"]').click()
    time.sleep(2)  # Aumentar tiempo de espera
    task_list = driver.find_element(By.ID, 'taskList')
    assert 'Tarea Editada' in task_list.text, "La tarea no se editó correctamente"
    print("Prueba 1 - Editar tarea (camino feliz): PASÓ")
    test_results.append({"test": "Editar tarea (camino feliz)", "status": "PASÓ"})

    # Prueba 2: Intentar editar con título vacío
    print("Ejecutando Prueba 2: Editar tarea con título vacío")
    buttons = driver.find_elements(By.CSS_SELECTOR, '.btn-warning')
    if not buttons:
        raise Exception("No se encontraron botones 'Editar' para la segunda prueba")
    buttons[0].click()  # Hacer clic en el primer botón "Editar" nuevamente
    time.sleep(2)  # Aumentar tiempo de espera
    driver.find_element(By.ID, 'taskTitle').clear()
    driver.find_element(By.ID, 'taskTitle').send_keys('')
    driver.find_element(By.ID, 'taskDescription').clear()
    driver.find_element(By.ID, 'taskDescription').send_keys('Descripción Nueva')
    driver.find_element(By.CSS_SELECTOR, '#taskForm button[type="submit"]').click()
    time.sleep(2)  # Aumentar tiempo de espera
    error_message = driver.find_elements(By.CLASS_NAME, 'text-danger')
    assert len(error_message) > 0, "No se mostró mensaje de error para título vacío al editar"
    assert 'Tarea Editada' in driver.find_element(By.ID, 'taskList').text, "La tarea se modificó inesperadamente"
    print("Prueba 2 - Editar tarea con título vacío: PASÓ")
    test_results.append({"test": "Editar tarea con título vacío", "status": "PASÓ"})

except AssertionError as e:
    print(f"Prueba falló: {str(e)}")
    test_results.append({"test": "Editar tarea (camino feliz)" if len(test_results) == 0 else "Editar tarea con título vacío", "status": "FALLÓ", "error": str(e)})
except Exception as e:
    print(f"Error inesperado: {str(e)}")
    test_results.append({"test": "Editar tarea (camino feliz)" if len(test_results) == 0 else "Editar tarea con título vacío", "status": "FALLÓ", "error": str(e)})
finally:
    # Generar reporte HTML
    with open('test_results_edit_task.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html lang="es">\n<head>\n')
        f.write('<meta charset="UTF-8">\n<title>Resultado de Pruebas - Editar Tarea</title>\n')
        f.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">\n')
        f.write('</head>\n<body class="bg-light">\n')
        f.write('<div class="container mt-5">\n')
        f.write('<h1 class="text-center">Reporte de Pruebas - Editar Tarea</h1>\n')
        f.write('<table class="table table-striped">\n<thead><tr><th>Prueba</th><th>Estado</th><th>Detalles</th></tr></thead>\n<tbody>\n')
        for result in test_results:
            status_class = "text-success" if result["status"] == "PASÓ" else "text-danger"
            details = result.get("error", "Sin errores")
            f.write(f'<tr><td>{result["test"]}</td><td class="{status_class}">{result["status"]}</td><td>{details}</td></tr>\n')
        f.write('</tbody>\n</table>\n')
        f.write('</div>\n</body>\n</html>')
    print("Reporte generado in test_results_edit_task.html")
    driver.quit()
    print("Pruebas completadas")