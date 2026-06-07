"""Greatest Common Divisor (GCD) implementation and contract.

This module provides `gcd(a, b)` with an explicit formal contract
used for property-based verification.
"""

def gcd(a: int, b: int) -> int:
    """
    Compute the greatest common divisor of two integers using the
    Euclidean algorithm.

    Preconditions:
    - `a` and `b` are integers.
    - Practical constraint for testing: |a|, |b| <= 10**9.

    Postconditions:
    - The result is a non-negative integer.
    - The result divides both inputs: result | a and result | b.
    - The result is the greatest such divisor.

    Invariants:
    - During the Euclidean loop, gcd(a, b) == gcd(b, a % b).
    """
    a0, b0 = a, b
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a
