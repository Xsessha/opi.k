import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from binary_search import binary_search

class TestInitialization:
    """
    Ілюструє крок Initialization у доведенні loop invariant.
    low=0, high=n-1: arr[low..high] — весь масив. Інваріант виконується тривіально.
    """

    def test_empty_array_returns_minus_one(self):
        """
        n = 0: масив порожній.
        Initialization: low=0, high=-1 → low > high одразу → termination.
        Інваріант: arr[0..-1] порожній → target ∉ arr → return -1. ✓
        """
        # Ілюструє: Initialization + Termination для n=0
        result = binary_search([], 5)
        assert result == -1, (
            "Порожній масив: має повертати -1 для будь-якого target"
        )

    def test_single_element_found(self):
        """
        n = 1: масив з одного елементу, target знайдено.
        Initialization: low=0, high=0, mid=0, arr[0]==target → return 0. ✓
        """
        # Ілюструє: Initialization → одразу Гілка 1 (arr[mid]==target)
        result = binary_search([42], 42)
        assert result == 0, (
            "Масив [42], target=42: має повертати індекс 0"
        )

    def test_single_element_not_found(self):
        """
        n = 1: масив з одного елементу, target відсутній.
        Initialization: low=0, high=0, mid=0, arr[0]≠target → low>high → return -1. ✓
        """
        # Ілюструє: Initialization → Гілка 2 або 3 → Termination
        result = binary_search([42], 99)
        assert result == -1, (
            "Масив [42], target=99: має повертати -1"
        )


class TestMaintenance:
    """
    Ілюструє крок Maintenance: інваріант зберігається після кожної ітерації.
    """

    def test_target_in_right_half(self):
        """
        Гілка 2 (arr[mid] < target): low = mid + 1.
        arr=[1,3,5,7,9], target=7.
        Ітерація 1: mid=2, arr[2]=5 < 7 → low=3.
        Ітерація 2: mid=4, arr[4]=9 > 7 → high=3.
        Ітерація 3: mid=3, arr[3]=7 == 7 → return 3. ✓
        Інваріант зберігається на кожному кроці: 7 ∈ arr[low..high].
        """
        arr = [1, 3, 5, 7, 9]
        result = binary_search(arr, 7)
        assert result == 3
        assert arr[result] == 7, (
            "Maintenance (гілка 2): target у правій половині — індекс коректний"
        )

    def test_target_in_left_half(self):
        """
        Гілка 3 (arr[mid] > target): high = mid - 1.
        arr=[2,4,6,8,10], target=2.
        Ітерація 1: mid=2, arr[2]=6 > 2 → high=1.
        Ітерація 2: mid=0, arr[0]=2 == 2 → return 0. ✓
        Інваріант зберігається: 2 ∈ arr[low..high] після звуження.
        """
        arr = [2, 4, 6, 8, 10]
        result = binary_search(arr, 2)
        assert result == 0
        assert arr[result] == 2, (
            "Maintenance (гілка 3): target у лівій половині — індекс коректний"
        )

    def test_target_at_mid_first_iteration(self):
        """
        Гілка 1 (arr[mid] == target) на першій ітерації.
        arr=[1,2,3,4,5], target=3.
        mid=2, arr[2]=3 → return 2 одразу. ✓
        """
        arr = [1, 2, 3, 4, 5]
        result = binary_search(arr, 3)
        assert result == 2
        assert arr[result] == 3, (
            "Maintenance (гілка 1): target на позиції mid → повернуто одразу"
        )

    def test_multiple_iterations_invariant(self):
        """
        Перевірка інваріанту через кілька ітерацій.
        arr=[1..15] (n=15), target=11.
        Ітерація 1: mid=7, arr[7]=8  < 11 → low=8
        Ітерація 2: mid=11, arr[11]=12 > 11 → high=10
        Ітерація 3: mid=9, arr[9]=10 < 11 → low=10
        Ітерація 4: mid=10, arr[10]=11 == 11 → return 10. ✓
        На кожній ітерації 11 ∈ arr[low..high].
        """
        arr = list(range(1, 16))  # [1,2,...,15]
        result = binary_search(arr, 11)
        assert result == 10
        assert arr[result] == 11, (
            "Maintenance через 4 ітерації: інваріант зберігається кожен крок"
        )


