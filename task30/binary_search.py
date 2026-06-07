
def binary_search(arr: list[int], target: int) -> int:
    """
    Бінарний пошук у відсортованому масиві.

    Precondition:
        arr — відсортований список цілих чисел (незхідний порядок)
        target — ціле число для пошуку

    Postcondition:
        Повертає індекс i такий, що arr[i] == target (якщо target ∈ arr)
        Повертає -1 (якщо target ∉ arr)

    Loop invariant:
        Якщо target ∈ arr, то target ∈ arr[low..high]
    """
    # Перевірка передумови (precondition)
    assert arr == sorted(arr), "Precondition: масив має бути відсортований"

    low, high = 0, len(arr) - 1

    # Initialization: arr[low..high] = весь масив → інваріант виконується
    while low <= high:
        # I: якщо target ∈ arr, то target ∈ arr[low..high]
        mid = (low + high) // 2

        if arr[mid] == target:
            # Гілка 1: знайдено → postcondition виконана
            return mid
        elif arr[mid] < target:
            # Гілка 2: arr[mid] < target → жоден елемент у arr[low..mid] не дорівнює target,
            # тому звужуємо пошук до правої половини: low = mid + 1
            low = mid + 1
        else:
            # Гілка 3: arr[mid] > target → жоден елемент у arr[mid..high] не дорівнює target,
            # тому звужуємо пошук до лівої половини: high = mid - 1
            high = mid - 1

    # Termination: low > high → arr[low..high] порожній → target ∉ arr
    return -1