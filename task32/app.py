"""
Система: TaskBoard — простий вебзастосунок для керування задачами.
Функціональність: реєстрація, авторизація, перегляд/оновлення профілю.
"""

from flask import Flask, request, session, redirect, url_for, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = "validation-lab-secret-key-2026"

users_db: dict[str, dict] = {}
failed_attempts: dict[str, int] = {}
MAX_FAILED = 5


BASE_HTML = """
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <title>TaskBoard — {{ title }}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Courier New', monospace; background: #0f0f0f; color: #e0e0e0; min-height: 100vh; }
    .container { max-width: 480px; margin: 80px auto; padding: 40px; border: 1px solid #333; background: #161616; }
    h1 { font-size: 1.6rem; margin-bottom: 24px; color: #fff; letter-spacing: -0.5px; }
    .field { margin-bottom: 16px; }
    label { display: block; font-size: 0.75rem; color: #888; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 1px; }
    input { width: 100%; padding: 10px 14px; background: #1e1e1e; border: 1px solid #333; color: #e0e0e0; font-family: inherit; font-size: 0.95rem; }
    input:focus { outline: none; border-color: #888; }
    button { width: 100%; padding: 12px; background: #e0e0e0; color: #0f0f0f; font-family: inherit; font-size: 0.95rem; font-weight: bold; border: none; cursor: pointer; margin-top: 8px; }
    button:hover { background: #fff; }
    .message { padding: 10px 14px; margin-bottom: 16px; font-size: 0.9rem; }
    .error { background: #2a1010; border-left: 3px solid #c0392b; color: #e74c3c; }
    .success { background: #0a2a10; border-left: 3px solid #27ae60; color: #2ecc71; }
    .nav { display: flex; gap: 20px; margin-bottom: 32px; font-size: 0.8rem; }
    .nav a { color: #888; text-decoration: none; }
    .nav a:hover { color: #fff; }
    .profile-field { padding: 12px 0; border-bottom: 1px solid #222; }
    .profile-field span { color: #888; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 4px; }
  </style>
</head>
<body>
  <div class="container">
    {% if session.user %}
    <nav class="nav">
      <a href="{{ url_for('profile') }}">профіль</a>
      <a href="{{ url_for('logout') }}">вихід</a>
    </nav>
    {% else %}
    <nav class="nav">
      <a href="{{ url_for('login_page') }}">вхід</a>
      <a href="{{ url_for('register_page') }}">реєстрація</a>
    </nav>
    {% endif %}
    {{ content | safe }}
  </div>
</body>
</html>
"""

def render(title, content, **kwargs):
    from flask import session as s
    return render_template_string(BASE_HTML, title=title, content=content, session=s, url_for=url_for, **kwargs)



def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

def is_strong_password(password: str) -> bool:
    """Мінімум 8 символів, хоча б одна цифра."""
    return len(password) >= 8 and any(c.isdigit() for c in password)

def is_locked(email: str) -> bool:
    return failed_attempts.get(email, 0) >= MAX_FAILED



@app.route("/")
def index():
    if session.get("user"):
        return redirect(url_for("profile"))
    return redirect(url_for("login_page"))



@app.route("/register", methods=["GET"])
def register_page():
    content = """
    <h1>Реєстрація</h1>
    <form method="POST" action="/register">
      <div class="field"><label>Ім'я</label><input name="name" required></div>
      <div class="field"><label>Email</label><input name="email" type="email" required></div>
      <div class="field"><label>Пароль</label><input name="password" type="password" required></div>
      <button type="submit">Зареєструватись</button>
    </form>
    """
    return render("Реєстрація", content)

@app.route("/register", methods=["POST"])
def register():
    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not name:
        return render("Реєстрація", '<p class="message error">Ім\'я не може бути порожнім</p>' + _reg_form()), 400
    if not is_valid_email(email):
        return render("Реєстрація", '<p class="message error">Невірний формат email</p>' + _reg_form()), 400
    if email in users_db:
        return render("Реєстрація", '<p class="message error">Email вже зареєстрований</p>' + _reg_form()), 409
    if not is_strong_password(password):
        return render("Реєстрація",
            '<p class="message error">Пароль має містити мінімум 8 символів та хоча б одну цифру</p>' + _reg_form()), 400

    users_db[email] = {
        "name": name,
        "email": email,
        "password_hash": generate_password_hash(password),
    }
    session["user"] = email
    return redirect(url_for("profile"))

