import json
import time
from concurrent.futures import ThreadPoolExecutor
import requests
import logging

logging.basicConfig(level=logging.DEBUG)


class BookClient:
    URL: str = 'http://127.0.0.1:5000/api/books'
    TIMEOUT: int = 5

    def get_all_books(self) -> dict:
        response = requests.get(self.URL, timeout=self.TIMEOUT)
        return response.json()

    def add_new_book(self, data: dict):
        response = requests.post(self.URL, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def measure_time_without_session(self, method_name: str, num_requests: int, *args) -> float:
        start_time = time.time()
        for _ in range(num_requests):
            getattr(self, method_name)(*args)
        return time.time() - start_time

    def measure_multiple_requests_without_session(self, method_name: str, num_requests: int, *args) -> float:
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(getattr(self, method_name), *args) for _ in range(num_requests)]
            for future in futures:
                future.result()  # Ждем завершения всех потоков
        return time.time() - start_time


class SessionAPIClient:
    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url

    def get_books(self):
        response = self.session.get(f"{self.base_url}/api/books")
        return response.json()

    def add_new_book(self, data):
        response = self.session.post(f"{self.base_url}/api/books", json=data)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def measure_with_session(self, method_name: str, num_requests: int, *args) -> float:
        start_time = time.time()
        for _ in range(num_requests):
            getattr(self, method_name)(*args)
        return time.time() - start_time

    def measure_multiple_requests_with_session(self, method_name: str, num_requests: int, *args) -> float:
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(getattr(self, method_name), *args) for _ in range(num_requests)]
            for future in futures:
                future.result()  # Ждем завершения всех потоков
        return time.time() - start_time


if __name__ == '__main__':
    base_url = 'http://127.0.0.1:5000'
    api_client = SessionAPIClient(base_url)

    # Добавляем новую книгу для тестирования
    # unique_title = f"Book {int(time.time())}"
    # api_client.add_new_book({'title': unique_title, 'author': {'first_name': 'first_name', 'last_name': 'last_name'}})

    client_without_session = BookClient()

    for num_requests in [1000]:
        print(f"Testing with {num_requests} requests:")

        # -S -T (без сессии и без потоков)
        time_taken_no_session_no_threads = client_without_session.measure_time_without_session('get_all_books',
                                                                                               num_requests)
        print(f"Without session and threads: {time_taken_no_session_no_threads:.2f} seconds")

        # +S -T (с сессией и без потоков)
        time_taken_with_session_no_threads = api_client.measure_with_session('get_books', num_requests)
        print(f"With session and without threads: {time_taken_with_session_no_threads:.2f} seconds")

        # -S +T (без сессии и с потоками)
        time_taken_no_session_with_threads = client_without_session.measure_multiple_requests_without_session(
            'get_all_books', num_requests)
        print(f"Without session and with threads: {time_taken_no_session_with_threads:.2f} seconds")

        # +S +T (с сессией и с потоками)
        time_taken_with_session_with_threads = api_client.measure_multiple_requests_with_session('get_books',
                                                                                                 num_requests)
        print(f"With session and with threads: {time_taken_with_session_with_threads:.2f} seconds")

        print("-" * 40)
