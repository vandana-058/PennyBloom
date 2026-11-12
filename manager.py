
import numpy as np
import pandas as pd


COLUMNS = ["date", "type", "category", "amount", "description"]


class ExpenseManager:
    def __init__(self, data=None):
        if data is None or data.empty:
            self.data = pd.DataFrame(columns=COLUMNS)
        else:
            self.data = data[COLUMNS].copy()

        self.data["amount"] = pd.to_numeric(
            self.data["amount"], errors="coerce"
        )
        self.data = self.data.dropna(subset=["amount"])
        self.data = self.data[self.data["amount"] > 0]
        self.data = self.data.reset_index(drop=True)

    def add_transaction(self, transaction):
        self.data.loc[len(self.data)] = transaction.to_dict()

    def remove_transaction(self, index):
        if 0 <= index < len(self.data):
            self.data = self.data.drop(index).reset_index(drop=True)
            return True
        return False

    def get_total_income(self):
        amounts = self.data.loc[
            self.data["type"] == "Income", "amount"
        ].to_numpy(dtype=float)

        return float(np.sum(amounts))

    def get_total_expenses(self):
        amounts = self.data.loc[
            self.data["type"] == "Expense", "amount"
        ].to_numpy(dtype=float)

        return float(np.sum(amounts))

    def get_balance(self):
        return self.get_total_income() - self.get_total_expenses()

    def get_category_summary(self, month=None):
        expenses = self.data[self.data["type"] == "Expense"].copy()

        if month:
            expenses = expenses[
                expenses["date"].astype(str).str.startswith(month)
            ]

        return expenses.groupby("category")["amount"].sum().sort_values(
            ascending=False
        )

    def get_monthly_summary(self, month):
        monthly = self.data[
            self.data["date"].astype(str).str.startswith(month)
        ]

        income = monthly.loc[
            monthly["type"] == "Income", "amount"
        ].sum()

        expenses = monthly.loc[
            monthly["type"] == "Expense", "amount"
        ].sum()

        return float(income), float(expenses)

    def get_average_expense(self, month=None):
        expenses = self.data[self.data["type"] == "Expense"].copy()

        if month:
            expenses = expenses[
                expenses["date"].astype(str).str.startswith(month)
            ]

        values = expenses["amount"].to_numpy(dtype=float)

        return float(np.mean(values)) if values.size else 0.0

    def get_daily_expenses(self, month=None):
        expenses = self.data[self.data["type"] == "Expense"].copy()

        if month:
            expenses = expenses[
                expenses["date"].astype(str).str.startswith(month)
            ]

        expenses["date"] = pd.to_datetime(
            expenses["date"], errors="coerce"
        )

        expenses = expenses.dropna(subset=["date"])

        return expenses.groupby(
            expenses["date"].dt.strftime("%Y-%m-%d")
        )["amount"].sum().sort_index()

    def check_budget(self, budget, month=None):
        if month:
            _, expenses = self.get_monthly_summary(month)
        else:
            expenses = self.get_total_expenses()

        return {
            "spent": expenses,
            "budget": budget,
            "remaining": budget - expenses,
            "exceeded": expenses > budget
        }
