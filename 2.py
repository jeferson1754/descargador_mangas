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


def extraer_datos(url):
    driver = configurar_driver(ancho=200, alto=300)
    driver.get(url)

    # Espera que la página se cargue
    time.sleep(5)  # Ajusta el tiempo según sea necesario

    # Encuentra todas las filas de la tabla
    rows = driver.find_elements(By.TAG_NAME, "tr")

    # Almacena los datos extraídos
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if cols:  # Comprueba si hay columnas en la fila
            # Extrae el nombre del manga y el enlace
            titulo_elemento = cols[0].find_element(By.TAG_NAME, "a")
            manga_info = {
                'nombre': titulo_elemento.text.strip(),
                # Obtiene el enlace del título
                'enlace': titulo_elemento.get_attribute('href'),
                'capitulo faltante': cols[2].text.strip(),
            }
            data.append(manga_info)

    driver.quit()
    return data


def extraer_relevant_part(url):
    """Extrae la parte relevante de la URL original."""
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    return path_parts[2] if len(path_parts) > 2 else None


def ingresar_capitulo(link_manga, capitulo,nombre):
    """Ingresa al capítulo especificado de un manga y retorna la nueva URL."""
    driver = configurar_driver(200,300)
    new_url = None

    try:
        driver.get(link_manga)

        # Intentar hacer clic en el capítulo
        try:
            # Usar By.PARTIAL_LINK_TEXT para buscar enlaces que contengan "Capítulo X.00"
            chapter_link = driver.find_element(
                By.PARTIAL_LINK_TEXT, f"Capítulo {capitulo}")
            chapter_link.click()
            print(f"Capítulo {capitulo} de {nombre} encontrado y clickeado.")
        except NoSuchElementException:
            print(f"No se encontró el enlace al capítulo {capitulo}.")
            return new_url  # Salir si no se encuentra el capítulo


        # Encuentra todos los enlaces de capítulos
        chapter_links = driver.find_elements(By.CSS_SELECTOR, "a.btn-collapse")

        # Iterar sobre cada enlace para encontrar el correspondiente al capítulo
        collapsible_id = None
        for link in chapter_links:
            if f"Capítulo {capitulo}" in link.text:
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


def desplazamiento_paginas(driver, pause_time=1, scroll_increment=500, max_same_height=15, max_scrolls = 100):
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

        print(f"Desplazamiento {total_scrolls}: Nueva altura: {new_height}px. Anterior: {last_height}px.")

        if new_height == last_height:
            same_height_count += 1
            print(f"Altura repetida: {same_height_count}/{max_same_height}")
        else:
            same_height_count = 0
            last_height = new_height

    if total_scrolls >= max_scrolls:
        print(f"Desplazamiento detenido. Se alcanzó el límite de {max_scrolls} desplazamientos.")
    else:
        print(f"Desplazamiento completo. Total de desplazamientos: {total_scrolls}")


def sacar_screenshot(driver, file_name):
    """Captura de pantalla de toda la página."""
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    # Redimensionar la ventana para la altura total
    driver.set_window_size(1920, total_height)
    driver.save_screenshot(file_name)
    print(f"Captura de pantalla guardada como: {file_name}")


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
    nueva_url = ingresar_capitulo(link_manga, capitulo, nombre)

    if nueva_url:
        print("Nueva URL:", nueva_url)

    # driver = configurar_driver(ancho=2560, alto=1440)
    driver = configurar_driver(ancho=1920, alto=1080)
    #driver = configurar_driver(ancho=1080, alto=1920)
    # driver = configurar_driver(ancho=200, alto=300)

    try:
        driver.get(nueva_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        desplazamiento_paginas(driver)

        # Tomar captura de pantalla de toda la página
        intentos = 1  # Contador de intentos
        max_intentos = 4  # Número máximo de intentos

        while intentos < max_intentos:
            try:
                sacar_screenshot(driver, imagen)
                if os.path.exists(imagen):
                    dividir_imagenes(imagen, partes, nombre, capitulo)
                    break  # Salir del bucle si se guarda correctamente
                else:
                    print(f"La imagen {imagen} no se pudo guardar correctamente.")
                    intentos += 1  # Aumentar el contador de intentos
                    print(
                        f"Reintentando el desplazamiento de páginas... (Intento {intentos})")
                    # Volver a desplazar páginas
                    desplazamiento_paginas(driver)
            except Exception as e:
                if isinstance(e, TimeoutException):
                    print(f"Se supero el tiempo determinado al intentar tomar la captura de la pagina")
                else:
                    print(f"Se produjo un error al tomar la captura: {e}")

                intentos += 1  # Aumentar el contador de intentos
                print(f"Reintentando el desplazamiento de páginas... (Intento {intentos})")
                desplazamiento_paginas(driver)  # Volver a desplazar páginas

    except Exception as e:
        print(f"Se produjo un error: {e}")
    finally:
        driver.quit()

    if os.path.exists(imagen):
        dividir_imagenes(imagen, partes, nombre, capitulo)
    else:
        print(f"La imagen {imagen} no se encontró.")


def eliminar_imagenes_png():
    """Elimina todas las imágenes en formato PNG en la carpeta actual tras confirmación."""
    archivos_png = [archivo for archivo in os.listdir('.') if archivo.endswith('.png')]
    
    if not archivos_png:
        print("No se encontraron imágenes PNG en la carpeta actual.")
        return
    
    print(f"Se encontraron las siguientes imágenes PNG:")
    for archivo in archivos_png:
        print(archivo)

    confirmar = input(f"¿Estás seguro de que deseas eliminar estas imágenes? (Presiona Enter para confirmar): ")
    
    if confirmar == '':
        for archivo in archivos_png:
            try:
                os.remove(archivo)
                print(f"Eliminado: {archivo}")
            except Exception as e:
                print(f"No se pudo eliminar {archivo}: {e}")
    else:
        print("Eliminación cancelada.")


if __name__ == "__main__":
    
    exitosos = []
    errores = []

    # URL de la página a analizar
    url = "http://inventarioncc.infinityfreeapp.com/Manga/?capitulos=1&accion=Filtro3"

    # Extrae y muestra los datos
    data = extraer_datos(url)

    # Conteo de mangas extraídos
    conteo_mangas = len(data)
    print(f"Cantidad de mangas extraídos: {conteo_mangas}")

    # Procesar cada manga en la lista extraída
    for manga in data:
        try:
            descargar_manga(manga['nombre'], manga['enlace'], manga['capitulo faltante'], partes=10)
            exitosos.append(manga['nombre'])  # Agregar a la lista de exitosos
        except Exception as e:
            errores.append((manga['nombre'], str(e)))  # Agregar a la lista de errores

    print("\nResumen del proceso:\n")
    print("Mangas procesados correctamente:")
    for manga in exitosos:
        print(f"- {manga}")

    print("\nMangas con errores:")
    for manga, error in errores:
        print(f"- {manga}: {error}")
        
    # Llamar a la función
    eliminar_imagenes_png()
