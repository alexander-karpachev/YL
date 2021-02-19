def quicksort(arr, left, right):
    if left >= right:
        return
    center = part(arr, left, right)
    quicksort(arr, left, center - 1)
    quicksort(arr, center + 1, right)


def part(arr, left, right):
    i = left - 1
    p = arr[right]
    for j in range(left, right+1):
        if a[j] <= p:
            i += 1
            a[i], a[j] = a[j], a[i]
    return i




def insertion_sort(array):
    for i in range(len(array)):
        x = array[i]
        j = i - 1
        while j >= 0 and array[j] > x:
            array[j + 1] = array[j]  # "сдвиг" вправо
            j -= 1
        array[j + 1] = x  # Вставка x в отсортированную часть


a = [10, 0, 1, 9, 3, 4, 5, 7, 6]

#print(a)
#insertion_sort(a)
#print(a)
print(a)
quicksort(a, 0, len(a)-1)
print(a)
