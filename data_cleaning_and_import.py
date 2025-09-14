import pandas as pd
import numpy as np
from dateutil import parser
from sqlalchemy import create_engine

# Load the CSV file
df = pd.read_csv("sales_transactions.csv")
rows_before = len(df)

# Create a clean copy
df_clean = df.copy()

# Compute any missing values intelligently

# Fill missing total_price
df_clean['total_price'] = df_clean.apply(
    lambda row: row['price_per_unit'] * row['quantity']
    if pd.isna(row['total_price']) and pd.notna(row['price_per_unit']) and pd.notna(row['quantity'])
    else row['total_price'],
    axis=1
)

# Fill missing price_per_unit
df_clean['price_per_unit'] = df_clean.apply(
    lambda row: row['total_price'] / row['quantity']
    if pd.isna(row['price_per_unit']) and pd.notna(row['total_price']) and pd.notna(row['quantity']) and row['quantity'] != 0
    else row['price_per_unit'],
    axis=1
)

# Fill missing quantity
df_clean['quantity'] = df_clean.apply(
    lambda row: row['total_price'] / row['price_per_unit']
    if pd.isna(row['quantity']) and pd.notna(row['total_price']) and pd.notna(row['price_per_unit']) and row['price_per_unit'] != 0
    else row['quantity'],
    axis=1
)

# Drop any rows where values still couldn't be recovered
df_clean.dropna(subset=['price_per_unit', 'quantity', 'total_price'], inplace=True)

# Normalize product names
def normalize_name(name):
    name = name.strip().lower()  
    if 'usb' in name:
        return 'USB-C Cable'
    elif 'headphone' in name:
        return 'Headphones'
    elif 'mouse' in name:
        return 'Mouse'
    else:
        return name.title()

df_clean['product_name'] = df_clean['product_name'].apply(normalize_name)

# Standardize transaction dates
def parse_date(x):
    try:
        return parser.parse(str(x)).strftime('%Y-%m-%d')
    except:
        return np.nan

df_clean['transaction_date'] = df_clean['transaction_date'].apply(parse_date)
df_clean.dropna(subset=['transaction_date'], inplace=True)

# Drop duplicates
df_clean.drop_duplicates(inplace=True)

# Remove outliers
df_clean = df_clean[df_clean['quantity'] < 1000]
df_clean = df_clean[df_clean['total_price'] < 100000]

# Count cleaned rows
rows_after = len(df_clean)

# Save cleaned data to CSV
df_clean.to_csv("cleaned_sales.csv", index=False)
print(f"Rows before cleaning: {rows_before}")
print(f"Rows after cleaning: {rows_after}")
print("Cleaned data saved to cleaned_sales.csv")

# Connect to PostgreSQL
engine = create_engine("postgresql+psycopg2://andreasrafailandrikopoulos@localhost:5432/eshop")

# Upload cleaned data to 'sales' table
df_clean.to_sql("sales", engine, if_exists="replace", index=False)

print("Data successfully imported into 'sales' table.")