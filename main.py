
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from transactions import IncomeTransaction, ExpenseTransaction
from manager import ExpenseManager
from storage import (
    load_transactions,
    save_transactions,
    load_budget,
    save_budget
)
from charts import (
    create_pie_chart,
    create_bar_chart,
    create_line_chart
)


# -------------------- THEME --------------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG = "#F6F0FF"
WHITE = "#FFFFFF"
PURPLE = "#A98AD9"
DARK = "#403653"
MUTED = "#81738F"
PINK = "#FFDDE8"
MINT = "#DDF3E4"
BORDER = "#E9DFF5"

CATEGORIES = [
    "Food", "Transport", "Education",
    "Shopping", "Bills", "Health", "Other"
]

manager = ExpenseManager(load_transactions())
budget = load_budget()
current_month = date.today().strftime("%Y-%m")


# -------------------- MAIN WINDOW --------------------

app = ctk.CTk()
app.title("PennyBloom | Expense & Budget Analyzer")
app.geometry("1200x780")
app.minsize(1000, 680)
app.configure(fg_color=BG)

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)


# -------------------- SIDEBAR --------------------

sidebar = ctk.CTkFrame(
    app, width=220, corner_radius=0, fg_color=WHITE
)
sidebar.grid(row=0, column=0, sticky="nsew")
sidebar.grid_propagate(False)

logo = ctk.CTkFrame(sidebar, fg_color="transparent")
logo.pack(fill="x", padx=20, pady=(28, 30))

ctk.CTkLabel(
    logo, text="🌷", font=("Segoe UI Emoji", 30)
).pack(anchor="w")

ctk.CTkLabel(
    logo, text="PennyBloom", font=("Segoe UI", 23, "bold"),
    text_color=DARK
).pack(anchor="w")

ctk.CTkLabel(
    logo, text="Your money, mindfully ♡",
    font=("Segoe UI", 11), text_color=MUTED
).pack(anchor="w", pady=(4, 0))


# -------------------- CONTENT AREA --------------------

content = ctk.CTkFrame(app, fg_color=BG, corner_radius=0)
content.grid(row=0, column=1, sticky="nsew", padx=22, pady=18)
content.grid_columnconfigure(0, weight=1)
content.grid_rowconfigure(1, weight=1)

header = ctk.CTkFrame(content, fg_color="transparent")
header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
header.grid_columnconfigure(0, weight=1)

page_title = ctk.CTkLabel(
    header, text="Your Dashboard",
    font=("Segoe UI", 26, "bold"), text_color=DARK
)
page_title.grid(row=0, column=0, sticky="w")

month_label = ctk.CTkLabel(
    header, text=date.today().strftime("%B %Y"),
    font=("Segoe UI", 13), text_color=MUTED
)
month_label.grid(row=0, column=1, sticky="e", padx=8)


# -------------------- PAGE FRAMES --------------------

pages = {}

for name in ("Dashboard", "Transactions", "Analytics"):
    frame = ctk.CTkScrollableFrame(
        content, fg_color="transparent", corner_radius=0
    )
    frame.grid(row=1, column=0, sticky="nsew")
    frame.grid_remove()
    pages[name] = frame


def show_page(name):
    for frame in pages.values():
        frame.grid_remove()

    pages[name].grid()
    page_title.configure(text={
        "Dashboard": "Your Dashboard 🌷",
        "Transactions": "Your Transactions ♡",
        "Analytics": "Your Spending Insights ✨"
    }[name])

    month_label.configure(
        text=date.today().strftime("%B %Y")
    )

    if name == "Dashboard":
        refresh_dashboard()
    elif name == "Transactions":
        refresh_table()
    elif name == "Analytics":
        refresh_charts()


def nav_button(text, page):
    button = ctk.CTkButton(
        sidebar,
        text=text,
        anchor="w",
        height=44,
        corner_radius=12,
        fg_color="transparent",
        hover_color="#F0E8FC",
        text_color=DARK,
        font=("Segoe UI", 14),
        command=lambda: show_page(page)
    )
    button.pack(fill="x", padx=14, pady=5)


nav_button("⌂   Dashboard", "Dashboard")
nav_button("♡   Transactions", "Transactions")
nav_button("✿   Analytics", "Analytics")

ctk.CTkLabel(
    sidebar,
    text="Little steps add up. ♡",
    text_color=MUTED,
    font=("Segoe UI", 12),
    wraplength=170
).pack(side="bottom", pady=25)


# -------------------- DASHBOARD --------------------

dashboard = pages["Dashboard"]

cards = ctk.CTkFrame(dashboard, fg_color="transparent")
cards.pack(fill="x", pady=(0, 14))

