# 🌷 PennyBloom – Smart Expense & Budget Analyzer

**A pastel-themed desktop application built using Python to manage personal finances, track expenses, analyze spending patterns, and monitor monthly budgets.**

## ✨ About the Project

PennyBloom is a Python-based personal finance management application developed using Object-Oriented Programming (OOP), NumPy, Pandas, Matplotlib, and CustomTkinter.

The application allows users to record income and expenses, organize transactions into categories, monitor monthly budgets, and visualize their financial activities through interactive charts.

It features a soft pastel-lavender interface designed to make expense tracking simple, attractive, and user-friendly.

## 🎯 Project Objectives

- Develop a desktop-based personal expense management application.
- Implement Python classes, objects, and inheritance.
- Use NumPy for numerical calculations and statistical analysis.
- Use Pandas for transaction management and data processing.
- Visualize financial data using Matplotlib.
- Develop an attractive graphical user interface using CustomTkinter.
- Store transaction records using CSV file handling.

## 🚀 Features

### 1. Dashboard
- View total monthly income.
- View total monthly expenses.
- Calculate the remaining balance.
- Monitor monthly budget usage.
- Display budget warnings when spending exceeds the limit.

### 2. Transaction Management
- Add income and expense transactions.
- Select transaction categories.
- Enter transaction dates, amounts, and descriptions.
- View transaction history in a structured table.
- Delete selected transactions.

### 3. Budget Management
- Set a monthly spending budget.
- Calculate remaining budget.
- Monitor spending against the budget.
- Display alerts when the budget is exceeded.

### 4. Data Analysis
- Calculate total income and expenses.
- Calculate average expenses.
- Group expenses by category.
- Generate monthly summaries.
- Analyze daily spending patterns.

### 5. Data Visualization
- **Pie Chart:** Displays category-wise expense distribution.
- **Bar Chart:** Compares spending across different categories.
- **Line Chart:** Displays daily spending trends.

### 6. Data Storage
- Save transactions in CSV format.
- Automatically load previously saved transactions.
- Save budget settings locally.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| CustomTkinter | Modern desktop GUI |
| Tkinter | Table and message dialogs |
| NumPy | Numerical calculations |
| Pandas | Data manipulation and analysis |
| Matplotlib | Data visualization |
| CSV | Transaction storage |

## 📂 Project Structure

```text
PennyBloom/
│
├── main.py
├── transactions.py
├── manager.py
├── storage.py
├── charts.py
├── README.md
├── .gitignore
│
└── data/
    ├── expenses.csv       (generated locally)
    └── budget.txt         (generated locally)
```

The `data` folder and its files are generated automatically when the application saves data. They are excluded from GitHub to protect personal financial records.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- Visual Studio Code (recommended)
- pip package manager

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the project folder

```bash
cd PennyBloom
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
python -m pip install customtkinter numpy pandas matplotlib
```

### Step 6: Run the application

```bash
python main.py
```

The PennyBloom desktop application will launch.

## 📊 Python Concepts Implemented

- Classes and Objects
- Constructors and Instance Attributes
- Inheritance
- Method Overriding
- Encapsulation through class-based organization
- Functions and Conditional Statements
- Exception Handling
- File Handling
- NumPy Arrays and Statistical Operations
- Pandas DataFrames and Grouping
- Matplotlib Data Visualization
- GUI Event Handling

## 🔮 Future Enhancements

- Monthly budget history and comparison.
- Separate income and expense categories.
- Exportable financial reports.
- Advanced filtering and search.
- Monthly and yearly analytics.
- Improved dashboard customization.

## 👩‍💻 Project Information

**Project Name:** PennyBloom – Smart Expense & Budget Analyzer

**Project Type:** Python Mini Project

**Application Type:** Desktop GUI Application

**Programming Language:** Python

**Developed Using:** VS Code

## 💜 Conclusion

PennyBloom demonstrates how Python programming concepts and data analysis libraries can be combined to create a practical desktop application.

It provides an organized way to track financial activities, monitor budgets, and understand spending habits through data visualization.

*Small steps, lovely progress! 🌷*