

import pytest
import sys
import os
from datetime import datetime


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, users_db, failed_attempts


@pytest.fixture
def client():
    """Тестовий клієнт Flask з чистою базою перед кожним тестом."""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as c:
        with app.app_context():
            users_db.clear()
            failed_attempts.clear()
            yield c


def register_user(client, name="Тест", email="test@test.com", password="testpass1"):
    """Хелпер: реєструє користувача через API."""
    return client.post("/api/register", json={
        "name": name,
        "email": email,
        "password": password,
    })




class TestUF01_Registration:
    """
    Flow: UF-01 — Реєстрація нового користувача
    Сценарії: AC-01 (happy path), AC-02 (дублікат email), AC-03 (слабкий пароль)
    """

    def test_AC01_successful_registration(self, client):
        """
        AC-01: Happy path — успішна реєстрація
        Given: база порожня
        When: надсилається валідний запит реєстрації
        Then: статус 201, повідомлення "Реєстрація успішна", email у базі
        """
        
        response = client.post("/api/register", json={
            "name": "Олексій",
            "email": "alex@test.com",
            "password": "secret123",
        })

     
        assert response.status_code == 201, (
            f"Очікувався статус 201, отримано {response.status_code}. "
            f"Тіло: {response.get_json()}"
        )
        data = response.get_json()
        assert "Реєстрація успішна" in data.get("message", ""), (
            f"Очікувалось повідомлення 'Реєстрація успішна', отримано: {data}"
        )
        assert "alex@test.com" in users_db, (
            "Email не з'явився в базі після реєстрації"
        )

    def test_AC02_duplicate_email(self, client):
        """
        AC-02: Дублікат email
        Given: акаунт alex@test.com вже існує
        When: повторна реєстрація з тим самим email
        Then: статус 409, повідомлення про дублікат
        """

        register_user(client, email="alex@test.com")

       
        response = client.post("/api/register", json={
            "name": "Інший",
            "email": "alex@test.com",
            "password": "another123",
        })

        assert response.status_code == 409, (
            f"Очікувався статус 409 (конфлікт), отримано {response.status_code}"
        )
        data = response.get_json()
        assert "вже зареєстрований" in data.get("error", "").lower() or \
               "вже зареєстрований" in data.get("error", ""), \
            f"Повідомлення про дублікат не знайдено: {data}"

    def test_AC03_weak_password(self, client):
        """
        AC-03: Слабкий пароль (менше 8 символів)
        Given: сервер запущений
        When: пароль "abc" (3 символи)
        Then: статус 400, повідомлення з вимогами до пароля
        """
       
        response = client.post("/api/register", json={
            "name": "Хтось",
            "email": "weak@test.com",
            "password": "abc",
        })

        
        assert response.status_code == 400, (
            f"Очікувався статус 400, отримано {response.status_code}"
        )
        data = response.get_json()
        error_msg = data.get("error", "")
        assert "8 символів" in error_msg or "пароль" in error_msg.lower(), (
            f"Повідомлення про слабкий пароль не знайдено: {data}"
        )




class TestUF02_Login:
    """
    Flow: UF-02 — Авторизація та блокування після 5 невдалих спроб
    Сценарії: AC-04 (happy path), AC-05 (невірний пароль), AC-06 (блокування)
    """

    def test_AC04_successful_login(self, client):
        """
        AC-04: Happy path — успішний вхід
        Given: акаунт bob@test.com існує з паролем "pass2026"
        When: запит /api/login з правильними даними
        Then: статус 200, "Вхід успішний", ім'я у відповіді
        """
        register_user(client, name="Боб", email="bob@test.com", password="pass2026")

        response = client.post("/api/login", json={
            "email": "bob@test.com",
            "password": "pass2026",
        })

        assert response.status_code == 200, (
            f"Очікувався статус 200, отримано {response.status_code}. "
            f"Тіло: {response.get_json()}"
        )
        data = response.get_json()
        assert "Вхід успішний" in data.get("message", ""), (
            f"Повідомлення 'Вхід успішний' не знайдено: {data}"
        )
        assert data.get("name") == "Боб", (
            f"Ім'я у відповіді не відповідає очікуваному: {data}"
        )

    def test_AC05_wrong_password(self, client):
        """
        AC-05: Невірний пароль
        Given: акаунт bob@test.com існує
        When: запит з невірним паролем "wrongpass1"
        Then: статус 401, "Невірний email або пароль"
        """
        register_user(client, name="Боб", email="bob@test.com", password="pass2026")

        response = client.post("/api/login", json={
            "email": "bob@test.com",
            "password": "wrongpass1",
        })

        assert response.status_code == 401, (
            f"Очікувався статус 401, отримано {response.status_code}"
        )
        data = response.get_json()
        assert "Невірний" in data.get("error", ""), (
            f"Повідомлення про помилку не знайдено: {data}"
        )

    def test_AC06_account_lockout_after_5_failures(self, client):
        """
        AC-06: Блокування після 5 невдалих спроб
        Given: акаунт bob@test.com існує
        When: 5 запитів поспіль з невірним паролем
        Then: 5-та спроба → статус 403, "Акаунт заблоковано"
        """
        register_user(client, name="Боб", email="bob@test.com", password="pass2026")

        last_response = None
        for i in range(5):
            last_response = client.post("/api/login", json={
                "email": "bob@test.com",
                "password": f"wrong{i}",
            })

        assert last_response.status_code == 403, (
            f"Очікувався статус 403 після 5 невдалих спроб, "
            f"отримано {last_response.status_code}"
        )
        data = last_response.get_json()
        assert "заблоковано" in data.get("error", "").lower(), (
            f"Повідомлення про блокування не знайдено: {data}"
        )

        correct_attempt = client.post("/api/login", json={
            "email": "bob@test.com",
            "password": "pass2026",
        })
        assert correct_attempt.status_code == 403, (
            "Після блокування навіть правильний пароль мав повертати 403"
        )


