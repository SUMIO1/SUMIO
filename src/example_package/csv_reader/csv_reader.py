from tkinter import filedialog, messagebox

import pandas as pd

required_columns = ['name', 'surname', 'age_category', 'weight', 'country', 'image_url']
df = None


def processCSV(df):
    print(df.head())


def readCSV():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if not file_path or not file_path.endswith('.csv'):
        raise ValueError("Please select a CSV file.")
    try:
        global df
        df = pd.read_csv(file_path)
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Columns {required_columns} are missing in the CSV file.")
        processCSV(df)

    except ValueError as e:
        messagebox.showerror("Error", str(e))


if __name__ == '__main__':
    readCSV()