for i in range(3):
    cards.grid_columnconfigure(i, weight=1)


def create_stat_card(parent, column, title, icon, color):
    card = ctk.CTkFrame(
        parent, fg_color=WHITE, corner_radius=18,
        border_width=1, border_color=BORDER
    )
    card.grid(
        row=0, column=column, sticky="ew",
        padx=(0 if column == 0 else 5, 5 if column < 2 else 0),
        pady=3
    )

    ctk.CTkLabel(
        card, text=icon, font=("Segoe UI Emoji", 22)
    ).pack(anchor="w", padx=15, pady=(14, 2))

    ctk.CTkLabel(
        card, text=title, text_color=MUTED,
        font=("Segoe UI", 12)
    ).pack(anchor="w", padx=15)

    value = ctk.CTkLabel(
        card, text="₹0.00", text_color=color,
        font=("Segoe UI", 21, "bold")
    )
    value.pack(anchor="w", padx=15, pady=(4, 16))

    return value


income_value = create_stat_card(
    cards, 0, "Monthly Income", "🌱", "#43865E"
)
expense_value = create_stat_card(
    cards, 1, "Monthly Expenses", "🛍", "#C96F91"
)
balance_value = create_stat_card(
    cards, 2, "Monthly Balance", "💜", DARK
)


# Budget card

budget_card = ctk.CTkFrame(
    dashboard, fg_color=WHITE, corner_radius=18,
    border_width=1, border_color=BORDER
)
budget_card.pack(fill="x", pady=(0, 14))

ctk.CTkLabel(
    budget_card, text="Your monthly budget 🌸",
    font=("Segoe UI", 18, "bold"), text_color=DARK
).pack(anchor="w", padx=18, pady=(15, 5))

budget_summary = ctk.CTkLabel(
    budget_card, text="", font=("Segoe UI", 13),
    text_color=MUTED
)
budget_summary.pack(anchor="w", padx=18, pady=4)

budget_bar = ctk.CTkProgressBar(
    budget_card, height=12, corner_radius=8,
    progress_color=PURPLE, fg_color="#EEE6F7"
)
budget_bar.pack(fill="x", padx=18, pady=8)

budget_status = ctk.CTkLabel(
    budget_card, text="", font=("Segoe UI", 12),
    text_color=MUTED
)
budget_status.pack(anchor="w", padx=18, pady=(0, 8))

budget_form = ctk.CTkFrame(
    budget_card, fg_color="transparent"
)
budget_form.pack(fill="x", padx=18, pady=(4, 16))

budget_entry = ctk.CTkEntry(
    budget_form, placeholder_text="Enter monthly budget (₹)",
    width=220, height=38, corner_radius=10
)
budget_entry.pack(side="left", padx=(0, 8))
budget_entry.insert(0, f"{budget:.2f}")


def update_budget():
    global budget

    try:
        value = float(budget_entry.get().strip())

        if value <= 0:
            raise ValueError

        budget = value
        save_budget(budget)
        refresh_dashboard()
        messagebox.showinfo(
            "Budget updated", "Your monthly budget was saved. ♡"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid budget", "Enter a number greater than zero."
        )


ctk.CTkButton(
    budget_form, text="Save Budget", command=update_budget,
    fg_color=PURPLE, hover_color="#9270C2",
    text_color=WHITE, corner_radius=10, height=38
).pack(side="left")


# Quick actions

quick = ctk.CTkFrame(dashboard, fg_color="transparent")
quick.pack(fill="x", pady=4)

ctk.CTkLabel(
    quick, text="Ready to update your money diary?",
    font=("Segoe UI", 17, "bold"), text_color=DARK
).pack(anchor="w", pady=(4, 10))

ctk.CTkButton(
    quick, text="+  Add a transaction",
    height=44, corner_radius=12,
    fg_color=PURPLE, hover_color="#9270C2",
    command=lambda: show_page("Transactions")
).pack(anchor="w")

ctk.CTkLabel(
    dashboard,
    text="Every little saving is a step forward. ✨",
    text_color=MUTED, font=("Segoe UI", 12)
).pack(anchor="w", pady=22)


def refresh_dashboard():
    income, expenses = manager.get_monthly_summary(current_month)

    income_value.configure(text=f"₹{income:,.2f}")
    expense_value.configure(text=f"₹{expenses:,.2f}")
    balance_value.configure(
        text=f"₹{income - expenses:,.2f}"
    )

    result = manager.check_budget(budget, current_month)
    spent = result["spent"]
    remaining = result["remaining"]

    budget_summary.configure(
        text=f"₹{spent:,.2f} spent out of ₹{budget:,.2f}"
    )

    budget_bar.set(min(max(spent / budget, 0), 1))

    if result["exceeded"]:
        budget_status.configure(
            text=f"Oops! You're ₹{abs(remaining):,.2f} over budget.",
            text_color="#C24165"
        )
    else:
        budget_status.configure(
            text=f"₹{remaining:,.2f} left to spend. You're doing great! ♡",
            text_color="#43865E"
        )


