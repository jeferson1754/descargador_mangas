import asyncio
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from pyppeteer import launch

# Configuración de Selenium WebDriver
chrome_options = Options()
# Comentamos esta línea para modo no headless
chrome_options.add_argument("--headless")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)


async def save_as_pdf(url, output_path):
    # Cambiado a False para modo no headless
    browser = await launch(headless=False, args=['--no-sandbox'])
    try:
        page = await browser.newPage()
        await page.setViewport({'width': 1920, 'height': 1080})
        print(f"Navegando a: {url}")
        await page.goto(url, {'waitUntil': 'networkidle0', 'timeout': 60000})
        print("Página cargada en Pyppeteer")
        await page.pdf({'path': output_path, 'format': 'A4', 'printBackground': True})
        print(f"PDF guardado en: {output_path}")
        await browser.close()
    except Exception as e:
        print(f"Error en save_as_pdf: {e}")
    finally:
        await browser.close()


def navigate_and_click():
    global driver
    try:
        driver.get(
            "https://visortmo.com/library/manga/27892/mairimashitairumakun")
        print("Página inicial cargada")

        # Esperar y hacer clic en el capítulo 363.00
        chapter_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Capítulo 363.00"))
        )
        chapter_link.click()
        print("Capítulo 363.00 encontrado y clickeado.")

        # Esperar y hacer clic en el capítulo 363.00
        sub_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#collapsible1136008 .col-2 .fas"))
        )
        sub_link.click()
        print("Icono del colapsable encontrado y clickeado.")

        # Esperar a que se carguen las imágenes
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "#chapter-container img"))
        )
        print("Imágenes cargadas.")

        # Desplazar hasta el final de la página
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        print("Desplazado hasta el final de la página.")

        time.sleep(10)  # Esperar más tiempo para asegurar la carga completa

        current_url = driver.current_url
        print(f"URL actual: {current_url}")
        
        return current_url

    except TimeoutException as e:
        print(f"Tiempo de espera excedido: {e}")
    except NoSuchElementException as e:
        print(f"Elemento no encontrado: {e}")
    except WebDriverException as e:
        print(f"Error del WebDriver: {e}")
    except Exception as e:
        print(f"Error inesperado durante la navegación: {e}")
    finally:
        if driver:
            print("Cerrando el navegador de Selenium")
            driver.quit()
    return None


async def main():
    url = navigate_and_click()
    if url:
        try:
            await save_as_pdf(url, 'manga_chapter.pdf')
            print("Proceso completado. PDF guardado como manga_chapter.pdf")
        except Exception as e:
            print(f"Error al guardar PDF: {e}")
    else:
        print("No se pudo obtener la URL para guardar como PDF")

if __name__ == "__main__":
    asyncio.run(main())
