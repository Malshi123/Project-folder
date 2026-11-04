import json
import os

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.json")

def save_expenses():
    with open(FILE_NAME, "w") as f:
        json.dump(expenses, f)

def load_expenses():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

expenses = load_expenses()

def add_expense():
    while True:
        try:
            amount = float(input("Enter the expense amount: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for the expense amount.")
            
    category=input("Enter the expense category: ")
    note=input("Enter a note for the expense: ")

    expenses.append({"amount": amount, "category": category, "note": note})
    save_expenses()
    print("Expense added successfully!")

def view_expenses():
    if len(expenses) == 0:
        print("No expenses yet...")
        return

    for i, e in enumerate(expenses, start=1):
        print(i, e["amount"], e["category"], e["note"])

def total_expense():
    total = 0
    for e in expenses:
        total = total + e["amount"]
    print("Total expense: ", total)

def delete_expense():
    if len(expenses ) == 0:
        print("No expenses yet...")
        return

    view_expenses()
    try:
        number = int(input("Enter the expense number to delete: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return
    
    if number < 1 or number > len(expenses):
        print("Invalid expense number")
        return

    expenses.pop(number - 1)
    save_expenses()
    print("Expense deleted successfully!")
    
while True:
    print("\n1. Add expense")
    print("2. View expense")
    print("3. Total expense")
    print("4. Delete expense")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        total_expense()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        break
    else:
        print("Invalid choice")