# -------------------- TRANSACTIONS PAGE --------------------

transactions_page = pages["Transactions"]

form = ctk.CTkFrame(
    transactions_page, fg_color=WHITE, corner_radius=18,
    border_width=1, border_color=BORDER
)
form.pack(fill="x", pady=(0, 14))

ctk.CTkLabel(
    form, text="Add a new transaction ✿",
    font=("Segoe UI", 18, "bold"), text_color=DARK
).grid(row=0, column=0, columnspan=2, sticky="w",
       padx=16, pady=(15, 10))

for column in range(2):
    form.grid_columnconfigure(column, weight=1)


def make_field(label, row, column, placeholder="", values=None):
    ctk.CTkLabel(
        form, text=label, text_color=MUTED,
        font=("Segoe UI", 12)
    ).grid(row=row, column=column, sticky="w",
           padx=16, pady=(6, 3))

    if values:
        widget = ctk.CTkComboBox(
            form, values=values, height=36,
            corner_radius=10, fg_color=WHITE,
            border_color=BORDER, text_color=DARK
        )
        widget.set(values[0])
    else:
        widget = ctk.CTkEntry(
            form, placeholder_text=placeholder,
            height=36, corner_radius=10,
            border_color=BORDER
        )

    widget.grid(row=row + 1, column=column,
                sticky="ew", padx=16, pady=(0, 5))
    return widget


date_input = make_field(
    "Date (YYYY-MM-DD)", 1, 0, date.today().isoformat()
)
date_input.insert(0, date.today().isoformat())

type_input = make_field(
    "Transaction type", 1, 1,
    values=["Expense", "Income"]
)
category_input = make_field(
    "Category", 3, 0, values=CATEGORIES
)
amount_input = make_field(
    "Amount (₹)", 3, 1, "e.g. 250"
)
description_input = make_field(
    "Description", 5, 0, "e.g. Lunch at college"
)

# Description spans both columns.
description_input.grid_configure(columnspan=2)

def add_transaction():
    raw_date = date_input.get().strip()
    raw_type = type_input.get().strip()
    raw_category = category_input.get().strip()
    raw_amount = amount_input.get().strip()
    description = description_input.get().strip()

    try:
        datetime.strptime(raw_date, "%Y-%m-%d")

        if raw_type not in ("Income", "Expense"):
            raise ValueError("Choose Income or Expense.")

        if raw_category not in CATEGORIES:
            raise ValueError("Choose a valid category.")

        amount = float(raw_amount)

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if not description:
            raise ValueError("Please enter a description.")

    except ValueError as error:
        messagebox.showerror(
            "Check your entry", str(error) or "Enter a valid date."
        )
        return

    if raw_type == "Income":
        transaction = IncomeTransaction(
            raw_date, amount, raw_category, description
        )
    else:
        transaction = ExpenseTransaction(
            raw_date, amount, raw_category, description
        )

    manager.add_transaction(transaction)

    try:
        save_transactions(manager.data)
    except OSError as error:
        manager.remove_transaction(len(manager.data) - 1)
        messagebox.showerror(
            "Save failed", f"Could not save the transaction:\n{error}"
        )
        return

    amount_input.delete(0, "end")
    description_input.delete(0, "end")

    refresh_table()
    refresh_dashboard()

    messagebox.showinfo(
        "Saved with love ♡", "Your transaction has been added."
    )


ctk.CTkButton(
    form, text="♡  Save Transaction", command=add_transaction,
    fg_color=PURPLE, hover_color="#9270C2",
    height=40, corner_radius=11
).grid(row=7, column=0, columnspan=2,
       sticky="ew", padx=16, pady=(12, 16))


# Transaction table

table_card = ctk.CTkFrame(
    transactions_page, fg_color=WHITE, corner_radius=18,
    border_width=1, border_color=BORDER
)
table_card.pack(fill="both", expand=True)

ctk.CTkLabel(
    table_card, text="Your money diary",
    font=("Segoe UI", 18, "bold"), text_color=DARK
).pack(anchor="w", padx=15, pady=(14, 8))

table_holder = tk.Frame(table_card, bg=WHITE)
table_holder.pack(fill="both", expand=True, padx=12, pady=8)


# -------------------- MONEY DIARY TABLE STYLE --------------------

style = ttk.Style()
style.theme_use("clam")

