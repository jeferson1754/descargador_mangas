from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from PIL import Image
import os
import time
from functools import wraps

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
    path_parts = urlparse(url).path.split('/')
    return path_parts[2] if len(path_parts) > 2 else None


def clic_en_elemento(driver, by, value):
    try:
        elemento = driver.find_element(by, value)
        elemento.click()
        return True
    except NoSuchElementException:
        return False


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"La función {func.__name__} tardó {
              end_time - start_time:.4f} segundos en ejecutarse.")
        return result
    return wrapper


@timer
def procesar_manga(driver, manga):
    try:
        driver.get(manga['link_manga'])
        try:
            chapter_link = driver.find_element(
                By.PARTIAL_LINK_TEXT, f"Capítulo {manga['capitulo']}")
            chapter_link.click()
            print(f"Capítulo {manga['capitulo']} de {
                  manga['nombre']} encontrado y clickeado.")
        except NoSuchElementException:
            print(f"No se encontró el enlace al capítulo {
                  manga['capitulo']} de {manga['nombre']}.")
            return None

        chapter_links = driver.find_elements(By.CSS_SELECTOR, "a.btn-collapse")
        collapsible_id = next((link.get_attribute("onclick").split("'")[
                              1] for link in chapter_links if f"Capítulo {manga['capitulo']}" in link.text), None)

        if collapsible_id:
            try:
                collapsible_div = driver.find_element(By.ID, collapsible_id)
                if collapsible_div.is_displayed():
                    link_element = collapsible_div.find_element(
                        By.CSS_SELECTOR, 'a.btn.btn-default.btn-sm')
                    link_element.click()
                    print(f"Clic en el enlace del capítulo {
                          manga['capitulo']} de {manga['nombre']} realizado.")
                else:
                    print(f"El div del capítulo {manga['capitulo']} de {
                          manga['nombre']} no está visible.")
            except NoSuchElementException:
                print(f"No se encontró el enlace del capítulo {
                      manga['capitulo']} de {manga['nombre']} en el div colapsable.")
            except Exception as e:
                print(f"Ocurrió un error al procesar {manga['nombre']}: {e}")
        else:
            print(f"No se encontró el enlace al capítulo {
                  manga['capitulo']} de {manga['nombre']}.")
            return None

        current_url = driver.current_url
        if "/paginated" in current_url:
            relevant_part = extraer_relevant_part(current_url)
            if relevant_part:
                return f"https://zonatmo.com/viewer/{relevant_part}/cascade"
            else:
                print(f"No se pudo extraer la parte relevante de la URL para {
                      manga['nombre']}.")
        else:
            print(f"La URL de {manga['nombre']} no contiene '/paginated', no se extraerá la parte relevante.")
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"Error al procesar {manga['nombre']}: {e}")

    return None


@timer
def desplazamiento_paginas(driver, pause_time=1, scroll_increment=500, max_same_height=15, max_scrolls=100):
    """Desplaza suavemente hacia abajo en la página completa, pero se detiene si el número de desplazamientos supera los 100."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    same_height_count = 0
    total_scrolls = 0

    print("Comenzando desplazamiento...")

    while same_height_count < max_same_height and total_scrolls < max_scrolls:
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        total_scrolls += 1

        print(f"Desplazamiento {total_scrolls}: Nueva altura: {
              new_height}px. Anterior: {last_height}px.")

        if new_height == last_height:
            same_height_count += 1
            print(f"Altura repetida: {same_height_count}/{max_same_height}")
        else:
            same_height_count = 0
            last_height = new_height

    if total_scrolls >= max_scrolls:
        print(f"Desplazamiento detenido. Se alcanzó el límite de {
              max_scrolls} desplazamientos.")
    else:
        print(f"Desplazamiento completo. Total de desplazamientos: {
              total_scrolls}")


@timer
def sacar_screenshot(driver, file_name):
    """Captura de pantalla de toda la página."""
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, total_height)
    driver.save_screenshot(file_name)
    print(f"Captura de pantalla guardada como: {file_name}")


@timer
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
    pdf_name = f"{nombre} - {capitulo}.pdf"
    pdf_path = os.path.join(os.getcwd(), "PDF", pdf_name)

    images = [Image.open(part) for part in parts]
    images[0].save(pdf_path, save_all=True, append_images=images[1:])

    # Limpiar archivos temporales
    for part in parts:
        os.remove(part)

    print(f"PDF {pdf_name} creado exitosamente.")


@timer
def descargar_manga(mangas, max_intentos, partes):
    driver = configurar_driver(ancho=1920, alto=1080)

    try:
        for manga in mangas:
            imagen = f"{manga['nombre']} - {manga['capitulo']}.png"
            intentos = 0  # Reiniciar intentos para cada manga
            while intentos < max_intentos:  # REVISAR ESTA PARTE
                nueva_url = procesar_manga(driver, manga)
                if nueva_url:
                    print(f"Nueva URL para {manga['nombre']}: {nueva_url}")
                    driver.get(nueva_url)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )

                    # Desplazamiento de páginas
                    desplazamiento_paginas(driver)

                    while intentos < max_intentos:
                        try:
                            sacar_screenshot(driver, imagen)
                            if os.path.exists(imagen):
                                dividir_imagenes(
                                    imagen, partes, manga['nombre'], manga['capitulo'])
                                break  # Salir del bucle si se guarda correctamente
                            else:
                                print(f"La imagen {
                                      imagen} no se pudo guardar correctamente.")
                        except Exception as e:
                            if isinstance(e, TimeoutException):
                                print(
                                    "Se superó el tiempo determinado al intentar tomar la captura de la página")
                            else:
                                print(
                                    f"Se produjo un error al tomar la captura: {e}")

                            intentos += 1  # Aumentar el contador de intentos
                            print(
                                f"Reintentando el desplazamiento de páginas... (Intento {intentos})")
                            desplazamiento_paginas(driver, max_scrolls=50)
                else:
                    print(f"No se pudo obtener una nueva URL para {
                          manga['nombre']} capítulo {manga['capitulo']}.")

        if os.path.exists(imagen):
            dividir_imagenes(
                imagen, partes, manga['nombre'], manga['capitulo'])
        else:
            print(f"La imagen {imagen} no se encontró.")

    finally:
        driver.quit()


if __name__ == "__main__":
    # Lista de mangas a procesar
    mangas = [
        {
            "nombre": "Saikyou Juzoku Tensei: Cheat Majutsushi no Slow Life",
            "link_manga": "https://lectortmo.com/library/manga/43676/saikyou-juzoku-tensei-majutsu-otaku-no-risoukyou",
            "capitulo": "27"
        }
    ]

    # Procesar cada manga en la lista
    descargar_manga(mangas, max_intentos=3, partes=15)
