import asyncio
import time
from pyppeteer import launch

async def save_as_pdf(url, output_path):
    # Usa esta línea si quieres usar el Chrome instalado en tu sistema
    browser = await launch(executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
    
    # Si prefieres usar el Chromium descargado por Pyppeteer, comenta la línea anterior y descomenta esta:
    # browser = await launch(headless=True)
    
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle0'})
    await page.pdf({'path': output_path, 'format': 'A4'})
    time.sleep(30)
    await browser.close()

async def main():
    await save_as_pdf('https://visortmo.com/viewer/05f6661521a5c6c37c9d7a0a09df1dec/cascade', 'output.pdf')

if __name__ == "__main__":
    asyncio.run(main())