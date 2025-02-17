import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

URL = 'https://ya.ru/'
MAX_DEEP = 3


def extract_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        full_url = urljoin(base_url, a_tag['href'])

        if urlparse(full_url).netloc != urlparse(base_url).netloc:
            links.append(full_url)
    return links


async def get_data(client: aiohttp.ClientSession, url_path: str, deep: int):
    if deep >= MAX_DEEP:
        return

    try:
        async with client.get(url_path) as response:
            if response.status == 200:
                html_content = await response.text()
                links = extract_links(html_content, url_path)
                await write_to_file(url_path)

                for link in links:
                    await get_data(client, link, deep + 1)
            else:
                print(f"Ошибка: получен статус {response.status} для {url_path}")
    except Exception as e:
        print(f"Ошибка при обработке {url_path}: {e}")


async def write_to_file(url_path):
    async with aiofiles.open('file.txt', mode='a') as f:
        await f.write(f'{url_path}\n')


async def main():
    async with aiohttp.ClientSession() as client:
        await get_data(client, URL, deep=0)


if __name__ == '__main__':
    asyncio.run(main())
