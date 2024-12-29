"""
Вася решил передать Пете шифрограмму.
Поскольку о промышленных шифрах Вася ничего не знает,
он решил зашифровать сообщение следующим образом: он посылает Пете строку.

Каждый символ строки — либо буква, либо пробел, либо точка «.», либо две точки «..».
Если после какой-то буквы стоит точка, значит, мы оставляем букву без изменений
(об одной точке Вася задумался, чтобы усложнить расшифровку). Саму точку при этом надо удалить.
Если после какой-то буквы стоят две точки, то предыдущий символ надо стереть. Обе точки при этом тоже нужно удалить.
Возможна ситуация, когда сообщение после расшифровки будет пустым.
В качестве результата можно вернуть просто пустую строку.

Примеры шифровок-расшифровок:

абра-кадабра. → абра-кадабра
абраа..-кадабра → абра-кадабра
абраа..-.кадабра → абра-кадабра
абра--..кадабра → абра-кадабра
абрау...-кадабра → абра-кадабра (сначала срабатывает правило двух точек, потом правило одной точки)
абра........ → <пустая строка>
абр......a. → a
1..2.3 → 23
. → <пустая строка>
1....................... → <пустая строка>

Помогите Пете написать программу для расшифровки.
Напишите функцию decrypt, которая принимает на вход шифр в виде строки, а возвращает расшифрованное сообщение.

Программа должна работать через конвейер (pipe):

$ echo  ‘абраа..-.кадабра’ | python3 decrypt.py
абра-кадабра

Команда echo выводит текст (в стандартный поток вывода).
"""

import sys

def remove_symbol(text: str, index_start: int, count_symb: int) -> str:
    '''
    Функция принимает на входе строку text, начальный индекс удаляемых элементов
    и количество удаляемых элементов и возвращает строку без этих элементов
    :param text: строка
    :param index_start: индекс начала удаляемой подстроки
    :param count_symb: количество символов для удаления
    :return: строка, в которой удалили count_symb, начиная с индекса index_start
    '''

    if index_start < 0:
        return text[count_symb:]

    return text[:index_start] + text[index_start + count_symb:]


def remove_two_points(text: str) -> str:
    '''
    Функция принимает на входе строку text и возвращает строку по следующему
    правилу: если в строке есть "..", то символ до двух точек и сами две точки удаляются
    :param text: строка с дешифровкой
    :return: строка, получаемая из строки text по следующему правилу:
    если в строке есть "..", то символ до двух точек и сами две точки удаляются
    '''
    index = text.find('..')

    while index != -1:
        text = remove_symbol(text, index - 1, 3)
        index = text.find('..')

    return text


def remove_one_point(text: str) -> str:
    '''
    Функция принимает на входе строку text и возвращает строку по следующему
    правилу: если в строке есть ".", то эта точка просто удаляется из строки
    :param text: строка с дешифровкой
    :return: строка, получаемая из строки text путем удаления одинарных точек
    '''
    index = text.find('.')

    while index != -1:
        text = remove_symbol(text, index, 1)
        index = text.find('.')
    return text


def decrypt(encryption: str) -> str:
    '''
    Функция принимает на входе строку encryption с дешифровкой и
    возвращает расшифрованную строку
    :param encryption: строка с дешифровкой
    :return: расшифрованная строка
    '''

    new_text = remove_two_points(encryption)
    new_text = remove_one_point(new_text)

    return new_text



if __name__ == '__main__':
    data: str = sys.stdin.read()
    decryption: str = decrypt(data)
    print(decryption)
