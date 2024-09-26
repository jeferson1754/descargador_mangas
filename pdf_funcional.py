import asyncio
from pyppeteer import launch

async def save_as_pdf(url, output_path):
    # Lanzar el navegador usando Chrome
    browser = await launch(executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe', 
                           headless=True)  # Modo headless para no mostrar la ventana del navegador
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle0'})  # Esperar hasta que no haya más solicitudes de red

    print("Desplazando hacia abajo...")

    # Desplazar hacia abajo para cargar imágenes si es necesario
    await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')

    # Esperar unos segundos para garantizar que las imágenes se carguen
    print("Esperando a que todas las imágenes se carguen...")
    await asyncio.sleep(3)  # Pausa de 3 segundos

    # Guardar la página como PDF
    await page.pdf({'path': output_path, 'format': 'A4'})
    print(f"PDF guardado en {output_path}")

    await browser.close()

async def main():
    await save_as_pdf('https://amazon.com', 'output.pdf')

if __name__ == "__main__":
    asyncio.run(main())
