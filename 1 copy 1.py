import time
import pdfkit 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

# Configuración del WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def save_page_as_pdf(html_content, output_path='manga_chapter.pdf'):
    """
    Guarda el contenido HTML en un archivo PDF, asegurándose de que todas las imágenes se carguen correctamente.
    
    :param html_content: Contenido HTML a guardar en el PDF.
    :param output_path: Ruta del archivo PDF de salida. Por defecto es 'manga_chapter.pdf'.
    """
    # Configuración de pdfkit con la ruta al ejecutable wkhtmltopdf
    wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    if not os.path.isfile(wkhtmltopdf_path):
        raise FileNotFoundError(f"El archivo wkhtmltopdf no se encuentra en la ruta: {wkhtmltopdf_path}")
    
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    
    options = {
        'javascript-delay': '3000',  # Espera 3 segundos para JavaScript
        'no-stop-slow-scripts': '',  # Permitir scripts lentos
        'enable-local-file-access': '',  # Permitir acceso a archivos locales
        'disable-smart-shrinking': ''  # Evita la reducción automática de tamaño
    }
    
    try:
        # Generar el archivo PDF a partir del contenido HTML
        pdfkit.from_string(html_content, output_path, configuration=config, options=options)
        print(f"Página guardada en {output_path}")
    except pdfkit.PDFKitException as e:
        print("Error al procesar el HTML con pdfkit:", e)
    except Exception as e:
        print("Error inesperado al guardar el PDF:", e)




try:
    # Navegar a la página web
    driver.get("https://visortmo.com/library/manga/27892/mairimashitairumakun")

    # Intentar hacer clic en el capítulo 363.00
    try:
        chapter_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Capítulo 363.00"))
        )
        chapter_link.click()
        print("Capítulo 363.00 encontrado y clickeado.")
    except TimeoutException:
        print("No se encontró el enlace al capítulo 363.00 o no se pudo hacer clic en él.")

    # Intentar hacer clic en el icono del colapsable
    try:
        collapsible_icon = driver.find_element(
            By.CSS_SELECTOR, "#collapsible1136008 .col-2 .fas")
        collapsible_icon.click()
        print("Icono del colapsable encontrado y clickeado.")
    except NoSuchElementException:
        print("No se pudo encontrar el icono del colapsable.")
        
    time.sleep(5)
    # Esperar a que se carguen las imágenes
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".img-container img"))
        )
        print("Imágenes cargadas.")
    except TimeoutException:
        print("Tiempo de espera agotado al cargar las imágenes.")

    
    # Desplazar hasta el final de la página para asegurar que todo el contenido se haya cargado
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Desplazado hasta el final de la página.")


    # Obtener el contenido HTML de la página
    html_content = driver.page_source

    # Guardar la página como PDF
    save_page_as_pdf(html_content)

except (TimeoutException, WebDriverException) as e:
    print("Error al acceder a la página o con el WebDriver:", e)

finally:
    # Cerrar el navegador
    driver.quit()
