from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "hemmelig123"

USERNAME = "admin"
PASSWORD = "alphaadmin"

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect("/todo")

    return render_template("login.html")

@app.route("/todo")
def todo():
    if not session.get("logged_in"):
        return redirect("/")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    if not session.get("logged_in"):
        return redirect("/")

    task = request.form["task"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()

    return redirect("/todo")

@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("logged_in"):
        return redirect("/")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/todo")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
