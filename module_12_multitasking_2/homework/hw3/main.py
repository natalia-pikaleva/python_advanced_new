from threading import Semaphore, Thread, Event
import time

sem: Semaphore = Semaphore()
stop_event = Event()


def fun1():
    while not stop_event.is_set():
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    while not stop_event.is_set():
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


t1: Thread = Thread(target=fun1)  # TODO добавьте параметр daemon=True
t2: Thread = Thread(target=fun2)  # TODO Аналогично предыдущему
# TODO создание потоков работающих в фоновом режиме https://codechick.io/tutorials/python/python-daemon-threads

try:
    t1.start()
    t2.start()
    while t1.is_alive() or t2.is_alive():  # TODO вместо цикла достаточно джойнить потоки прямо тут, ведь join блокирующий метод
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\nReceived keyboard interrupt, quitting threads.')
    stop_event.set()
    t1.join()
    t2.join()
    print('Threads have been terminated gracefully.')
