import pandas as pd

df = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv', nrows=5)
print("First 20 column names from CSV:")
for i, col in enumerate(df.columns[:20]):
    print(f"{i+1}. {col}")

print("\nSearching for common indices:")
search_terms = ['IT', 'Bank', 'AUTO', 'PSU', '500']
for term in search_terms:
    matches = [col for col in df.columns if term.upper() in col.upper()]
    if matches:
        print(f"\n'{term}' matches:")
        for match in matches[:3]:
            print(f"  - {match}")
