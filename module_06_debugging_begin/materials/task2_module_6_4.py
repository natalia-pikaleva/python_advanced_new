import heapq
import json
import logging
from typing import List

from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

logger = logging.getLogger("sort")


def bubble_sort(array: List[int]) -> List[int]:
    n = len(array)

    for i in range(n):
        for j in range(i + 1, n):
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]

    return array


def tim_sort(array: List[int]) -> List[int]:
    array.sort()

    return array


def heap_sort(array: List[int]) -> List[int]:
    data = []

    for val in array:
        heapq.heappush(data, val)

    return [heapq.heappop(data) for _ in range(len(data))]


algorithms = {
    "bubble": bubble_sort,
    "tim": tim_sort,
    "heap": heap_sort,
}


@app.route("/<algorithm_name>/", methods=["POST"])
def sort_endpoint(algorithm_name: str):
    logger.info(f'Started sort {algorithm_name}')
    start_time = datetime.now()

    if algorithm_name not in algorithms:
        return f"Bad algorithm name, acceptable values are {algorithms.keys()}", 400

    form_data = request.get_data(as_text=True)

    array = json.loads(form_data)

    result = algorithms[algorithm_name](array)

    current_time = datetime.now()
    logger.info(f'Время работы алгоритма {algorithm_name}: {current_time - start_time}')
    return json.dumps(result)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Started sort server")
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
