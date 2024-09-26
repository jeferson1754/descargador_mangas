from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from PIL import Image
import os
from io import BytesIO

Image.MAX_IMAGE_PIXELS = None

def configurar_driver(ancho, alto):
    """Configura y retorna el controlador de Selenium."""
    options = Options()
    options.add_argument("--headless")  # Ejecutar en segundo plano
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-web-security')
    options.add_argument(f"--window-size={ancho},{alto}")
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
    driver = configurar_driver(ancho=200, alto=300)
    new_url = None

    try:
        driver.get(link_manga)

        # Intentar hacer clic en el capítulo
        try:
            chapter_link = driver.find_element(
                By.LINK_TEXT, f"Capítulo {capitulo}.00")
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
                link_element = collapsible_div.find_element(
                    By.CSS_SELECTOR, 'a.btn.btn-default.btn-sm')
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
            # print("Nueva URL:", new_url)
        else:
            print("No se pudo extraer la parte relevante de la URL.")

    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print("Error al buscar los capítulos o con el WebDriver:", e)

    finally:
        driver.quit()  # Asegurarse de cerrar el navegador
        return new_url


def desplazamiento_paginas(driver, pause_time=1, scroll_increment=500, max_same_height=15):
    """Desplaza suavemente hacia abajo en la página completa."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    same_height_count = 0
    total_scrolls = 0

    print("Comenzando desplazamiento...")

    while same_height_count < max_same_height:
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        total_scrolls += 1

        print(f"Desplazamiento {total_scrolls}: {scroll_increment}px. "
              f"Nueva altura: {new_height}px. Anterior: {last_height}px.")

        if new_height == last_height:
            same_height_count += 1
            print(f"Altura repetida: {same_height_count}/{max_same_height}")
        else:
            same_height_count = 0
            last_height = new_height

    print(f"Desplazamiento completo. Total de scrolls: {total_scrolls}")


def desplazamiento_paginas_y_capturas(driver, file_name, pause_time=1, scroll_increment=500, max_same_height=15):
    """Desplaza suavemente hacia abajo en la página completa y captura capturas de pantalla por secciones."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    same_height_count = 0
    total_scrolls = 0
    total_height = last_height

    # Lista para almacenar las capturas por secciones
    capturas = []

    print("Comenzando desplazamiento y captura de pantalla...")

    while same_height_count < max_same_height:
        # Captura la sección visible actual
        screenshot = driver.get_screenshot_as_png()
        capturas.append(Image.open(BytesIO(screenshot)))

        # Desplazar hacia abajo
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(pause_time)

        # Verificar nueva altura de la página
        new_height = driver.execute_script("return document.body.scrollHeight")
        total_scrolls += 1

        print(f"Desplazamiento {total_scrolls}: {scroll_increment}px. "
              f"Nueva altura: {new_height}px. Anterior: {last_height}px.")

        if new_height == last_height:
            same_height_count += 1
            print(f"Altura repetida: {same_height_count}/{max_same_height}")
        else:
            same_height_count = 0
            last_height = new_height

    print(f"Desplazamiento completo. Total de scrolls: {total_scrolls}")

    # Una vez que todas las capturas están hechas, unirlas
    imagen_final = Image.new('RGB', (capturas[0].width, total_height))
    
    current_height = 0
    for captura in capturas:
        imagen_final.paste(captura, (0, current_height))
        current_height += captura.height

    # Guardar la imagen final
    imagen_final.save(file_name)
    print(f"Captura de pantalla de toda la página guardada como: {file_name}")


def sacar_screenshot(driver, file_name):
    """Captura de pantalla de toda la página."""
    try:
        # Obtener la altura total del documento y la altura de la ventana visible
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        
        # Redimensionar la ventana para la altura total de la página
        driver.set_window_size(1920, total_height)
        
        # Esperar un momento para que la página se redibuje correctamente
        time.sleep(1)
        
        # Tomar la captura de pantalla y guardarla
        driver.save_screenshot(file_name)
        print(f"Captura de pantalla guardada como: {file_name}")
        
    except Exception as e:
        print(f"Se produjo un error al tomar la captura: {e}")


def dividir_imagenes(image_path, num_parts, nombre, capitulo):
    # Abrir la imagen
    img = Image.open(image_path)
    width, height = img.size

    # Calcular la altura de cada parte
    part_height = height // num_parts
    parts = []

    # Dividir la imagen en partes
    for i in range(num_parts):
        # Definir la caja de recorte para cada parte
        top = i * part_height
        bottom = (i + 1) * part_height if i < num_parts - 1 else height
        part = img.crop((0, top, width, bottom))

        # Guardar la parte como una imagen temporal
        part_path = f"parte_{i + 1}.png"
        part.save(part_path)
        parts.append(part_path)

    # Crear un PDF a partir de las partes

    # Aquí podrías tener la lógica para generar el PDF.
    pdf_name = f"{nombre} - {capitulo}.pdf"  # Formato del nombre del PDF
    pdf_path = os.path.join(os.getcwd(), "PDF", pdf_name)  #

    images = [Image.open(part) for part in parts]
    images[0].save(pdf_path, save_all=True, append_images=images[1:])

    # Limpiar archivos temporales
    for part in parts:
        os.remove(part)

    # Eliminar la imagen original si lo deseas

    print(f"PDF {pdf_name} creado exitosamente")


def descargar_manga(nombre, link_manga, capitulo, partes):
    imagen = f"{nombre} - {capitulo}.png"
    nueva_url = ingresar_capitulo(link_manga, capitulo)

    if nueva_url:
        print("Nueva URL:", nueva_url)

    driver = configurar_driver(ancho=1920, alto=1080)

    try:
        # Acceder a la nueva URL del capítulo
        driver.get(nueva_url)

        # Esperar que la página esté completamente cargada
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Desplazarse por la página y capturar capturas de pantalla por secciones
        try:
            desplazamiento_paginas_y_capturas(driver, imagen)
            if os.path.exists(imagen):
                dividir_imagenes(imagen, partes, nombre, capitulo)  # Procesar la imagen para dividirla en partes
            else:
                print(f"La imagen {imagen} no se pudo guardar correctamente.")
        except Exception as e:
            print(f"Se produjo un error al tomar la captura: {e}")

    except Exception as e:
        print(f"Se produjo un error durante la navegación: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    # Lista de mangas a procesar
    mangas = [
        {
            "nombre": "Isekai de Tochi wo Katte Noujou wo Tsukurou",
            "link_manga": "https://lectortmo.com/library/manga/47114/isekai-de-tochi-wo-katte-noujou-wo-tsukurou",
            "capitulo": "44"
        }
        # Agrega más mangas según sea necesario
    ]

    # Procesar cada manga en la lista
    for manga in mangas:
        descargar_manga(manga['nombre'], manga['link_manga'],
                        manga['capitulo'], partes=10)
