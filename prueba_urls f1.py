from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import time
from functools import wraps


def configurar_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-web-security')
    options.add_argument("--window-size=200,300")
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
                print(f"Ocurrió un error al procesar {manga['nombre']}:", e)
        else:
            print(f"No se encontró el enlace al capítulo {
                  manga['capitulo']} de {manga['nombre']}.")
            return None

        current_url = driver.current_url
        if "/paginated" in current_url:
            relevant_part = extraer_relevant_part(current_url)
            if relevant_part:
                return f"https://visortmo.com/viewer/{relevant_part}/cascade"
            else:
                print(f"No se pudo extraer la parte relevante de la URL para {
                      manga['nombre']}.")
        else:
            print(f"La URL de {
                  manga['nombre']} no contiene '/paginated', no se extraerá la parte relevante.")

    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"Error al procesar {manga['nombre']}:", e)

    return None


def main(mangas):
    driver = configurar_driver()
    resultados = {'correctos': 0, 'errores': 0}

    try:
        for manga in mangas:
            nueva_url = procesar_manga(driver, manga)
            if nueva_url:
                print(f"Nueva URL para {manga['nombre']}: {nueva_url}")
                resultados['correctos'] += 1
            else:
                print(f"No se pudo obtener una nueva URL para {
                      manga['nombre']} capítulo {manga['capitulo']}.")
                resultados['errores'] += 1
    finally:
        driver.quit()

    print("\nResumen de resultados:")
    print(f"Correctos: {resultados['correctos']}")
    print(f"Errores: {resultados['errores']}")


if __name__ == "__main__":
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

    main(mangas)
