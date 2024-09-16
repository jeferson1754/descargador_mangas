import asyncio
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pyppeteer import launch


# Configuración del WebDriver
chrome_options = Options()
# Ejecutar en modo headless para no mostrar la interfaz gráfica
chrome_options.add_argument("--headless")



driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)


async def guardar_como_pdf(contenido_html, ruta_salida):
    navegador = await launch(headless=True)  # O usa executablePath si es necesario
    pagina = await navegador.newPage()
    await pagina.setContent(contenido_html)
    
    # Espera a que el <body> esté presente
    await pagina.waitForSelector('body')
    
    await pagina.pdf({'path': ruta_salida, 'format': 'A4'})
    await navegador.close()


async def main():
    try:
        # Navegar a la página web
        driver.get(
            "https://visortmo.com/library/manga/27892/mairimashitairumakun")

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

        # Esperar un momento para asegurar que el contenido se haya cargado
        time.sleep(5)

        # Desplazar hasta el final de la página para asegurar que todo el contenido se haya cargado
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        print("Desplazado hasta el final de la página.")

        # Dentro de tu función main o donde sea necesario
        contenido_html = driver.page_source
        await guardar_como_pdf(contenido_html, 'salida.pdf')
        print("PDF generado con éxito.")

    except (TimeoutException, WebDriverException) as e:
        print("Error al acceder a la página o con el WebDriver:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
