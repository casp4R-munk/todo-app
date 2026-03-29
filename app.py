from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect(url_for("home"))
        else:
            return "Feil brukernavn eller passord"

    return render_template("login.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# HOME (beskyttet)
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

# GET TASKS
@app.route("/tasks", methods=["GET"])
def get_tasks():
    if "user_id" not in session:
        return jsonify([])

    conn = get_db()
    tasks = conn.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in tasks])

# ADD TASK
@app.route("/tasks", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"})

    data = request.get_json()
    text = data.get("text")

    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (text, user_id) VALUES (?, ?)",
        (text, session["user_id"])
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Task lagt til!"})

# DELETE TASK
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Slettet"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