class TestUF03_ProfileAndLogout:
    """
    Flow: UF-03 — Оновлення профілю та захист після виходу
    Сценарії: AC-07 (happy path), AC-08 (порожнє ім'я), AC-09 (захист /profile)
    """

    def test_AC07_update_profile_name(self, client):
        """
        AC-07: Happy path — оновлення імені профілю
        Given: акаунт carol@test.com існує
        When: запит /api/profile з новим ім'ям "Кароліна"
        Then: статус 200, "Профіль оновлено", name="Кароліна" у відповіді
        """
        register_user(client, name="Кароль", email="carol@test.com", password="carol2026")

        response = client.post("/api/profile", json={
            "email": "carol@test.com",
            "name": "Кароліна",
        })

        assert response.status_code == 200, (
            f"Очікувався статус 200, отримано {response.status_code}. "
            f"Тіло: {response.get_json()}"
        )
        data = response.get_json()
        assert "Профіль оновлено" in data.get("message", ""), (
            f"Повідомлення 'Профіль оновлено' не знайдено: {data}"
        )
        assert data.get("name") == "Кароліна", (
            f"Нове ім'я не відображається у відповіді: {data}"
        )

    def test_AC08_empty_name_rejected(self, client):
        """
        AC-08: Порожнє ім'я при оновленні профілю
        Given: акаунт carol@test.com існує
        When: запит /api/profile з порожнім рядком
        Then: статус 400, "Ім'я не може бути порожнім"
        """
        register_user(client, name="Кароль", email="carol@test.com", password="carol2026")

        response = client.post("/api/profile", json={
            "email": "carol@test.com",
            "name": "",
        })

        assert response.status_code == 400, (
            f"Очікувався статус 400, отримано {response.status_code}"
        )
        data = response.get_json()
        assert "порожнім" in data.get("error", "") or "ім'я" in data.get("error", "").lower(), (
            f"Повідомлення про порожнє ім'я не знайдено: {data}"
        )

    def test_AC09_profile_protected_after_logout(self, client):
        """
        AC-09: /profile захищений від неавторизованого доступу
        Given: сервер запущений, клієнт без сесії
        When: GET /profile без авторизації
        Then: редирект (302) на /login
        """
        response = client.get("/profile", follow_redirects=False)

        assert response.status_code == 302, (
            f"Очікувався редирект 302, отримано {response.status_code}"
        )
        location = response.headers.get("Location", "")
        assert "login" in location, (
            f"Редирект має вести на /login, але Location: {location}"
        )



class TestEdgeCases:
    """Граничні випадки, що не є основними flows, але важливі для повноти."""

    def test_register_invalid_email_format(self, client):
        """Реєстрація з невалідним форматом email."""
        response = client.post("/api/register", json={
            "name": "Хтось",
            "email": "not-an-email",
            "password": "validpass1",
        })
        assert response.status_code == 400
        data = response.get_json()
        assert "email" in data.get("error", "").lower()

    def test_register_empty_name(self, client):
        """Реєстрація з порожнім ім'ям."""
        response = client.post("/api/register", json={
            "name": "",
            "email": "someone@test.com",
            "password": "validpass1",
        })
        assert response.status_code == 400

    def test_login_nonexistent_user(self, client):
        """Вхід з email, якого немає в базі."""
        response = client.post("/api/login", json={
            "email": "nobody@test.com",
            "password": "somepass1",
        })
        assert response.status_code == 401

    def test_password_no_digit(self, client):
        """Пароль ≥8 символів, але без цифр — має бути відхилений."""
        response = client.post("/api/register", json={
            "name": "Тест",
            "email": "nodigit@test.com",
            "password": "passwordonly",
        })
        assert response.status_code == 400



if __name__ == "__main__":
    print("\n" + "═" * 70)
    print("  ПРАКТИЧНА РОБОТА №32 — Запуск валідаційних тестів")
    print(f"  Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("═" * 70 + "\n")
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--no-header",
        "-q",
    ])
    sys.exit(exit_code)