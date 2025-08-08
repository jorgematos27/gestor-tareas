from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Ruta a chromedriver.exe
service = Service('C:\\chromedriver\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

test_results = []

try:
    # Prueba 1: Login exitoso
    print("Ejecutando Prueba 1: Login exitoso")
    driver.get('http://localhost:8080/index.html')
    driver.find_element(By.ID, 'username').send_keys('testuser')
    driver.find_element(By.ID, 'password').send_keys('password123')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(1)
    assert 'dashboard.html' in driver.current_url
    print("Prueba 1 - Login exitoso: PASÓ")
    test_results.append({"test": "Login exitoso", "status": "PASÓ"})

    # Regresar a index.html para la siguiente prueba
    driver.get('http://localhost:8080/index.html')

    # Prueba 2: Campos vacíos
    print("Ejecutando Prueba 2: Campos vacíos")
    driver.find_element(By.ID, 'username').clear()
    driver.find_element(By.ID, 'password').clear()
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(1)
    assert 'index.html' in driver.current_url or 'dashboard.html' not in driver.current_url
    error_message = driver.find_elements(By.CLASS_NAME, 'text-danger')
    assert len(error_message) > 0, "No se mostró mensaje de error para campos vacíos"
    print("Prueba 2 - Campos vacíos: PASÓ")
    test_results.append({"test": "Campos vacíos", "status": "PASÓ"})

except AssertionError as e:
    print(f"Prueba falló: {str(e)}")
    test_results.append({"test": "Login exitoso" if len(test_results) == 0 else "Campos vacíos", "status": "FALLÓ", "error": str(e)})
except Exception as e:
    print(f"Error inesperado: {str(e)}")
    test_results.append({"test": "Login exitoso" if len(test_results) == 0 else "Campos vacíos", "status": "FALLÓ", "error": str(e)})
finally:
    # Generar reporte HTML
    with open('test_results.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html lang="es">\n<head>\n')
        f.write('<meta charset="UTF-8">\n<title>Resultado de Pruebas - Gestor de Tareas</title>\n')
        f.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">\n')
        f.write('</head>\n<body class="bg-light">\n')
        f.write('<div class="container mt-5">\n')
        f.write('<h1 class="text-center">Reporte de Pruebas Automatizadas</h1>\n')
        f.write('<table class="table table-striped">\n<thead><tr><th>Prueba</th><th>Estado</th><th>Detalles</th></tr></thead>\n<tbody>\n')
        for result in test_results:
            status_class = "text-success" if result["status"] == "PASÓ" else "text-danger"
            details = result.get("error", "Sin errores")
            f.write(f'<tr><td>{result["test"]}</td><td class="{status_class}">{result["status"]}</td><td>{details}</td></tr>\n')
        f.write('</tbody>\n</table>\n')
        f.write('</div>\n</body>\n</html>')
    print("Reporte generado en test_results.html")

    driver.quit()
    print("Pruebas completadas")