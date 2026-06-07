from hypothesis import given, settings
import hypothesis.strategies as st

from lab33.gcd import gcd


@given(st.integers(min_value=-10**6, max_value=10**6), st.integers(min_value=-10**6, max_value=10**6))
@settings(max_examples=200)
def test_commutative(a, b):
    """P2: gcd(a, b) == gcd(b, a)"""
    assert gcd(a, b) == gcd(b, a)


@given(st.integers(min_value=-10**6, max_value=10**6), st.integers(min_value=-10**6, max_value=10**6))
@settings(max_examples=200)
def test_absitivity(a, b):
    """P3: gcd(a, b) == gcd(abs(a), abs(b))"""
    assert gcd(a, b) == gcd(abs(a), abs(b))


@given(st.integers(min_value=-10**6, max_value=10**6))
@settings(max_examples=200)
def test_gcd_with_zero(a):
    """P4: gcd(a, 0) == abs(a) (including gcd(0,0)==0)"""
    assert gcd(a, 0) == abs(a)


@given(st.integers(min_value=-10**6, max_value=10**6), st.integers(min_value=-10**6, max_value=10**6))
@settings(max_examples=200)
def test_divides(a, b):
    """P1: result divides both a and b (or result==0 iff a==b==0)"""
    g = gcd(a, b)
    assert (g != 0 and a % g == 0 and b % g == 0) or (g == 0 and a == 0 and b == 0)


@given(st.integers(min_value=-10**6, max_value=10**6), st.integers(min_value=-10**6, max_value=10**6))
@settings(max_examples=200)
def test_nonnegative(a, b):
    """P5: gcd is non-negative"""
    assert gcd(a, b) >= 0


@given(st.integers(min_value=-10**6, max_value=10**6), st.integers(min_value=-10**6, max_value=10**6))
@settings(max_examples=200)
def test_leq_max_abs(a, b):
    """P6: gcd(a,b) <= max(|a|,|b|)"""
    g = gcd(a, b)
    assert g <= max(abs(a), abs(b))


@given(st.integers(min_value=-10**6, max_value=10**6))
@settings(max_examples=200)
def test_gcd_self(a):
    """P7: gcd(a, a) == |a|"""
    assert gcd(a, a) == abs(a)


@given(st.integers(min_value=-10**6, max_value=10**6), st.integers(min_value=-10**6, max_value=10**6))
@settings(max_examples=200)
def test_euclidean_step(a, b):
    """P8: Euclidean invariant gcd(a,b) == gcd(b, a % b) when b!=0"""
    assume = None
    if b == 0:
        return
    assert gcd(a, b) == gcd(b, a % b)


@given(
    st.integers(min_value=-10**6, max_value=10**6),
    st.integers(min_value=-10**6, max_value=10**6),
    st.integers(min_value=-10, max_value=10),
)
@settings(max_examples=200)
def test_add_multiple_invariant(a, b, k):
    """P9: gcd(a, b) == gcd(a, b + k*a) (invariance under adding multiples)"""
    # no precondition needed; check invariance
    assert gcd(a, b) == gcd(a, b + k * a)


@given(
    st.integers(min_value=-10**6, max_value=10**6),
    st.integers(min_value=-10**6, max_value=10**6),
    st.integers(min_value=-10, max_value=10),
)
@settings(max_examples=200)
def test_scaling(a, b, k):
    """P10: gcd(a*k, b*k) == |k| * gcd(a, b) for k != 0"""
    if k == 0:
        return
    assert gcd(a * k, b * k) == abs(k) * gcd(a, b)


@given(st.integers(min_value=-10**6, max_value=10**6), st.integers(min_value=-10**6, max_value=10**6))
@settings(max_examples=200)
def test_lcm_gcd_product(a, b):
    """P11: gcd * lcm == |a*b| (with lcm defined as abs(a*b)//g)"""
    g = gcd(a, b)
    # define lcm as 0 when a or b is 0 (consistent with integer arithmetic)
    if a == 0 or b == 0:
        l = 0
    else:
        l = abs(a * b) // g
    assert g * l == abs(a * b)

