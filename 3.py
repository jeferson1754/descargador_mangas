import time
import pdfkit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuración del WebDriver
chrome_options = Options()
# Ejecutar en modo headless para no mostrar la interfaz gráfica
chrome_options.add_argument("--headless")
# Añadir opciones para manejar SSL/TLS
chrome_options.add_argument('--ignore-certificate-errors')  # Ignorar errores de certificado
chrome_options.add_argument('--disable-web-security')  # Desactivar seguridad web
chrome_options.add_argument('--allow-insecure-localhost')  # Permitir conexiones inseguras a localhost

# Medir el tiempo de inicio
start_time = time.time()

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

def save_page_as_pdf(html_content):
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')  # Cambia esto a la ruta de tu ejecutable
    options = {
        'zoom': '1.3',  # Ajusta el nivel de zoom si es necesario
        'no-stop-slow-scripts': '',  # Evita detener scripts lentos
        'enable-local-file-access': ''  # Permite el acceso a archivos locales, si es necesario
    }
    try:
        pdfkit.from_string(html_content, 'output.pdf', configuration=config, options=options)
        print("Página guardada en output.pdf")
    except IOError as e:
        print("Error al guardar el PDF:", e)

try:
    # Navegar a la página web
    driver.get("https://visortmo.com/library/manga/27892/mairimashitairumakun")
    # Intentar hacer clic en el primer elemento de la lista
    try:
        first_item = driver.find_element(By.CSS_SELECTOR, ".list-group > .list-group-item:nth-child(1) > .px-2 .col-2")
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
        collapsible_icon = driver.find_element(By.CSS_SELECTOR, "#collapsible1136008 .col-2 .fas")
        collapsible_icon.click()
        print("Icono del colapsable encontrado y clickeado.")
    except NoSuchElementException:
        print("No se pudo encontrar el icono del colapsable.")

    # Esperar un momento para asegurar que el contenido se haya cargado
    time.sleep(5)

    # Desplazar hasta el final de la página para asegurar que todo el contenido se haya cargado
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Desplazado hasta el final de la página.")
    
    # Esperar para asegurar que el contenido se haya cargado
    time.sleep(5)  # Ajusta según sea necesario
    
    # Dentro de tu función main o donde sea necesario
    html_content = driver.page_source
    save_page_as_pdf(html_content)

except (TimeoutException, WebDriverException) as e:
    # Manejar errores de acceso a la página o problemas con el WebDriver
    print("Error al acceder a la página o con el WebDriver:", e)

finally:
    # Cerrar el navegador
    driver.quit()

# Medir el tiempo de fin
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tiempo de ejecución: {elapsed_time:.2f} segundos")