# Main table appearance
style.configure(
    "Treeview",
    background="#FFFFFF",
    foreground="#403653",
    fieldbackground="#FFFFFF",
    rowheight=38,
    font=("Segoe UI", 11),
    borderwidth=1,
    relief="solid"
)

# Table heading appearance
style.configure(
    "Treeview.Heading",
    background="#E7D8FF",
    foreground="#403653",
    font=("Segoe UI", 11, "bold"),
    padding=(8, 10),
    borderwidth=1,
    relief="solid"
)

# Highlight selected row
style.map(
    "Treeview",
    background=[("selected", "#FFDDE8")],
    foreground=[("selected", "#403653")]
)

columns = ("date", "type", "category", "amount", "description")

table = ttk.Treeview(
    table_holder,
    columns=columns,
    show="headings",
    height=8,
    style="Treeview"
)

# Column headings and centered text
for col, title in zip(
    columns,
    ("Date", "Type", "Category", "Amount (₹)", "Description")
):
    table.heading(col, text=title, anchor="center")

    table.column(
        col,
        anchor="center",
        stretch=True,
        width=130
    )

# Slightly wider description column
table.column("description", width=240, anchor="center")
table.column("amount", width=130, anchor="center")

table.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(
    table_holder,
    orient="vertical",
    command=table.yview
)
scrollbar.pack(side="right", fill="y")

table.configure(yscrollcommand=scrollbar.set)

# Alternate row colors for readability
table.tag_configure("evenrow", background="#FFFFFF")
table.tag_configure("oddrow", background="#F8F3FF")




def refresh_table():
    for item in table.get_children():
        table.delete(item)

    for index, row in manager.data.iterrows():
        tag = "evenrow" if index % 2 == 0 else "oddrow"

        table.insert(
            "",
            "end",
            iid=str(index),
            values=(
                row["date"],
                row["type"],
                row["category"],
                f'{float(row["amount"]):,.2f}',
                row["description"]
            ),
            tags=(tag,)
        )



def delete_transaction():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Select a transaction",
            "Please select a transaction to remove."
        )
        return

    if not messagebox.askyesno(
        "Confirm removal",
        "Are you sure you want to delete this transaction?"
    ):
        return

    # Treeview item IDs match DataFrame row indices.
    indices = sorted(
        [int(item) for item in selected], reverse=True
    )

    original = manager.data.copy()

    for index in indices:
        manager.remove_transaction(index)

    try:
        save_transactions(manager.data)
    except OSError as error:
        manager.data = original
        refresh_table()
        messagebox.showerror(
            "Delete failed", f"Could not save changes:\n{error}"
        )
        return

    refresh_table()
    refresh_dashboard()
    messagebox.showinfo("Updated", "Transaction removed. ♡")


ctk.CTkButton(
    table_card, text="Remove selected transaction",
    command=delete_transaction, fg_color="#F4D8E3",
    hover_color=PINK, text_color="#8D3C5D",
    corner_radius=10, height=36
).pack(anchor="e", padx=14, pady=(0, 14))


# -------------------- ANALYTICS PAGE --------------------

analytics = pages["Analytics"]


def refresh_charts():
    for child in analytics.winfo_children():
        child.destroy()

    income, expenses = manager.get_monthly_summary(current_month)
    categories = manager.get_category_summary(current_month)
    daily = manager.get_daily_expenses(current_month)
    average = manager.get_average_expense(current_month)

    summary = ctk.CTkFrame(
        analytics, fg_color=WHITE, corner_radius=16
    )
    summary.pack(fill="x", pady=(0, 12))

    ctk.CTkLabel(
        summary,
        text=f"Monthly income: ₹{income:,.2f}    |    "
             f"Expenses: ₹{expenses:,.2f}    |    "
             f"Average expense: ₹{average:,.2f}",
        font=("Segoe UI", 13, "bold"), text_color=DARK
    ).pack(padx=14, pady=15)

    chart_specs = [
        ("Spending by Category", create_pie_chart(categories)),
        ("Category Comparison", create_bar_chart(categories)),
        ("Daily Spending Trend", create_line_chart(daily))
    ]

    for title, figure in chart_specs:
        card = ctk.CTkFrame(
            analytics, fg_color=WHITE, corner_radius=16
        )
        card.pack(fill="x", pady=8)

        ctk.CTkLabel(
            card, text=title, font=("Segoe UI", 16, "bold"),
            text_color=DARK
        ).pack(anchor="w", padx=12, pady=(10, 0))

        canvas = FigureCanvasTkAgg(figure, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=6, pady=4)
        plt.close(figure)


# -------------------- START APPLICATION --------------------

refresh_dashboard()
refresh_table()
show_page("Dashboard")

app.mainloop()
