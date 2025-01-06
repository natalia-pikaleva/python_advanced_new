"""
Напишите код, который выводит сам себя.
Обратите внимание, что скрипт может быть расположен в любом месте.
"""

result = 0
for n in range(1, 11):
    result += n ** 2
print("Сумма квадратов от 1 до 10:", result)

filename = __file__

with open(filename, 'r') as file:
    code = file.read()

print(code)
