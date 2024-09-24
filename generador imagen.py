import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

def smooth_scroll(driver, pause_time=1, scroll_increment=500, max_same_height=8):
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

def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Ejecutar en segundo plano
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1980,1080")
    options.page_load_strategy = 'eager'
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def take_screenshot(driver, file_name):
    """Captura de pantalla de toda la página."""
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    driver.set_window_size(1920, total_height)  # Redimensionar la ventana para la altura total

    driver.save_screenshot(file_name)
    print(f"Captura de pantalla guardada como: {file_name}")


def main(url):
    driver = setup_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        smooth_scroll(driver)

        # Tomar captura de pantalla de toda la página
        screenshot_file = "screenshot.png"
        take_screenshot(driver, screenshot_file)

    except Exception as e:
        print(f"Se produjo un error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    target_url = "https://visortmo.com/viewer/a305ade97d053a2cd02455bf80d56c80/cascade"
    main(target_url)
