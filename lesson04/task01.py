"""
Задание №1
� Написать программу, которая считывает список из 10 URL-адресов и одновременно загружает данные с каждого
адреса.
� После загрузки данных нужно записать их в отдельные
файлы.
� Используйте потоки.
"""
import os
import time

import requests
import threading


def download(url, start_time):
    response = requests.get(url)
    filename = 'threads_' + url.replace('https://', '').replace('.', '_').replace('/', '_') + '.html'
    with open(os.path.join('../lesson04/uploads', filename), 'w', encoding='utf-8') as file:
        file.write(response.text)
    print(f"Downloaded {url} in {time.time()-start_time:.2f}seconds")


def thread_example(urls: list[str]):
    threads = []
    start_time = time.time()
    for url in urls:
        thread = threading.Thread(target=download, args=[url, start_time])
        threads.append(thread)
        thread.start()
        # download(url, start_time)
    for thread in threads:
        thread.join()

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

    thread_example(urls)


if __name__ == '__main__':
    main() # 0.83seconds