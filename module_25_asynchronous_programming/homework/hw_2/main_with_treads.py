from pathlib import Path
import time
from multiprocessing.pool import ThreadPool
import multiprocessing
import requests

URL = 'https://cataas.com/cat'
CATS_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()
ID_NUMBERS = [id for id in range(CATS_WE_WANT)]


def write_to_disk(index: int, content: bytes) -> None:
    file_path = "{}/{}.png".format(OUT_PATH, index)
    with open(file_path, 'wb') as f:
        f.write(content)


def get_all_cats(index):
    response = requests.get(URL, stream=True)
    if response.status_code == 200:
        write_to_disk(index, response.content)
    else:
        print(f"Ошибка при загрузке кота {index}: {response.status_code}")


def main():
    with ThreadPool(processes=multiprocessing.cpu_count() * 20) as pool:
        result = pool.map(get_all_cats, ID_NUMBERS)


if __name__ == '__main__':
    start = time.time()
    main()
    print(f'Main was completed in {round(time.time() - start, 4)} seconds')
