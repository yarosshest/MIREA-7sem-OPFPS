import os
import random
import threading
import math
import logging
from multiprocessing import Pool, Manager

# Настройка логирования
logging.basicConfig(
    filename=os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "log", "main.log"),
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    encoding='utf-8'
)


# Функция для проверки числа на простоту
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    limit = int(math.sqrt(n)) + 1
    for i in range(5, limit, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def find_next_prime(start, prime_cache):
    """Находит следующее большее простое число."""
    current = start + 1
    while True:
        kache = True
        if random.random() > 0.95:
            logging.error(f"Кеш не ответил")
            kache = False
        if current in prime_cache and kache:
            if prime_cache[current]:
                logging.info(f"Число {current} найдено в кэше: {prime_cache[current]}")
                return current
        else:
            result = is_prime(current)
            prime_cache[current] = result
            if result:
                logging.info(f"Найдено новое простое число: {current}")
                return current
        current += 1


def worker_task(args):
    """Задача для процесса: нахождение одного простого числа."""
    start, prime_cache = args
    return find_next_prime(start, prime_cache)


if __name__ == "__main__":
    # Начальное число
    start_number = 1
    primes_to_find = 10000000
    num_processes = 6

    with Manager() as manager:
        prime_cache = manager.dict()
        with Pool(processes=num_processes) as pool:
            tasks = [(start_number + i, prime_cache) for i in range(primes_to_find)]
            results = pool.map(worker_task, tasks)

        for prime in results:
            logging.info(f"Найдено простое число: {prime}")
