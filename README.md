# PortfolioPresenter
Python Script to Generate a Chart from Yahoo Finance Portfolio CSV 

## This script will:  
Load your Yahoo Finance CSV export.  
Calculate the value of each holding.  
Compute percentage of total.  
Plot a chart of holdings by company.

## Input parameters:
- File Picker Dialog: Select the exported from Yahoo Finance .csv file with the holdings of your portfolio.
- Include amounts in labels? (y/n): Whether to include the amount value or not (yes or no - type 'y' or 'n'). If not - the final chart will show only percentage.
- Chart type - Pie, Line, or Bar? (p/l/b): The type of the output chart (p - pie, l - line, b - bar).

## Requirements
- Python 3.x
- pandas
- matplotlib

## Usage
1. Run `PortfolioPresenter.py`
2. Select your CSV file when prompted
3. Follow the on-screen instructions

## CSV Format
The CSV should have columns: Symbol, Current Price, Quantity (the script is working fine with an export from **yahoo finance**, for other sources, please adapt the .csv accordingly)
