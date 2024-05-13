from src.config.constraints import CONSTRAINTS
from tkinter import filedialog, messagebox
import pandas as pd
from pandas import DataFrame
from datetime import datetime

df = None


def validateCSV(df: DataFrame):

    # Check if all required columns are present
    if not all(col in df.columns for col in CONSTRAINTS['required_columns']):
        raise ValueError(f"Columns {CONSTRAINTS['required_columns']} are missing in the CSV file.")

    for index, row in df.iterrows():

        # Check if age category is one of the age categories
        if row['age_category'] not in CONSTRAINTS['age_categories']:
            raise ValueError(f"Invalid age category {row['age_category']} at row {index + 1}")

        # Check if weight category is one of the weight categories
        if row['weight_category'] not in CONSTRAINTS['age_categories'][row['age_category']]:
            raise ValueError(f"Invalid weight category {row['weight_category']} at row {index + 1}")

        # Check if age category is properly assigned
        date_of_birth_str = row['date_of_birth']
        date_of_birt = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - date_of_birt.year - ((today.month, today.day) < (date_of_birt.month, date_of_birt.day))
        min_age = CONSTRAINTS['age_categories'][row['age_category']]['min_age']
        max_age = CONSTRAINTS['age_categories'][row['age_category']]['max_age']
        if not (min_age <= age <= max_age):
            raise ValueError(f"Age {age} is not within the valid range at row {index + 1}")

        # Check if weight category is properly assigned
        weight = row['weight']
        min_weight = CONSTRAINTS['age_categories'][row['age_category']][row['weight_category']]['min']
        max_weight = CONSTRAINTS['age_categories'][row['age_category']][row['weight_category']]['max']
        if not (min_weight <= weight <= max_weight):
            raise ValueError(f"Weight {weight} is not within the valid range at row {index + 1}")


def processCSV(df: DataFrame):
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
