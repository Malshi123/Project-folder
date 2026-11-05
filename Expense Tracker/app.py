import json
from multiprocessing import connection
import os
from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change-this-to-a-long-random-text"

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)),"expenses.json")

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",    
        database="Expense_tracker"
    )

def load_expenses():
    try:
        with open(FILE_NAME,"r") as f:
            return json.load(f)
    except FileNotFoundError:
        return[]

def save_expenses(expenses):
    with open(FILE_NAME,"w") as f:
        json.dump(expenses,f)

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, amount, category, note, expense_date AS date "
        "FROM expenses WHERE user_id = %s ORDER BY expense_date DESC, id DESC",
        (session["user_id"],)
    )
    expenses = cursor.fetchall()
    db.close()

    total = 0
    category_totals = {}
    for e in expenses:
        e["amount"] = float(e["amount"])
        total = total + e["amount"]

        category = e["category"]
        if category in category_totals:
            category_totals[category] = category_totals[category] + e["amount"]
        else:
            category_totals[category] = e["amount"]

    return render_template("index.html", expenses=expenses, total=total, category_totals=category_totals)

@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")

    amount = float(request.form["amount"])
    category = request.form["category"]
    note = request.form["note"]
    date = request.form["date"]

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO expenses (user_id, amount, category, note, expense_date) "
        "VALUES (%s, %s, %s, %s, %s)",
        (session["user_id"], amount, category, note, date)
    )
    db.commit()
    db.close()

    return redirect("/")

@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    expenses = load_expenses()

    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(expenses)

    return redirect("/")

@app.route("/edit/<int:index>")
def edit(index):
    expenses = load_expenses()

    if 0 <= index < len(expenses):
        expense = expenses[index]
        return render_template("edit.html", index=index, expense=expense)
    else:
        return redirect("/")

@app.route("/update/<int:index>", methods=["POST"])
def update(index):
    expenses = load_expenses()

    if 0 <= index < len(expenses):
        expenses[index] = {
            "amount": float(request.form["amount"]),
            "category": request.form["category"],
            "note": request.form["note"],
            "date": request.form["date"]
        }
        save_expenses(expenses)

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register(): 
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )
            db.commit()
        except mysql.connector.IntegrityError:
            db.close()
            return render_template("register.html", error="Username already exists. Please choose a different username.")

        db.close()
        return redirect("/login")

    return render_template("register.html", error=None)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        db.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect("/")

        return render_template("login.html", error="Wrong username or password.")

    return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)