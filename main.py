from flask import Flask, request
import os

data = {}

def add_user(name):
    data[name] = {}

def add_file_to_user(user, filename, cont):
    if not user in data:
        return 0
    else:
        data[user][filename] = cont
        return 1

def get_user_ip():
    ip = request.remote_addr
    return ip

def add_user_ip(user, ip):
    data[user]["ip"] = ip

def get_user_data(user):
    return data[user]

def get_file(userdata, name):
    return userdata[name]

port = int(os.environ.get("PORT", 10000))

app = Flask()

@app.route("/<path:path>")
def add_users(path):
    add_user(path)
    return path

@app.route("/fileadd/<user>/<name>/<path:path>")
def add_file_to_users(user, name, path):
    add_file_to_user(user, name, path)
    return name

@app.route("/add_ip_to_user/<user>")
def addiptouser(user):
    add_user_ip(user, get_user_ip())
    return user

@app.route("/get_user_data/<user>")
def kjg(user):
    return get_user_data(user)

@app.route("/get_file/<user>/<file:path>")
def lgihkj(user, file):
    return get_file(get_user_data(user), file)

@app.route("/users")
def yftghj():
    return data

app.run(debug=False, port=port)
