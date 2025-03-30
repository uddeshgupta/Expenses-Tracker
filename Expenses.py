import csv
import os

# Define categories
CATEGORIES = ["Food", "Home", "Work", "Fun", "Misc"]

# Load or initialize budget and expenses
BUDGET_FILE = "budget.txt"
EXPENSE_FILE = "expenses.csv"

def load_budget():
    global BUDGET
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as file:
            BUDGET = float(file.read().strip())
    else:
        BUDGET = 10000  # Default budget

def save_budget():
    with open(BUDGET_FILE, "w") as file:
        file.write(str(BUDGET))

expenses = []

def load_expenses():
    global expenses
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            expenses = [row for row in reader]

def save_expenses():
    with open(EXPENSE_FILE, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Amount", "Category"])
        writer.writerows(expenses)

def set_budget():
    global BUDGET
    print(f"Current monthly budget: ${BUDGET:.2f}")
    change_budget = input("Do you want to change it? (yes/no): ")
    if change_budget.lower() == "yes":
        BUDGET = float(input("Enter your new monthly budget: $"))
        save_budget()
        print(f"Monthly budget updated to ${BUDGET:.2f}\n")

def add_expense():
    name = input("Enter expense name: ")
    amount = float(input("Enter expense amount ($): "))
    
    print("Select a category:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")
    category = CATEGORIES[int(input("Enter a category number: ")) - 1]
    
    expenses.append([name, amount, category])
    save_expenses()
    print(f"You've added {name} (${amount:.2f}) to your expenses.\n")

def show_expenses():
    print("\nExpenses by category:")
    category_totals = {cat: 0 for cat in CATEGORIES}
    for _, amount, category in expenses:
        category_totals[category] += float(amount)
    for cat, total in category_totals.items():
        print(f"{cat}: ${total:.2f}")

def show_budget():
    total_spent = sum(float(exp[1]) for exp in expenses)
    remaining = BUDGET - total_spent
    print(f"\nBudget\nYou have ${remaining:.2f} left to spend this month.")
    print(f"That's roughly ${remaining / 30:.2f} per day.\n")

def export_data():
    save_expenses()
    print("\nData exported successfully to expenses.csv!")

def main():
    load_budget()
    load_expenses()
    set_budget()  # Prompt user to change budget only if needed
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. Show Expenses by Category")
        print("3. Show Budget")
        print("4. Export Data")
        print("5. Exit")
        
        choice = input("Select an option: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            show_budget()
        elif choice == "4":
            export_data()
        elif choice == "5":
            print("Exiting... Have a great day!")
            break
        else:
            print("Invalid choice, try again!")

if __name__ == "__main__":
    main()
