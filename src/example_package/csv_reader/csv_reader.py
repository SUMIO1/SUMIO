from src.config.constraints import CONSTRAINTS
from tkinter import filedialog, messagebox
import pandas as pd

df = None


def validateCSV(df):

    # Check if all required columns are present
    if not all(col in df.columns for col in CONSTRAINTS['required_columns']):
        raise ValueError(f"Columns {CONSTRAINTS['required_columns']} are missing in the CSV file.")

    for index, row in df.iterrows():

        # Check if age category is valid
        if row['age_category'] not in CONSTRAINTS['age_categories']:
            raise ValueError(f"Invalid age category {row['age_category']} at row {index + 1}")

        # Check if weight category is valid
        if row['weight_category'] not in CONSTRAINTS['age_categories'][row['age_category']]:
            raise ValueError(f"Invalid weight category {row['weight_category']} at row {index + 1}")

        # Check if weight is within the valid range
        weight = row['weight']
        min_weight = CONSTRAINTS['age_categories'][row['age_category']][row['weight_category']]['min']
        max_weight = CONSTRAINTS['age_categories'][row['age_category']][row['weight_category']]['max']
        if not (min_weight <= weight <= max_weight):
            raise ValueError(f"Weight {weight} is not within the valid range at row {index + 1}")


def processCSV(df):
    print(df.head())


def readCSV():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if not file_path or not file_path.endswith('.csv'):
        messagebox.showerror("Error", "Please select a CSV file.")
        return
    try:
        global df
        df = pd.read_csv(file_path)
        validateCSV(df)
    except ValueError as e:
        messagebox.showerror("Error", str(e))


if __name__ == '__main__':
    readCSV()
