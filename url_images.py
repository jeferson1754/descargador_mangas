import asyncio
from pyppeteer import launch

async def find_image_urls(url):
    browser = await launch(executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    page = await browser.newPage()
    
    await page.goto(url, {'waitUntil': 'networkidle0'})

    # Buscar todas las imágenes en el documento
    image_urls = await page.evaluate('''() => {
        const images = Array.from(document.querySelectorAll('.img-container.text-center img'));
        return images.map(img => img.src);  // Devolver un array con las URLs de las imágenes
    }''')

    # Imprimir todas las URLs encontradas
    for idx, img_url in enumerate(image_urls):
        print(f'URL de la imagen {idx + 1}: {img_url}')

    # Contar el total de imágenes encontradas
    total_images = len(image_urls)
    print(f'Total de imágenes encontradas: {total_images}')

    await browser.close()

async def main():
    await find_image_urls('https://visortmo.com/viewer/a305ade97d053a2cd02455bf80d56c80/cascade')

if __name__ == "__main__":
    asyncio.run(main())
