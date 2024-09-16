import asyncio
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pyppeteer import launch

# Configuración de Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)


async def save_as_pdf(url, output_path):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle0'})
    await page.pdf({'path': output_path, 'format': 'A4'})
    await browser.close()


def navigate_and_click():
    try:
        # Navegar a la página web
        driver.get(
            "https://visortmo.com/library/manga/27892/mairimashitairumakun")

        # Intentar hacer clic en el capítulo 363.00
        try:
            chapter_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Capítulo 363.00"))
            )
            chapter_link.click()
            print("Capítulo 363.00 encontrado y clickeado.")
        except Exception as e:
            print(f"No se pudo hacer clic en el capítulo: {e}")

        # Intentar hacer clic en el icono del colapsable
        try:
            collapsible_icon = driver.find_element(
                By.CSS_SELECTOR, "#collapsible1136008 .col-2 .fas")
            collapsible_icon.click()
            print("Icono del colapsable encontrado y clickeado.")
        except Exception as e:
            print("No se pudo encontrar el icono del colapsable.")

        # Esperar a que se carguen las imágenes
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".img-container img"))
        )
        print("Imágenes cargadas.")

        # Desplazar hasta el final de la página
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        print("Desplazado hasta el final de la página.")

        # Esperar un momento adicional
        time.sleep(5)

        # Obtener la URL actual después de la navegación
        current_url = driver.current_url
        return current_url

    except Exception as e:
        print(f"Error durante la navegación: {e}")
        return None
    finally:
        driver.quit()


async def main():
    url = navigate_and_click()
    if url:
        await save_as_pdf(url, 'manga_chapter.pdf')
        print("PDF guardado como manga_chapter.pdf")
    else:
        print("No se pudo obtener la URL para guardar como PDF")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
