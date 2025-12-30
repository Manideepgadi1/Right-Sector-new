import pandas as pd

# Read the Excel file
df = pd.read_excel('data/NIFTY_Index_Short_Names.xlsx')

print("Excel file contents:")
print(f"Total rows: {len(df)}")
print("\nFirst 20 entries:")
for idx, row in df.head(20).iterrows():
    print(f"{row['Index Name']:50} -> {row['Category']}")

print("\n" + "="*80)
print("\nLooking for specific indices:")
search_terms = ['SHARIAH', 'TOP 10', 'CONSUMER DUR', 'MAATR', 'ESG', 'QUALITY 50']
for term in search_terms:
    matches = df[df['Index Name'].str.contains(term, case=False, na=False)]
    if len(matches) > 0:
        print(f"\n'{term}' matches:")
        for _, row in matches.iterrows():
            print(f"  {row['Index Name']} -> {row['Category']}")