class TestTermination:
    """
    Ілюструє крок Termination: коли low > high, target точно відсутній.
    """

    def test_target_absent_returns_minus_one(self):
        """
        target ∉ arr → Termination: low > high → return -1. ✓
        arr=[1,3,5,7,9], target=4.
        Цикл звужує підмасив до порожнього, не знаходить 4 → return -1.
        """
        result = binary_search([1, 3, 5, 7, 9], 4)
        assert result == -1, (
            "Termination: target=4 відсутній → повертає -1"
        )

    def test_target_less_than_all_elements(self):
        """
        target менший за всі елементи → Гілка 3 кожну ітерацію →
        high зменшується до -1 → low > high → return -1. ✓
        """
        result = binary_search([10, 20, 30, 40, 50], 5)
        assert result == -1, (
            "Termination: target < min(arr) → повертає -1"
        )

    def test_target_greater_than_all_elements(self):
        """
        target більший за всі елементи → Гілка 2 кожну ітерацію →
        low збільшується до n → low > high → return -1. ✓
        """
        result = binary_search([10, 20, 30, 40, 50], 100)
        assert result == -1, (
            "Termination: target > max(arr) → повертає -1"
        )



class TestBoundaryValues:
    """
    Граничний аналіз: перевірка першого, останнього елементу та меж масиву.
    """

    def test_first_element(self):
        """Target — перший елемент масиву (індекс 0)."""
        arr = [1, 3, 5, 7, 9]
        result = binary_search(arr, 1)
        assert result == 0
        assert arr[result] == 1

    def test_last_element(self):
        """Target — останній елемент масиву (індекс n-1)."""
        arr = [1, 3, 5, 7, 9]
        result = binary_search(arr, 9)
        assert result == 4
        assert arr[result] == 9

    def test_just_below_range(self):
        """Target на одиницю менший за мінімум → має повертати -1."""
        arr = [5, 10, 15, 20]
        result = binary_search(arr, 4)
        assert result == -1

    def test_just_above_range(self):
        """Target на одиницю більший за максимум → має повертати -1."""
        arr = [5, 10, 15, 20]
        result = binary_search(arr, 21)
        assert result == -1

    def test_large_array(self):
        """
        n = 1000: перевірка O(log n) — цикл виконується ≤ 10 ітерацій.
        Ілюструє: Termination гарантований для великих n.
        """
        arr = list(range(0, 2000, 2))  # [0, 2, 4, ..., 1998]
        # target є в масиві
        result = binary_search(arr, 500)
        assert result == 250
        assert arr[result] == 500
        # target відсутній
        result2 = binary_search(arr, 501)
        assert result2 == -1

    def test_negative_numbers(self):
        """Масив з від'ємних чисел — інваріант та доведення не залежать від знаку."""
        arr = [-10, -7, -3, 0, 4, 8]
        assert binary_search(arr, -7) == 1
        assert binary_search(arr, 0) == 3
        assert binary_search(arr, 5) == -1



class TestPostcondition:
    """
    Перевіряє, що для будь-якого знайденого результату виконується postcondition:
    arr[result] == target.
    """

    def test_postcondition_holds_when_found(self):
        """
        Якщо result >= 0, то arr[result] == target (postcondition P1).
        """
        arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
        targets_in_arr = [2, 8, 23, 72, 91]
        for t in targets_in_arr:
            result = binary_search(arr, t)
            assert result >= 0, f"target={t} має бути знайдений"
            assert arr[result] == t, (
                f"Postcondition: arr[{result}] має дорівнювати {t}"
            )

    def test_postcondition_holds_when_not_found(self):
        """
        Якщо result == -1, то target ∉ arr (postcondition P2).
        """
        arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
        targets_not_in_arr = [1, 3, 10, 50, 100]
        for t in targets_not_in_arr:
            result = binary_search(arr, t)
            assert result == -1, f"target={t} має бути відсутній"
            assert t not in arr, (
                f"Postcondition: target={t} справді відсутній у масиві"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])