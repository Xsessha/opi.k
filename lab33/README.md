# Практична робота No33 — Верифікація коду за допомогою формальних методів

Ця папка містить реалізацію алгоритму НСД (`gcd`) з формальним контрактом, моделлю верифікації і property-based тестами на `hypothesis`.

- `gcd.py` — реалізація з контрактом (preconditions/postconditions/invariants).
- `test_gcd.py` — property-based тести (hypothesis).
- `verification_model.md` — верифікаційна модель (input constraints, properties, forbidden states).
- `verification_report.md` — звіт з результатами верифікації (оновлено після запуску тестів).
- `requirements.txt` — залежності.



результат: `11 passed` (усі property-based тести пройшли).

