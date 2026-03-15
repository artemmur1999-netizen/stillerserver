from flask import Flask, request
import os

# Хранение данных в памяти
data = {}

# --- Функции для работы с данными ---
def add_user(name):
    if name not in data:
        data[name] = {}
    return data[name]

def add_file_to_user(user, filename, content):
    if user not in data:
        return False
    data[user][filename] = content
    return True

def get_user_ip():
    if request.headers.get("X-Forwarded-For"):
        ip = request.headers.get("X-Forwarded-For").split(",")[0]
    else:
        ip = request.remote_addr
    return ip

def add_user_ip(user, ip):
    if user not in data:
        return False
    data[user]["ip"] = ip
    return True

def get_user_data(user):
    return data.get(user, None)

def get_file(userdata, filename):
    return userdata.get(filename, None)

# --- Настройка Flask ---
port = int(os.environ.get("PORT", 10000))
app = Flask(__name__)

# --- Маршруты ---
@app.route("/<path:username>")
def add_users(username):
    add_user(username)
    return f"User added: {username}"

@app.route("/fileadd/<user>/<name>", methods=["GET", "POST"])
def add_file_to_users(user, name):
    # Можно передавать содержимое через тело запроса или через URL
    content = request.args.get("content", "")
    if not content and request.method == "POST":
        content = request.get_data(as_text=True)
    success = add_file_to_user(user, name, content)
    if success:
        return f"File added: {name}"
    else:
        return "User not found", 404

@app.route("/add_ip_to_user/<user>")
def add_ip_to_user(user):
    ip = get_user_ip()
    success = add_user_ip(user, ip)
    if success:
        return f"IP {ip} added to user {user}"
    else:
        return "User not found", 404

@app.route("/get_user_data/<user>")
def get_user_info(user):
    userdata = get_user_data(user)
    if userdata is None:
        return "User not found", 404
    # Превращаем словарь в текст
    result = ""
    for key, value in userdata.items():
        result += f"{key}: {value}\n"
    return result

@app.route("/get_file/<user>/<path:filename>")
def get_file_route(user, filename):
    userdata = get_user_data(user)
    if userdata is None:
        return "User not found", 404
    file_content = get_file(userdata, filename)
    if file_content is None:
        return "File not found", 404
    return file_content

@app.route("/users")
def all_users():
    # Возвращаем все данные текстом
    result = ""
    for user, files in data.items():
        result += f"{user}:\n"
        for fname, content in files.items():
            result += f"  {fname}: {content}\n"
    return result

# --- Запуск сервера ---
if __name__ == "__main__":
    app.run(debug=False, port=port)
