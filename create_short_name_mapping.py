import pandas as pd
import json

# Read the Excel file with short names
df_short = pd.read_excel('data/NIFTY_Index_Short_Names.xlsx')

# Read the current summary data
with open('data/summary_data.json', 'r') as f:
    summary_data = json.load(f)

# Create mapping from full name to short name
name_mapping = {}
for _, row in df_short.iterrows():
    index_name = row['Index Name']
    short_name = row['Short Name']
    category = row['Category']
    name_mapping[index_name] = {
        'short_name': short_name,
        'category': category
    }

# Create new data with short names
new_summary_data = {}
for key, value in summary_data.items():
    # Remove "tri - " prefix and clean the name
    clean_key = key.replace('tri - ', '').strip()
    
    # Try to find matching entry in the Excel file
    matched = False
    for full_name, mapping in name_mapping.items():
        # Try exact match first
        if clean_key.upper() == full_name.upper():
            short_name = mapping['short_name'].strip()
            category = mapping['category']
            new_summary_data[short_name] = {
                'percentile': value,
                'full_name': full_name,
                'category': category
            }
            matched = True
            break
        # Try partial match with normalization
        clean_full = full_name.upper().replace('&', '').replace('-', '').replace('  ', ' ')
        clean_key_norm = clean_key.upper().replace('&', '').replace('-', '').replace('  ', ' ')
        if clean_key_norm == clean_full:
            short_name = mapping['short_name'].strip()
            category = mapping['category']
            new_summary_data[short_name] = {
                'percentile': value,
                'full_name': full_name,
                'category': category
            }
            matched = True
            break
    
    if not matched:
        print(f"No match found for: {clean_key}")

print(f"\nTotal indices: {len(summary_data)}")
print(f"Matched indices: {len(new_summary_data)}")

# Save the new mapping
with open('data/short_name_summary.json', 'w') as f:
    json.dump(new_summary_data, f, indent=2)

print("\nCreated data/short_name_summary.json")

# Print some samples
print("\nSample data:")
for i, (short_name, data) in enumerate(list(new_summary_data.items())[:10]):
    print(f"{short_name}: {data['percentile']:.4f} ({data['full_name']}) - {data['category']}")
