from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def configurar_navegador():
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecuta en modo headless (sin interfaz gráfica)
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
                'enlace': titulo_elemento.get_attribute('href'),  # Obtiene el enlace del título
                'capitulo faltante': cols[2].text.strip(),
            }
            data.append(manga_info)

    driver.quit()
    return data

# URL de la página a analizar
url = "http://inventarioncc.infinityfreeapp.com/Manga/?capitulos=1&accion=Filtro3"

# Extrae y muestra los datos
data = extraer_datos(url)

# Conteo de mangas extraídos
conteo_mangas = len(data)

print(f"Cantidad de mangas extraídos: {conteo_mangas}")

for item in data:
    print(item)
