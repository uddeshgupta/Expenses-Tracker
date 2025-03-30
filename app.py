from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "expenses.db"

# Initialize database
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                amount REAL,
                category TEXT
            )
        ''')
        conn.commit()
        conn.close()

init_db()

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Add Expense
@app.route("/add", methods=["POST"])
def add_expense():
    data = request.json
    name = data.get("name")
    amount = data.get("amount")
    category = data.get("category")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (name, amount, category) VALUES (?, ?, ?)", (name, amount, category))
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully"})

# Fetch all expenses
@app.route("/expenses", methods=["GET"])
def get_expenses():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()

    expense_list = [{"id": row[0], "name": row[1], "amount": row[2], "category": row[3]} for row in expenses]
    return jsonify(expense_list)

# Delete Expense
@app.route("/delete/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Expense deleted successfully"})

# Edit Expense
@app.route("/edit/<int:expense_id>", methods=["PUT"])
def edit_expense(expense_id):
    data = request.json
    name = data.get("name")
    amount = data.get("amount")
    category = data.get("category")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE expenses SET name=?, amount=?, category=? WHERE id=?", (name, amount, category, expense_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense updated successfully"})

if __name__ == "__main__":
    app.run(debug=True)
