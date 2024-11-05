"""
Задание №6
� Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль.
� Используйте асинхронный подход.
"""
import asyncio
import os
import time


async def count_words(file, start_time):
    with open(file, 'r', encoding='utf-8') as f:
        words = f.read().split()
    print(f"File {os.path.basename(file)} has {len(words)} words in {time.time() - start_time:.2f} seconds")


async def async_example():
    files = [os.path.join('../lesson04/uploads', file) for file in os.listdir('../lesson04/uploads')]
    tasks = []
    start_time = time.time()
    for file in files:
        task = asyncio.ensure_future(count_words(file, start_time))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(async_example())  # 0.05 seconds
