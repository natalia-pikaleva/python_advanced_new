import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10
TOTAL_SITS: int = 50

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):

    def __init__(self, lock: threading.Lock) -> None:
        super().__init__()
        self.lock: threading.Lock = lock
        self.tickets_sold: int = 0
        logger.info('Seller started work')

    def director_add_tickets(self) -> int:
        global TOTAL_TICKETS, TOTAL_SITS

        add_tickets: int = random.randint(1, 10)

        if TOTAL_SITS > 0:
            if add_tickets <= TOTAL_SITS:
                TOTAL_TICKETS += add_tickets
                return add_tickets
            else:
                added = TOTAL_SITS
                TOTAL_TICKETS += added
                return added
        return 0

    def run(self) -> None:
        global TOTAL_TICKETS, TOTAL_SITS
        while True:
            self.random_sleep()

            with self.lock:

                if TOTAL_SITS <= 0:
                    break


                if TOTAL_TICKETS <= 4 and TOTAL_SITS > 0:
                    add_tickets: int = self.director_add_tickets()

                    logger.info(
                        f'{self.name} director added: {add_tickets}, TOTAL_TICKETS: {TOTAL_TICKETS}')

                if TOTAL_TICKETS > 0 and TOTAL_SITS > 0:
                    self.tickets_sold += 1
                    TOTAL_TICKETS -= 1
                    TOTAL_SITS -= 1
                    logger.info(f'{self.name} sold one; {TOTAL_TICKETS} left, TOTAL_SITS: {TOTAL_SITS}')

        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


def main() -> None:
    lock: threading.Lock = threading.Lock()
    sellers: List[Seller] = []
    for _ in range(4):
        seller = Seller(lock)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()


if __name__ == '__main__':
    main()
