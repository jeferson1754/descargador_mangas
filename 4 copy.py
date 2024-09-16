import asyncio
import time
from pyppeteer import launch

async def scroll_down(page, delay=7):
    """Scroll down the page until reaching the bottom."""
    last_height = await page.evaluate('document.body.scrollHeight')
    while True:
        # Scroll down
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        # Wait for new content to load
        await page.waitFor(delay * 3000)
        # Calculate new scroll height and compare with last height
        new_height = await page.evaluate('document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

async def save_as_pdf(url, output_path):
    browser = await launch(executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle0'})
    
    # Scroll down the page
    print("Desplazando hacia abajo...")
    await scroll_down(page)
    
    # Wait for a moment to ensure all images are loaded
    print("Esperando a que todas las imágenes se carguen...")
    #await page.waitFor(30000)  # Espera 30 segundos
    
    # Save the page as PDF
    await page.pdf({'path': output_path, 'format': 'A4'})
    print(f"PDF guardado en {output_path}")
    
    await browser.close()

async def main():
    await save_as_pdf('https://visortmo.com/viewer/05f6661521a5c6c37c9d7a0a09df1dec/cascade', 'output.pdf')

if __name__ == "__main__":
    asyncio.run(main())
