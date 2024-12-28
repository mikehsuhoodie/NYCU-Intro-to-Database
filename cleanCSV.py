import pandas as pd

# Load the original CSV file
input_file = "Data/PurchasesFINAL12312016_original.csv"  # Update with your file name
output_file = "Data/PurchasesFINAL12312016.csv"

# Read the original CSV
df = pd.read_csv(input_file)

# Select the required columns for the new schema
transformed_df = df[[
    "InventoryId",
    "Brand",
    "VendorNumber",
    "PONumber",
    "InvoiceDate",
    "PayDate",
    "Quantity",
    "Dollars"
]]

# Remove duplicate rows based on the primary key columns
primary_key_columns = ["InventoryId", "VendorNumber", "InvoiceDate", "PayDate"]
transformed_df = transformed_df.drop_duplicates(subset=primary_key_columns, keep='first')

# Save the transformed and cleaned data to a new CSV file
transformed_df.to_csv(output_file, index=False)

print(f"Transformed and cleaned CSV saved to: {output_file}")
