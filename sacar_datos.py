from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def configurar_navegador():
    # Configurar opciones de Chrome
    chrome_options = Options()
    # Ejecuta en modo headless (sin interfaz gráfica)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=200,300")

    # Iniciar el navegador
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def extraer_datos(url):
    driver = configurar_navegador()
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


def guardar_resultados_txt(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        # Escribir el conteo de mangas
        file.write(f"Cantidad de mangas extraídos: {len(data)}\n\n")

        # Escribir los detalles de cada manga
        for item in data:
            file.write(f'"nombre": "{item["nombre"]}",\n')
            file.write(f'"link_manga": "{item["enlace"]}",\n')
            file.write(f'"capitulo": "{item["capitulo faltante"]}"\n')
            file.write("-" * 40 + "\n")


# URL de la página a analizar
url = "http://inventarioncc.infinityfreeapp.com/Manga/?capitulos=2&accion=Filtro3"

# Extrae y muestra los datos
data = extraer_datos(url)

# Guardar los datos en un archivo .txt
guardar_resultados_txt(data, "resultados_mangas.txt")

# Conteo de mangas extraídos
conteo_mangas = len(data)

print(f"Cantidad de mangas extraídos: {conteo_mangas}")

for item in data:
    print(item)

print(f"Datos guardados en 'resultados_mangas.txt'")
