
class Transaction:
    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = float(amount)
        self.category = category
        self.description = description

    def display_details(self):
        return (
            f"Date: {self.date}\n"
            f"Category: {self.category}\n"
            f"Amount: ₹{self.amount:.2f}\n"
            f"Description: {self.description}"
        )

    def to_dict(self):
        return {
            "date": self.date,
            "type": self.transaction_type,
            "category": self.category,
            "amount": self.amount,
            "description": self.description
        }


class IncomeTransaction(Transaction):
    transaction_type = "Income"

    def display_details(self):
        return "INCOME\n" + super().display_details()


class ExpenseTransaction(Transaction):
    transaction_type = "Expense"

    def display_details(self):
        return "EXPENSE\n" + super().display_details()
