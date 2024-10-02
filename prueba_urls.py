from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse



def configurar_driver():
    """Configura y retorna el controlador de Selenium."""
    options = Options()
    options.add_argument("--headless")  # Ejecutar en segundo plano
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-web-security')
    options.add_argument("--window-size=200,300")
    options.add_argument('--allow-insecure-localhost')
    options.page_load_strategy = 'eager'
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def extraer_relevant_part(url):
    """Extrae la parte relevante de la URL original."""
    path_parts = urlparse(url).path.split('/')
    return path_parts[2] if len(path_parts) > 2 else None


def clic_en_elemento(driver, by, value):
    """Intenta hacer clic en un elemento y maneja excepciones."""
    try:
        elemento = driver.find_element(by, value)
        elemento.click()
        return True
    except NoSuchElementException:
        return False


'''
def ingresar_capitulo(link_manga, capitulo):
    """Ingresa al capítulo especificado de un manga y retorna la nueva URL."""
    driver = configurar_driver()
    new_url = None

    try:
        driver.get(link_manga)

        if clic_en_elemento(driver, By.LINK_TEXT, f"Capítulo {capitulo}.00"):
            print(f"Capítulo {capitulo} encontrado y clickeado.")
        else:
            print(f"No se encontró el enlace al capítulo {capitulo}.")
            return new_url

        # Encuentra todos los enlaces de capítulos
        chapter_links = driver.find_elements(By.CSS_SELECTOR, "a.btn-collapse")
        collapsible_id = next((link.get_attribute("onclick").split("'")[
                              1] for link in chapter_links if f"Capítulo {capitulo}.00" in link.text), None)

        if collapsible_id:
            print(f"ID del div colapsable: {collapsible_id}")
            collapsible_div = driver.find_element(By.ID, collapsible_id)

            if collapsible_div.is_displayed():
                print(f"El div con id '{collapsible_id}' está visible.")
                if clic_en_elemento(collapsible_div, By.CSS_SELECTOR, 'a.btn.btn-default.btn-sm'):
                    print("Clic en el enlace del capítulo realizado.")
                else:
                    print("No se encontró el enlace del capítulo en el div colapsable.")
            else:
                print(f"El div con id '{collapsible_id}' no está visible.")
        else:
            print(f"No se encontró el enlace al capítulo {capitulo}.")

        # Obtener la URL actual
        current_url = driver.current_url

        print("URL original:", current_url)

        # Verificar si la URL contiene '/paginated' antes de extraer la parte relevante
        if "/paginated" in current_url:
            relevant_part = extraer_relevant_part(current_url)

            if relevant_part:
                new_url = f"https://visortmo.com/viewer/{
                    relevant_part}/cascade"
            else:
                print("No se pudo extraer la parte relevante de la URL.")
        else:
            print("La URL no contiene '/paginated', no se extraerá la parte relevante.")

    except (TimeoutException, WebDriverException) as e:
        print("Error al buscar los capítulos o con el WebDriver:", e)

    finally:
        driver.quit()  # Asegurarse de cerrar el navegador
        return new_url
'''

import time
from functools import wraps

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

# Ejemplo de uso:


@timer
def ingresar_capitulo(link_manga, capitulo, nombre):
    """Ingresa al capítulo especificado de un manga y retorna la nueva URL."""
    driver = configurar_driver()  # Se puede ajustar el tamaño según sea necesario
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
        collapsible_id = next(
            (link.get_attribute("onclick").split("'")[
             1] for link in chapter_links if f"Capítulo {capitulo}" in link.text),
            None
        )

        if collapsible_id:
            print(f"ID del div colapsable: {collapsible_id}")
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

        else:
            print(f"No se encontró el enlace al capítulo {capitulo}.")
            return new_url

        # Obtener la URL actual
        current_url = driver.current_url

        print("URL original:", current_url)

        # Verificar si la URL contiene '/paginated' antes de extraer la parte relevante
        if "/paginated" in current_url:
            relevant_part = extraer_relevant_part(current_url)

            if relevant_part:
                new_url = f"https://visortmo.com/viewer/{
                    relevant_part}/cascade"
                # print("Nueva URL:", new_url)
            else:
                print("No se pudo extraer la parte relevante de la URL.")
        else:
            print("La URL no contiene '/paginated', no se extraerá la parte relevante.")

    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print("Error al buscar los capítulos o con el WebDriver:", e)

    finally:
        driver.quit()  # Asegurarse de cerrar el navegador
        return new_url


