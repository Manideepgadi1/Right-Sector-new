import pandas as pd
import json

# Read the short names Excel file
df = pd.read_excel('data/NIFTY_Index_Short_Names.xlsx')
print("Excel columns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print(f"\nTotal rows: {len(df)}")

# Read the existing summary data
with open('data/summary_data.json', 'r') as f:
    summary_data = json.load(f)

print("\nSample summary data keys:")
for i, key in enumerate(list(summary_data.keys())[:5]):
    print(f"  {key}")

# Create mapping from full name to short name
# Assuming Excel has columns like 'Index Name' or 'Full Name' and 'Short Name'
print("\n" + "="*80)
print("Creating name mapping...")
