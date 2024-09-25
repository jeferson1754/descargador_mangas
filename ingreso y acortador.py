
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, urlunparse


def configurar_driver():
    """Configura y retorna el controlador de Selenium."""
    options = Options()
    options.add_argument("--headless")  # Ejecutar en segundo plano
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-web-security')
    options.add_argument("--window-size=1980,1080")
    options.add_argument('--allow-insecure-localhost')
    options.page_load_strategy = 'eager'
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def extraer_relevant_part(url):
    """Extrae la parte relevante de la URL original."""
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    return path_parts[2] if len(path_parts) > 2 else None

def ingresar_capitulo(link_manga, capitulo):
    """Ingresa al capítulo especificado de un manga y retorna la nueva URL."""
    driver = configurar_driver()
    new_url = None

    try:
        driver.get(link_manga)

        # Intentar hacer clic en el capítulo
        try:
            chapter_link = driver.find_element(By.LINK_TEXT, f"Capítulo {capitulo}.00")
            chapter_link.click()
            print(f"Capítulo {capitulo} encontrado y clickeado.")
        except NoSuchElementException:
            print(f"No se encontró el enlace al capítulo {capitulo}.")
            return new_url  # Salir si no se encuentra el capítulo

        # Encuentra todos los enlaces de capítulos
        chapter_links = driver.find_elements(By.CSS_SELECTOR, "a.btn-collapse")

        # Iterar sobre cada enlace para encontrar el correspondiente al capítulo
        collapsible_id = None
        for link in chapter_links:
            if f"Capítulo {capitulo}.00" in link.text:
                # Extraer el id del div correspondiente
                collapsible_id = link.get_attribute("onclick").split("'")[1]
                print(f"ID del div colapsable: {collapsible_id}")
                break
        else:
            print(f"No se encontró el enlace al capítulo {capitulo}.")
            return new_url

        # Buscar el div colapsable usando el ID extraído
        try:
            collapsible_div = driver.find_element(By.ID, collapsible_id)

            # Verificar si el div está visible
            if collapsible_div.is_displayed():
                print(f"El div con id '{collapsible_id}' está visible.")
                link_element = collapsible_div.find_element(By.CSS_SELECTOR, 'a.btn.btn-default.btn-sm')
                link_element.click()
                print("Clic en el enlace del capítulo realizado.")
            else:
                print(f"El div con id '{collapsible_id}' no está visible.")
        except NoSuchElementException:
            print("No se encontró el enlace del capítulo en el div colapsable.")
        except Exception as e:
            print("Ocurrió un error:", e)

        # Obtener la URL actual y construir la nueva URL
        current_url = driver.current_url
        relevant_part = extraer_relevant_part(current_url)

        if relevant_part:
            new_url = f"https://visortmo.com/viewer/{relevant_part}/cascade"
            print("URL original:", current_url)
            print("Nueva URL:", new_url)
        else:
            print("No se pudo extraer la parte relevante de la URL.")

    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print("Error al buscar los capítulos o con el WebDriver:", e)

    finally:
        driver.quit()  # Asegurarse de cerrar el navegador
        return new_url


if __name__ == "__main__":

    link_manga = "https://visortmo.com/library/manga/27892/mairimashitairumakun"
    capitulo = "362"  # Número del capítulo como variable

    nueva_url = ingresar_capitulo(link_manga, capitulo)

    if nueva_url:
        print("Nueva URL:", nueva_url)