if __name__ == "__main__":
    # Lista de mangas a procesar
    mangas = [
        {
            "nombre": "Saikyou no Shien-shoku 'Wajutsushi' Dearu Ore wa Sekai Saikyou Clan wo Shitagaeru",
            "link_manga": "https://lectortmo.com/library/manga/50889/saikyou-no-shien-shoku-wajutsushi-dearu-ore-wa-sekai-saikyou-kuran-o-shitagaeru",
            "capitulo": "49"
        },
        {
            "nombre": "El misterioso trabajo llamado Oda Nobunaga resulto ser mas tramposo que espadachín mágico, así que decidí crear un reino",
            "link_manga": "https://lectortmo.com/library/manga/40790/oda-nobunaga-to-iu-nazo-no-shokugyou-ga-mahou-kenshi-yori-cheat-datta-node-oukoku-wo-tsukuru-koto-ni-shimashita",
            "capitulo": "25"
        },
        {
            "nombre": "Joshi Ochi!!",
            "link_manga": "https://lectortmo.com/library/manga/40646/joshi-ochi-2-kai-kara-ero-musume-ga-futte-kite-ore-no-areni",
            "capitulo": "65"
        },
        {
            "nombre": "Saikyou no Maou ni Kitaerareta Yuusha, Isekai Kikansha-tachi no Gakuen de Musou suru",
            "link_manga": "https://lectortmo.com/library/manga/67943/saikyou-no-maou-ni-kitaerareta-yuusha-isekai-kikanshatati-no-gakuen-de-musou-suru",
            "capitulo": "16"
        },
        {
            "nombre": "Kaifuku Jutsushi no Yarinaoshi",
            "link_manga": "https://lectortmo.com/library/manga/28551/kaifuku-jutsushi-no-yarinaoshi",
            "capitulo": "63"
        },
        {
            "nombre": "Gotou-san quiere que me dé la vuelta.",
            "link_manga": "https://lectortmo.com/library/manga/65661/gotou-san-wants-me-to-look-back",
            "capitulo": "20"
        },
        {
            "nombre": "Lo siento, pero no me gusta el Yuri",
            "link_manga": "https://lectortmo.com/library/manga/57343/lo-siento-pero-no-me-gusta-el-yuri",
            "capitulo": "39"
        },
        {
            "nombre": "Tsuihosareta Ochikobore, Henkyo de Ikinuite S-Rank Taimashi ni Nariagaru",
            "link_manga": "https://lectortmo.com/library/manga/58556/a-banished-failure-survives-in-the-borderland-and-becomes-an-s-rank-exorcist",
            "capitulo": "14"
        },
        {
            "nombre": "El que sube de nivel mas rapido",
            "link_manga": "https://lectortmo.com/library/manga/58624/sekai-saisoku-no-level-up",
            "capitulo": "21"
        },
        {
            "nombre": "Isekai de Tochi wo Katte Noujou wo Tsukurou",
            "link_manga": "https://lectortmo.com/library/manga/47114/isekai-de-tochi-wo-katte-noujou-wo-tsukurou",
            "capitulo": "44"
        }
        # Agrega más mangas según sea necesario
    ]

    # Procesar cada manga en la lista
    for manga in mangas:
        nueva_url = ingresar_capitulo(
            manga['link_manga'],
            manga['capitulo'],
            manga['nombre']
        )

        # Verificar si se obtuvo una nueva URL
        if nueva_url:
            print("Nueva URL para el manga:", nueva_url)
        else:
            print(f"No se pudo obtener una nueva URL para {
                  manga['nombre']} capítulo {manga['capitulo']}.")