def _reg_form():
    return """
    <form method="POST" action="/register">
      <div class="field"><label>Ім'я</label><input name="name"></div>
      <div class="field"><label>Email</label><input name="email" type="email"></div>
      <div class="field"><label>Пароль</label><input name="password" type="password"></div>
      <button type="submit">Зареєструватись</button>
    </form>"""



@app.route("/login", methods=["GET"])
def login_page():
    content = """
    <h1>Вхід</h1>
    <form method="POST" action="/login">
      <div class="field"><label>Email</label><input name="email" type="email" required></div>
      <div class="field"><label>Пароль</label><input name="password" type="password" required></div>
      <button type="submit">Увійти</button>
    </form>
    """
    return render("Вхід", content)

@app.route("/login", methods=["POST"])
def login():
    email    = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if is_locked(email):
        return render("Вхід",
            '<p class="message error">Акаунт заблоковано після 5 невдалих спроб</p>'), 403

    user = users_db.get(email)
    if not user or not check_password_hash(user["password_hash"], password):
        failed_attempts[email] = failed_attempts.get(email, 0) + 1
        remaining = MAX_FAILED - failed_attempts[email]
        msg = f'<p class="message error">Невірний email або пароль. Залишилось спроб: {remaining}</p>'
        if is_locked(email):
            msg = '<p class="message error">Акаунт заблоковано після 5 невдалих спроб</p>'
        return render("Вхід", msg), 401

    failed_attempts[email] = 0
    session["user"] = email
    return redirect(url_for("profile"))



@app.route("/profile", methods=["GET"])
def profile():
    if not session.get("user"):
        return redirect(url_for("login_page"))
    user = users_db[session["user"]]
    content = f"""
    <h1>Профіль</h1>
    <div class="profile-field"><span>Ім'я</span>{user['name']}</div>
    <div class="profile-field"><span>Email</span>{user['email']}</div>
    <br>
    <h1>Редагувати ім'я</h1>
    <form method="POST" action="/profile">
      <div class="field"><label>Нове ім'я</label><input name="name" value="{user['name']}"></div>
      <button type="submit">Зберегти</button>
    </form>
    """
    return render("Профіль", content)

@app.route("/profile", methods=["POST"])
def profile_update():
    if not session.get("user"):
        return redirect(url_for("login_page"))
    email = session["user"]
    name  = request.form.get("name", "").strip()
    if not name:
        return render("Профіль", '<p class="message error">Ім\'я не може бути порожнім</p>'), 400
    users_db[email]["name"] = name
    content = f'<p class="message success">Профіль оновлено. Ім\'я: {name}</p>'
    return render("Профіль", content)



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))



@app.route("/api/register", methods=["POST"])
def api_register():
    data     = request.get_json() or {}
    name     = data.get("name", "").strip()
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name:
        return jsonify({"error": "Ім'я не може бути порожнім"}), 400
    if not is_valid_email(email):
        return jsonify({"error": "Невірний формат email"}), 400
    if email in users_db:
        return jsonify({"error": "Email вже зареєстрований"}), 409
    if not is_strong_password(password):
        return jsonify({"error": "Пароль має містити мінімум 8 символів та хоча б одну цифру"}), 400

    users_db[email] = {
        "name": name,
        "email": email,
        "password_hash": generate_password_hash(password),
    }
    return jsonify({"message": "Реєстрація успішна", "email": email}), 201


@app.route("/api/login", methods=["POST"])
def api_login():
    data     = request.get_json() or {}
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if is_locked(email):
        return jsonify({"error": "Акаунт заблоковано після 5 невдалих спроб"}), 403

    user = users_db.get(email)
    if not user or not check_password_hash(user["password_hash"], password):
        failed_attempts[email] = failed_attempts.get(email, 0) + 1
        if is_locked(email):
            return jsonify({"error": "Акаунт заблоковано після 5 невдалих спроб"}), 403
        return jsonify({"error": "Невірний email або пароль"}), 401

    failed_attempts[email] = 0
    with app.test_request_context():
        pass
    return jsonify({"message": "Вхід успішний", "name": user["name"]}), 200


@app.route("/api/profile", methods=["POST"])
def api_profile_update():
    data  = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    name  = data.get("name", "").strip()

    if email not in users_db:
        return jsonify({"error": "Користувача не знайдено"}), 404
    if not name:
        return jsonify({"error": "Ім'я не може бути порожнім"}), 400

    users_db[email]["name"] = name
    return jsonify({"message": "Профіль оновлено", "name": name}), 200


@app.route("/api/reset", methods=["POST"])
def api_reset():
    """Скидає стан для тестів."""
    users_db.clear()
    failed_attempts.clear()
    return jsonify({"message": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)