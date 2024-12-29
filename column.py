import os
import pandas as pd

# Correct file path using one of the solutions above
data_dir = r'C:\Users\seash\OneDrive\桌面\學校Study\資料庫\Final_Project\ddddData'

# List all files in the directory
for file_name in os.listdir(data_dir):
    if file_name.endswith('.csv'):  # Check if the file is a CSV
        file_path = os.path.join(data_dir, file_name)
        df = pd.read_csv(file_path)
        print(f"Columns in '{file_name}':")
        print(df.columns)
        print()  # Blank line for better readability
