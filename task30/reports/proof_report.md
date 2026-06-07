# Практична робота №30 — Доведення коректності алгоритму індукцією

| Поле         | Значення                                        |
|--------------|-------------------------------------------------|
| **Алгоритм** | `binary_search(arr, target)`                    |
| **Метод**    | Loop invariant (аналог математичної індукції)   |
| **Дата**     | 2026-06-07                                      |
| **Студент**  | Ксенія                                     |



## Крок 1. Вибір алгоритму та параметра n

```
Algorithm:   binary_search(arr, target)
Parameter n: довжина масиву arr  (n = len(arr))
Domain:      n >= 0;  arr відсортований у незхідному порядку
```

**Реалізація:**

```python
def binary_search(arr: list[int], target: int) -> int:
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

---

## Крок 2. Формулювання P(n)

```
P(n): для будь-якого відсортованого масиву arr довжиною n
      та будь-якого цілого target виконується:

      (1) якщо target ∈ arr →  binary_search(arr, target) повертає індекс i,
                                де arr[i] == target  та  0 <= i < n
      (2) якщо target ∉ arr →  binary_search(arr, target) повертає -1
```

**Loop invariant I:**

```
На початку кожної ітерації циклу while:
  "якщо target присутній у arr, то він знаходиться у підмасиві arr[low..high]"
```

Перевірка якості: інваріант містить конкретне математичне твердження про
стан змінних `low` і `high`, його можна перевірити без запуску коду. ✓

---

## Крок 3. Доведення (loop invariant)

### Initialization — до першої ітерації

```
Стан: low = 0,  high = n - 1
      arr[low..high] = arr[0..n-1] = весь масив

Якщо target ∈ arr, він міститься у arr[0..n-1] — тобто у arr[low..high].
Інваріант I виконується. ✓
```

### Maintenance — зберігається на кожній ітерації

```
Припустимо: I виконується на початку ітерації.
            Тобто: якщо target ∈ arr, то target ∈ arr[low..high]

Тіло циклу: mid = (low + high) // 2

Гілка 1: arr[mid] == target
  Функція повертає mid. arr[mid] == target → postcondition виконана. ✓
  (Maintenance не потрібен, виконання завершується.)

Гілка 2: arr[mid] < target
  arr відсортований → ∀ j ≤ mid: arr[j] ≤ arr[mid] < target
  Жоден елемент arr[low..mid] не дорівнює target.
  Тому: target ∈ arr[low..high] ⟹ target ∈ arr[mid+1..high]
  Встановлюємо: low = mid + 1
  Інваріант I зберігається для нових low, high. ✓

Гілка 3: arr[mid] > target
  arr відсортований → ∀ j ≥ mid: arr[j] ≥ arr[mid] > target
  Жоден елемент arr[mid..high] не дорівнює target.
  Тому: target ∈ arr[low..high] ⟹ target ∈ arr[low..mid-1]
  Встановлюємо: high = mid - 1
  Інваріант I зберігається для нових low, high. ✓

Maintenance доведено для всіх трьох гілок. ✓
```

---

## Примітка про дублікати

Якщо у масиві є повторювані значення, алгоритм гарантує повернення деякого
індексу `i` такого, що `arr[i] == target`. Алгоритм не гарантує, що це буде
перший або останній індекс входження; якщо потрібна така властивість, слід
явно модифікувати алгоритм (наприклад, пошук першого/останнього входження).

### Termination — після виходу з циклу

```
Умова виходу: low > high  →  підмасив arr[low..high] порожній.

За інваріантом I: "якщо target ∈ arr, то target ∈ arr[low..high]"
Але arr[low..high] порожній — суперечність.
Отже, target ∉ arr → функція повертає -1. ✓

Завершення за скінченний час:
  Кожна ітерація суворо зменшує розмір підмасиву (high - low):
    Гілка 2: low збільшується → (high - low) зменшується
    Гілка 3: high зменшується → (high - low) зменшується
  Таким чином, цикл завершується не більш ніж за ⌊log₂(n)⌋ + 1 ітерацій. ✓
```

### Підсумок доведення

```
I (Initialization) ∧ I (Maintenance) ∧ (Termination) ⟹ P(n)

Обидва випадки P(n) доведені:
  — target ∈ arr → Гілка 1 у Maintenance → arr[result] == target     ✓
  — target ∉ arr → Termination → return -1                            ✓
```

---

## Крок 4. Ілюстративні тести

### Тест 1 — Initialization (базовий випадок n=0)

```python
def test_empty_array_returns_minus_one():
    """
    Ілюструє: Initialization для n=0.
    low=0, high=-1 → low > high одразу → Termination без жодної ітерації.
    Інваріант: arr[0..-1] порожній → target ∉ arr → return -1.
    """
    result = binary_search([], 5)
    assert result == -1
