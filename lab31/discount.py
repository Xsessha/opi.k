def calculate_discount(
    is_student: bool,
    order_amount: float,
    is_loyal_customer: bool
) -> int:
    """
    Calculates discount percentage based on:
    - student status
    - order amount
    - loyalty status
    """

    if is_student and order_amount >= 1000 and is_loyal_customer:
        return 25

    if is_student and order_amount >= 1000 and not is_loyal_customer:
        return 20

    if is_student and order_amount < 1000 and is_loyal_customer:
        return 15

    if is_student and order_amount < 1000 and not is_loyal_customer:
        return 10

    if not is_student and order_amount >= 1000 and is_loyal_customer:
        return 10

    if not is_student and order_amount >= 1000 and not is_loyal_customer:
        return 5

    if not is_student and order_amount < 1000 and is_loyal_customer:
        return 3

    return 0