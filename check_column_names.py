import pandas as pd

# Check the actual column names in raw CSV
df = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv', nrows=1)
print("Column names in raw CSV (first 20):")
for i, col in enumerate(df.columns[:20]):
    print(f"{i+1:3d}. {col}")

print(f"\nTotal columns: {len(df.columns)}")

# Check Excel names
excel_df = pd.read_excel('data/251229_Final_summary.xlsx')
print("\n" + "=" * 80)
print("Excel SYMBOL names (first 20):")
for i, row in excel_df.head(20).iterrows():
    print(f"{i+1:3d}. {row['SYMBOL']}")

print(f"\nTotal in Excel: {len(excel_df)}")