```

```
Зв'язок з доведенням:
  Initialization: low=0, high=-1.
  arr[low..high] = arr[0..-1] = ∅ → Termination одразу → -1. ✓
```

---

### Тест 2 — Maintenance (збереження інваріанту через кілька ітерацій)

```python
def test_multiple_iterations_invariant():
    """
    Ілюструє: Maintenance через 4 ітерації.
    arr=[1,2,...,15], target=11.

    Ітерація 1: mid=7,  arr[7]=8  < 11 → low=8   | 11 ∈ arr[8..14]  ✓
    Ітерація 2: mid=11, arr[11]=12 > 11 → high=10 | 11 ∈ arr[8..10]  ✓
    Ітерація 3: mid=9,  arr[9]=10 < 11 → low=10   | 11 ∈ arr[10..10] ✓
    Ітерація 4: mid=10, arr[10]=11 == 11 → return 10. ✓
    """
    arr = list(range(1, 16))
    result = binary_search(arr, 11)
    assert result == 10
    assert arr[result] == 11
```

```
Зв'язок з доведенням:
  На кожній з 4 ітерацій 11 ∈ arr[low..high] — інваріант зберігається.
  Maintenance виконується для Гілок 2, 3, 1 послідовно. ✓
```

---

### Тест 3 — Termination (граничне значення)

```python
def test_target_absent_returns_minus_one():
    """
    Ілюструє: Termination для target ∉ arr.
    arr=[1,3,5,7,9], target=4.
    Цикл звужує [low..high] до ∅ → return -1.
    """
    result = binary_search([1, 3, 5, 7, 9], 4)
    assert result == -1
```

```
Зв'язок з доведенням:
  Після звуження: low > high → arr[low..high] = ∅.
  За інваріантом + умовою виходу: target ∉ arr → -1. ✓
```

---

### Evidence — реальний вивід pytest

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3

tests/test_proof.py::TestInitialization::test_empty_array_returns_minus_one PASSED
tests/test_proof.py::TestInitialization::test_single_element_found          PASSED
tests/test_proof.py::TestInitialization::test_single_element_not_found      PASSED
tests/test_proof.py::TestMaintenance::test_target_in_right_half             PASSED
tests/test_proof.py::TestMaintenance::test_target_in_left_half              PASSED
tests/test_proof.py::TestMaintenance::test_target_at_mid_first_iteration    PASSED
tests/test_proof.py::TestMaintenance::test_multiple_iterations_invariant    PASSED
tests/test_proof.py::TestTermination::test_target_absent_returns_minus_one  PASSED
tests/test_proof.py::TestTermination::test_target_less_than_all_elements    PASSED
tests/test_proof.py::TestTermination::test_target_greater_than_all_elements PASSED
tests/test_proof.py::TestBoundaryValues::test_first_element                 PASSED
tests/test_proof.py::TestBoundaryValues::test_last_element                  PASSED
tests/test_proof.py::TestBoundaryValues::test_just_below_range              PASSED
tests/test_proof.py::TestBoundaryValues::test_just_above_range              PASSED
tests/test_proof.py::TestBoundaryValues::test_large_array                   PASSED
tests/test_proof.py::TestBoundaryValues::test_negative_numbers              PASSED
tests/test_proof.py::TestPostcondition::test_postcondition_holds_when_found PASSED
tests/test_proof.py::TestPostcondition::test_postcondition_holds_when_not_found PASSED

============================== 18 passed in 0.05s ==============================
```

---

## Висновок

**Алгоритм:** `binary_search(arr, target)`

**Доведена властивість:**

```
P(n): для всіх відсортованих масивів arr довжиною n >= 0
      та будь-якого цілого target:

  (1) якщо target ∈ arr → повертається індекс i такий, що arr[i] == target
  (2) якщо target ∉ arr → повертається -1
  (3) алгоритм завершується за ⌊log₂(n)⌋ + 1 ітерацій
```

**Метод:** Loop invariant (три кроки — Initialization, Maintenance, Termination)

**Діапазон:** усі n ≥ 0, відсортований масив будь-якої довжини.

Loop invariant `"якщо target ∈ arr, то target ∈ arr[low..high]"` виконується
до першої ітерації (Initialization), зберігається після кожної (Maintenance)
і разом з умовою виходу `low > high` гарантує коректний результат (Termination).
Тестування підтвердило властивість на 18 сценаріях, включаючи граничні випадки. ✓