
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, urlunparse

# Configuración del WebDriver
chrome_options = Options()
# Ejecutar en modo headless para no mostrar la interfaz gráfica
chrome_options.add_argument("--headless")
# Añadir opciones para manejar SSL/TLS
# Ignorar errores de certificado
chrome_options.add_argument('--ignore-certificate-errors')
# Desactivar seguridad web
chrome_options.add_argument('--disable-web-security')
# Permitir conexiones inseguras a localhost
chrome_options.add_argument('--allow-insecure-localhost')


driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

try:
    # Navegar a la página web
    driver.get("https://visortmo.com/library/manga/27892/mairimashitairumakun")

    # Intentar hacer clic en el primer elemento de la lista
    try:
        first_item = driver.find_element(
            By.CSS_SELECTOR, ".list-group > .list-group-item:nth-child(1) > .px-2 .col-2")
        first_item.click()
        print("Primer elemento de la lista encontrado y clickeado.")
    except NoSuchElementException:
        print("No se pudo encontrar el primer elemento en la lista.")

    # Intentar hacer clic en el capítulo 363.00
    try:
        chapter_link = driver.find_element(By.LINK_TEXT, "Capítulo 363.00")
        chapter_link.click()
        print("Capítulo 363.00 encontrado y clickeado.")
    except NoSuchElementException:
        print("No se encontró el enlace al capítulo 363.00.")

    # Intentar hacer clic en el icono del colapsable
    try:
        collapsible_icon = driver.find_element(
            By.CSS_SELECTOR, "#collapsible1136008 .col-2 .fas")
        collapsible_icon.click()
        print("Icono del colapsable encontrado y clickeado.")
    except NoSuchElementException:
        print("No se pudo encontrar el icono del colapsable.")

    # Obtener y mostrar la URL actual de la página
    current_url = driver.current_url

    # URL original
    original_url = current_url

    # Parsear la URL
    parsed_url = urlparse(original_url)

    # Extraer la parte relevante después de /news/
    path_parts = parsed_url.path.split('/')
    if len(path_parts) > 2:
        relevant_part = path_parts[2]  # '05f6661521a5c6c37c9d7a0a09df1dec'

    # Construir la nueva URL
    new_url = f"https://visortmo.com/viewer/{relevant_part}/cascade"

    print("URL original:", original_url)
    print("Nueva URL:", new_url)

except (TimeoutException, WebDriverException) as e:
    # Manejar errores de acceso a la página o problemas con el WebDriver
    print("Error al acceder a la página o con el WebDriver:", e)

finally:
    # Cerrar el navegador
    driver.quit()
