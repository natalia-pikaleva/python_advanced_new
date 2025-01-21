from typing import Union, List

Number = Union[int, float, complex]


def find_insert_position(array: List[Number], number: Number) -> int:
    if len(array) == 0:
        return 0

    if number <= array[0]:
        return 0

    if number >= array[-1]:
        return len(array)

    mmin = 0
    mmax = len(array) - 1
    avg_index = len(array) // 2

    result = find_insert_position(array[mmin:avg_index], number) + find_insert_position(array[avg_index: mmax], number)

    return result
# TODO намного проще использовать обычный бинарный поиск без рекурсий:
# def find_insert_position(array: list[Number], number: Number) -> int:
#     left, right = 0, len(array) - 1
#     while left <= right:
#         mid = (left + right) // 2
#         if array[mid] == number:
#             return mid
#         if array[mid] < number:
#             left = mid + 1
#         else:
#             right = mid - 1
#     return right + 1


if __name__ == '__main__':
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 5

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    A.insert(insert_position, x)
    assert A == sorted(A)
