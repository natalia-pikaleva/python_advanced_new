from typing import Union, List

Number = Union[int, float, complex]


def find_insert_position(array: List[Number], number: Number) -> int:
    if len(array) == 0:
        return 0

    avg_index = len(array) // 2

    if number == array[avg_index]:
        return avg_index + 1

    if number < array[avg_index]:
        for index in range(0, avg_index):
            if array[index] <= number <= array[index + 1]:
                return index + 1

    if number > array[avg_index]:
        for index in range(len(array), avg_index, -1):
            if array[index - 1] <= number <= array[index]:
                return index


if __name__ == '__main__':
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 5

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    A.insert(insert_position, x)
    assert A == sorted(A)
