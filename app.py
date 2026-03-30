from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"


def get_db():
    return sqlite3.connect("database.db")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        db = get_db()
        cur = db.cursor()

        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            return redirect("/login")
        except:
            return "Bruker finnes allerede"

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id, password FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect("/")

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# HOME
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("index.html")


# TASKS
@app.route("/tasks")
def tasks():
    if "user_id" not in session:
        return jsonify([])

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, text FROM tasks WHERE user_id=?", (session["user_id"],))
    rows = cur.fetchall()

    return jsonify([{"id": r[0], "text": r[1]} for r in rows])


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO tasks (user_id, text) VALUES (?, ?)",
                (session["user_id"], data["text"]))
    db.commit()

    return "", 200


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    db.commit()

    return "", 200


if __name__ == "__main__":
    app.run(debug=True)
