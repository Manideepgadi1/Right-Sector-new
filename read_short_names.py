import pandas as pd
import json

# Read the short names Excel file
df = pd.read_excel('data/NIFTY_Index_Short_Names.xlsx')

print(f'Total rows: {len(df)}\n')

# Create a mapping from full name to short name
name_mapping = {}
for idx, row in df.iterrows():
    full_name = row['Index Name']
    short_name = row['Short Name']
    category = row['Category']
    name_mapping[full_name] = short_name
    print(f'{full_name:<50} -> {short_name:<20} [{category}]')

# Save the mapping to a JSON file
with open('data/name_mapping.json', 'w') as f:
    json.dump(name_mapping, f, indent=2)

print('\n\nMapping saved to data/name_mapping.json')
