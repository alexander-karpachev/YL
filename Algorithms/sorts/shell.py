
def insertion_sort(array):
    for i in range(len(array)):
        x = array[i]
        j = i - 1
        print(f'step:{i}, x={x}, j={j}')
        print('       ', array)
        while j >= 0 and array[j] > x:
            print(f'copy: array[{j+1}]=array[{j}], {array[j + 1]}->{array[j]}')
            array[j + 1] = array[j]  # "сдвиг" вправо
            print(f'copy:  ', array)
            j = j - 1
        array[j + 1] = x  # Вставка x в отсортированную часть
        print('       ', array)
        i = i + 1


a = [10, 0, 1, 9, 3, 4, 5, 7, 6]

print(a)
insertion_sort(a)
print(a)
