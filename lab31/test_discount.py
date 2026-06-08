import pytest
from discount import calculate_discount

# DECISION TABLE TESTS 

# Decision table: Rule 1
def test_rule1_c1_true_c2_true_c3_true():
    # Arrange
    is_student = True
    order_amount = 1500
    is_loyal_customer = True

    # Act
    result = calculate_discount(
        is_student,
        order_amount,
        is_loyal_customer
    )

    # Assert
    assert result == 25


# Decision table: Rule 2
def test_rule2_c1_true_c2_true_c3_false():
    # Arrange
    is_student = True
    order_amount = 1500
    is_loyal_customer = False

    # Act
    result = calculate_discount(
        is_student,
        order_amount,
        is_loyal_customer
    )

    # Assert
    assert result == 20


# Decision table: Rule 3
def test_rule3_c1_true_c2_false_c3_true():
    # Arrange
    is_student = True
    order_amount = 500
    is_loyal_customer = True

    # Act
    result = calculate_discount(
        is_student,
        order_amount,
        is_loyal_customer
    )

    # Assert
    assert result == 15


# Decision table: Rule 4
def test_rule4_c1_true_c2_false_c3_false():
    # Arrange
    is_student = True
    order_amount = 500
    is_loyal_customer = False

    # Act
    result = calculate_discount(
        is_student,
        order_amount,
        is_loyal_customer
    )

    # Assert
    assert result == 10


# Decision table: Rule 5
def test_rule5_c1_false_c2_true_c3_true():
    # Arrange
    is_student = False
    order_amount = 1500
    is_loyal_customer = True

    # Act
    result = calculate_discount(
        is_student,
        order_amount,
        is_loyal_customer
    )

    # Assert
    assert result == 10


# Decision table: Rule 6
def test_rule6_c1_false_c2_true_c3_false():
    # Arrange
    is_student = False
    order_amount = 1500
    is_loyal_customer = False

    # Act
    result = calculate_discount(
        is_student,
        order_amount,
        is_loyal_customer
    )

    # Assert
    assert result == 5


# Decision table: Rule 7
def test_rule7_c1_false_c2_false_c3_true():
    # Arrange
    is_student = False
    order_amount = 500
    is_loyal_customer = True

    # Act
    result = calculate_discount(
        is_student,
        order_amount,
        is_loyal_customer
    )

    # Assert
    assert result == 3


# Decision table: Rule 8
def test_rule8_c1_false_c2_false_c3_false():
    # Arrange
    is_student = False
    order_amount = 500
    is_loyal_customer = False

    # Act
    result = calculate_discount(
        is_student,
        order_amount,
        is_loyal_customer
    )

    # Assert
    assert result == 0

# BOUNDARY VALUE TESTS 

def test_c2_boundary_999_student_loyal():
    assert calculate_discount(True, 999, True) == 15


def test_c2_boundary_1000_student_loyal():
    assert calculate_discount(True, 1000, True) == 25


def test_c2_boundary_1001_student_loyal():
    assert calculate_discount(True, 1001, True) == 25


def test_c2_boundary_999_not_student():
    assert calculate_discount(False, 999, False) == 0


def test_c2_boundary_1000_not_student():
    assert calculate_discount(False, 1000, False) == 5


def test_c2_boundary_1001_not_student():
    assert calculate_discount(False, 1001, False) == 5

# EQUIVALENCE CLASS TESTS 

def test_valid_class_large_amount():
    assert calculate_discount(True, 2500, False) == 20


def test_valid_class_small_amount():
    assert calculate_discount(True, 100, False) == 10


def test_equivalence_c1_false_large_amount():
    assert calculate_discount(False, 2500, True) == 10


def test_equivalence_c1_false_small_amount():
    assert calculate_discount(False, 100, True) == 3


def test_equivalence_c3_true():
    assert calculate_discount(True, 700, True) == 15


def test_equivalence_c3_false():
    assert calculate_discount(True, 700, False) == 10

# ADDITIONAL TESTS 

def test_zero_amount():
    assert calculate_discount(True, 0, True) == 15


def test_amount_one():
    assert calculate_discount(True, 1, True) == 15


def test_very_large_amount_student():
    assert calculate_discount(True, 100000, True) == 25


def test_very_large_amount_non_student():
    assert calculate_discount(False, 100000, False) == 5


def test_exact_threshold_non_student_loyal():
    assert calculate_discount(False, 1000, True) == 10


def test_exact_threshold_student_not_loyal():
    assert calculate_discount(True, 1000, False) == 20