"""
Задание №3
� Написать программу, которая считывает список из 10 URL-адресов и одновременно загружает данные с каждого
адреса.
� После загрузки данных нужно записать их в отдельные
файлы.
� Используйте асинхронный подход.
"""
import asyncio
import os.path

import aiohttp
import time


async def download(url, start_time):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    filename = 'async_' + url.replace('https://', '').replace('.', '_').replace('/', '_') + '.html'
    with open(os.path.join('../lesson04/uploads', filename), 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Downloaded {url} in {time.time() - start_time:.2f}seconds")


async def async_example(urls: list[str]):
    tasks = []
    start_time = time.time()
    for url in urls:
        task = asyncio.ensure_future(download(url, start_time))
        tasks.append(task)
    await asyncio.gather(*tasks)


def main():
    urls = ['https://www.google.ru/',
            'https://gb.ru/',
            'https://ya.ru/',
            'https://www.python.org/',
            'https://habr.com/ru/all/',
            'https://metanit.com/',
            'https://www.codewars.com/dashboard',
            'https://leetcode.com/',
            'https://plafon.gitbook.io/fedora-zero'
            ]

    # loop = asyncio.get_event_loop()  # Может не работать
    # loop.run_until_complete(async_example(urls)) # Может не работать
    asyncio.run(async_example(urls)) # Предпочтительно



if __name__ == '__main__':
    main() # 0.95seconds
