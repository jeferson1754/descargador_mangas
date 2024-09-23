import asyncio
import random
from pyppeteer import launch


async def random_sleep(min_seconds, max_seconds):
    await asyncio.sleep(random.uniform(min_seconds, max_seconds))


async def scroll_down(page, delay=7):
    """Scroll down the page until reaching the bottom."""
    last_height = await page.evaluate('document.body.scrollHeight')
    while True:
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await random_sleep(delay * 0.8, delay * 1.2)
        new_height = await page.evaluate('document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height


async def remove_ads(page):
    """Remove ads and unnecessary elements from the page."""
    await page.evaluate('''() => {
        const selectors = [
            'div[class*="ad"]', 
            'div[id*="ad"]',
            'script',
            'noscript',
            '.navigation-controls',
            '#disqus_thread',
            'footer'
        ];
        selectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(el => el.remove());
        });
    }''')


async def save_as_pdf(url, output_path):
    browser = await launch(
        executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-infobars',
            '--window-position=0,0',
            '--ignore-certificate-errors',
            '--ignore-certificate-errors-spki-list',
        ],
        ignoreHTTPSErrors=True
    )

    page = await browser.newPage()

    # Set a random user agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    await page.setUserAgent(random.choice(user_agents))

    # Set viewport to a common resolution
    await page.setViewport({'width': 1920, 'height': 1080})

    # Enable JavaScript
    await page.setJavaScriptEnabled(True)

    # Add additional headers
    await page.setExtraHTTPHeaders({
        'Referer': 'https://www.google.com/'
    })

    # Navigate to the page
    await page.goto(url, {'waitUntil': 'networkidle0', 'timeout': 60000})

    # Check for Cloudflare challenge
    if await page.querySelector('iframe[src*="challenges.cloudflare.com"]'):
        print("Cloudflare challenge detected. Waiting for manual solve...")
        await page.waitForNavigation({'waitUntil': 'networkidle0', 'timeout': 60000})

    print("Desplazando hacia abajo...")
    await scroll_down(page)

    print("Removiendo anuncios y elementos innecesarios...")
    await remove_ads(page)

    print("Esperando a que todas las imágenes se carguen...")
    await random_sleep(8, 12)

    print("Guardando como PDF...")
    await page.pdf({
        'path': output_path,
        'format': 'A4',
        'printBackground': True,
        'margin': {'top': '20px', 'right': '20px', 'bottom': '20px', 'left': '20px'}
    })
    print(f"PDF guardado en {output_path}")

    await browser.close()


async def main():
    await save_as_pdf('https://visortmo.com/viewer/a305ade97d053a2cd02455bf80d56c80/cascade', 'output.pdf')

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
