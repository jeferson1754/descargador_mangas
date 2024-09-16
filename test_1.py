
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuración del WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Abrir el navegador maximizado
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Navegar a la página web
    driver.get("https://visortmo.com/library/manga/27892/mairimashitairumakun")
    
    try:
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
        
    except WebDriverException as e:
        # Manejar otros problemas con el WebDriver (como fallos de interacción)
        print("Error con el WebDriver durante la interacción:", e)

except (TimeoutException, WebDriverException) as e:
    # Manejar errores de acceso a la página (p. ej., si la página no responde)
    print("Error al acceder a la página:", e)

finally:
    # Cerrar el navegador
    driver.quit()
