import os
import json
from datetime import datetime

class Transaction:
    def __init__(self, amount, category, type, date=None):
        self.amount = amount
        self.category = category
        self.type = type  # 'income' or 'expense'
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            'amount': self.amount,
            'category': self.category,
            'type': self.type,
            'date': self.date
        }

    @staticmethod
    def from_dict(data):
        return Transaction(
            amount=data['amount'],
            category=data['category'],
            type=data['type'],
            date=data['date']
        )

class BudgetTracker:
    def __init__(self, filename='transactions.json'):
        self.filename = filename
        self.transactions = self.load_transactions()

    def load_transactions(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                transactions_data = json.load(file)
                return [Transaction.from_dict(trans) for trans in transactions_data]
        return []

    def save_transactions(self):
        with open(self.filename, 'w') as file:
            json.dump([trans.to_dict() for trans in self.transactions], file, indent=4)

    def add_transaction(self, amount, category, type):
        transaction = Transaction(amount, category, type)
        self.transactions.append(transaction)
        self.save_transactions()

    def calculate_budget(self):
        income = sum(trans.amount for trans in self.transactions if trans.type == 'income')
        expenses = sum(trans.amount for trans in self.transactions if trans.type == 'expense')
        return income - expenses

    def analyze_expenses(self):
        categories = {}
        for trans in self.transactions:
            if trans.type == 'expense':
                if trans.category not in categories:
                    categories[trans.category] = 0
                categories[trans.category] += trans.amount
        return categories

    def list_transactions(self):
        for trans in self.transactions:
            print(f"{trans.date} - {trans.type.capitalize()}: {trans.amount} ({trans.category})")

def main():
    budget_tracker = BudgetTracker()

    while True:
        print("\nBudget Tracker Application")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Calculate Budget")
        print("4. Analyze Expenses")
        print("5. List Transactions")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Income Amount: "))
            category = input("Category: ")
            budget_tracker.add_transaction(amount, category, 'income')
        elif choice == '2':
            amount = float(input("Expense Amount: "))
            category = input("Category: ")
            budget_tracker.add_transaction(amount, category, 'expense')
        elif choice == '3':
            budget = budget_tracker.calculate_budget()
            print(f"Remaining Budget: {budget}")
        elif choice == '4':
            expenses = budget_tracker.analyze_expenses()
            for category, amount in expenses.items():
                print(f"{category}: {amount}")
        elif choice == '5':
            budget_tracker.list_transactions()
        elif choice == '6':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
