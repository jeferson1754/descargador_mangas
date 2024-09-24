import asyncio
import time
from pyppeteer import launch



async def save_as_pdf(url, output_path):
    browser = await launch(executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle0'})
    
    # Scroll down the page
    print("Desplazando hacia abajo...")
    
    # Wait for a moment to ensure all images are loaded
    print("Esperando a que todas las imágenes se carguen...")
    
    # Save the page as PDF
    await page.pdf({'path': output_path, 'format': 'A4'})
    print(f"PDF guardado en {output_path}")
    
    await browser.close()

async def main():
    await save_as_pdf('https://emol.com', 'output.pdf')

if __name__ == "__main__":
    asyncio.run(main())

