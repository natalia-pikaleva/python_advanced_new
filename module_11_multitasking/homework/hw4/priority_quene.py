import threading
from time import sleep
from typing import List, Callable
import random

import queue


class Task():
    def __init__(self, priority: int, func: Callable, args) -> None:
        self.priority = priority
        self.func = func
        self.args = args

    def __lt__(self, other: "Task") -> bool:
        return self.priority < other.priority


class Producer(threading.Thread):
    def __init__(self, queue: queue.PriorityQueue, event: threading.Event) -> None:
        super().__init__()
        self.queue = queue
        self.event = event

    def run(self):
        print('Produser running')
        for _ in range(10):
            priority = random.randint(0, 7)
            time_sleep = random.random()

            self.queue.put(Task(priority, sleep, time_sleep))
        print('Producer: Done')
        self.event.set()


class Consumer(threading.Thread):
    def __init__(self, queue: queue.PriorityQueue, event: threading.Event) -> None:
        super().__init__()
        self.queue = queue
        self.event = event

    def run(self):
        print('Consumer running')
        self.event.wait()

        while not self.queue.empty():
            task = self.queue.get()
            print(f'running Task(priority={task.priority}).\tSleep({task.args})')
            task.func(task.args)
            self.queue.task_done()

        print('Consumer: Done')


if __name__ == "__main__":
    task_queue = queue.PriorityQueue()
    event = threading.Event()

    producer = Producer(task_queue, event)
    consumer = Consumer(task_queue, event)

    producer.start()
    producer.join()

    consumer.start()
    consumer.join()
