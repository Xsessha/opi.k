# Verification Report — `gcd`

Algorithm: `gcd(a, b)`
Tool: hypothesis (property-based testing)
Date: 2026-06-07

Formal contract:
Preconditions:
- `a` and `b` are integers in [-10^6, 10^6]
Postconditions:
- Result is non-negative and divides both inputs.
- Result is the greatest such divisor.
Invariants:
- gcd(a,b) preserved by Euclidean step: gcd(a,b) == gcd(b, a % b)

Verification model:
- See `verification_model.md`.

Results:

Property | Test name | Status | Notes
--------:|:----------|:------:|:----
P1 | `test_divides` | PASS | 200 examples, no counterexample
P2 | `test_commutative` | PASS | 200 examples, no counterexample
P3 | `test_absitivity` | PASS | 200 examples, no counterexample
P4 | `test_gcd_with_zero` | PASS | 200 examples, no counterexample
P5 | `test_nonnegative` | PASS | 200 examples, no counterexample
P6 | `test_leq_max_abs` | PASS | 200 examples, no counterexample
P7 | `test_gcd_self` | PASS | 200 examples, no counterexample
P8 | `test_euclidean_step` | PASS | 200 examples, no counterexample
P9 | `test_add_multiple_invariant` | PASS | 200 examples, no counterexample
P10 | `test_scaling` | PASS | 200 examples, no counterexample
P11 | `test_lcm_gcd_product` | PASS | 200 examples, no counterexample

Counterexample analysis (for any FAIL):
- (no failures observed)

Conclusion:
- Trust level: MEDIUM — properties empirically verified on randomly sampled integers in [-10^6,10^6] with 200 examples per test. This provides strong practical confidence but is not a formal proof for all integers.
