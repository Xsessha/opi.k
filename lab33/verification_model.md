# Verification model for `gcd`

Algorithm: `gcd(a, b)` (Euclidean algorithm)

Input constraints:
- `a`: integer in range [-10^6, 10^6]
- `b`: integer in range [-10^6, 10^6]

Expected properties:
- P1: The result divides both inputs. Formally: let g = gcd(a,b). Then (g != 0 => a % g == 0 and b % g == 0) and (g == 0 => a == 0 and b == 0).
- P2: Commutativity: gcd(a,b) == gcd(b,a).
- P3: Abs-invariance: gcd(a,b) == gcd(|a|,|b|).
- P4: Zero identity: gcd(a,0) == |a| (and gcd(0,0) == 0).

Forbidden states:
- Division by zero during assertions (tests must avoid modulo by zero by treating g==0 separately).
- Non-integer inputs.
