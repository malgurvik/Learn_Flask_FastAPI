"""
Задание №4
� Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль.
� Используйте потоки.
"""
import threading
import os
import time


def count_words(file, start_time):
    with open(file, 'r', encoding='utf-8') as f:
        words = f.read().split()
    print(f"File {os.path.basename(file)} has {len(words)} words in {time.time() - start_time:.2f} seconds")


def thread_example():
    files = [os.path.join('../lesson04/uploads', file) for file in os.listdir('../lesson04/uploads')]
    threads = []
    start_time = time.time()
    for file in files:
        thread = threading.Thread(target=count_words, args=[file, start_time])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    thread_example() # 0.06 seconds
