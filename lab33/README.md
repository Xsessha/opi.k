# Практична робота No33 — Верифікація коду за допомогою формальних методів

Ця папка містить реалізацію алгоритму НСД (`gcd`) з формальним контрактом, моделлю верифікації і property-based тестами на `hypothesis`.

Файли для здачі:
- `gcd.py` — реалізація з контрактом (preconditions/postconditions/invariants).
- `test_gcd.py` — property-based тести (hypothesis).
- `verification_model.md` — верифікаційна модель (input constraints, properties, forbidden states).
- `verification_report.md` — звіт з результатами верифікації (оновлено після запуску тестів).
- `requirements.txt` — залежності.

Швидкий старт (Windows PowerShell):
```powershell
cd lab33
python -m pip install -r requirements.txt
& "C:/Users/Lenovo Yoga/AppData/Local/Programs/Python/Python314/python.exe" -m pytest -q
```

Альтернативно можна запустити скрипт:
- PowerShell: `.
un_tests.ps1`
- Bash (WSL/git-bash): `./run_tests.sh`

Очікуваний результат: `4 passed` (усі property-based тести пройшли).

Порада для здачі: включіть у архів або репозиторій перелічені вище файли та цей `README.md`.

Автор: (ви можете поставити своє ім'я)
Дата: 2026-06-07
