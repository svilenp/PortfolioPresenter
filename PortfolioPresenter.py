import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# === File Picker Dialog ===
root = tk.Tk()
root.withdraw()  # Hide the main window
file_path = filedialog.askopenfilename(
    title="Select portfolio CSV file",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
)
if not file_path:
    print("No file selected. Exiting.")
    exit()

# === User Input ===
include_amounts = input("Include amounts in labels? (y/n): ").strip().lower() == "y"
chart_type = input("Chart type - Pie, Line, or Bar? (p/l/b): ").strip().lower()

# === Load CSV ===
try:
    df = pd.read_csv(file_path)
except Exception:
    df = pd.read_csv(file_path, sep='\t')

df.columns = df.columns.str.strip()  # Strip extra spaces

# === Check required columns ===
required_cols = {'Symbol', 'Current Price', 'Quantity'}
if not required_cols.issubset(df.columns):
    raise ValueError(f"Missing columns: {required_cols - set(df.columns)}")

# === Clean data ===
df['Current Price'] = pd.to_numeric(df['Current Price'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df = df.dropna(subset=['Current Price', 'Quantity', 'Symbol'])

# === Calculate Market Value ===
df['Market Value'] = df['Current Price'] * df['Quantity']

# === Group by Symbol ===
summary = df.groupby('Symbol', as_index=True)['Market Value'].sum().sort_values(ascending=False)
total = summary.sum()

# === Prepare Labels ===
if include_amounts:
    labels = [
        f"{symbol} ({value/total*100:.1f}%, ${value:,.2f})"
        for symbol, value in summary.items()
    ]
else:
    labels = [
        f"{symbol} ({value/total*100:.1f}%)"
        for symbol, value in summary.items()
    ]

# === Plot Chart ===
plt.figure(figsize=(10, 8))
if chart_type == 'p':
    plt.pie(summary.values, labels=labels, startangle=140)
    plt.title('Portfolio Allocation by Market Value')
    plt.axis('equal')
elif chart_type == 'l':
    plt.plot(summary.index, summary.values, marker='o')
    plt.title('Portfolio Market Value by Symbol')
    plt.xlabel('Symbol')
    plt.ylabel('Market Value')
    plt.xticks(rotation=45)
    for i, value in enumerate(summary.values):
        if include_amounts:
            plt.text(i, value, f"${value:,.2f}", ha='center', va='bottom')
        else:
            plt.text(i, value, f"{value/total*100:.1f}%", ha='center', va='bottom')
    plt.tight_layout()
elif chart_type == 'b':
    bars = plt.bar(summary.index, summary.values)
    plt.title('Portfolio Market Value by Symbol')
    plt.xlabel('Symbol')
    plt.ylabel('Market Value')
    plt.xticks(rotation=45)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        if include_amounts:
            plt.text(bar.get_x() + bar.get_width()/2, height, f"${height:,.2f}", ha='center', va='bottom')
        else:
            plt.text(bar.get_x() + bar.get_width()/2, height, f"{height/total*100:.1f}%", ha='center', va='bottom')
    plt.tight_layout()
else:
    print("Invalid chart type. Please enter 'p' for pie, 'l' for line, or 'b' for bar.")
    exit()

plt.tight_layout()
plt.show()
