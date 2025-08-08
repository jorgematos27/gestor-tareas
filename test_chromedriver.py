from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service('C:\\chromedriver\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get('http://www.google.com')
print('Página cargada:', driver.title)

driver.quit()