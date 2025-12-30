import pandas as pd
import json
import re

# Read the Excel file for categories
df = pd.read_excel('data/NIFTY_Index_Short_Names.xlsx')

# Read the existing summary data
with open('data/summary_data.json', 'r') as f:
    summary_data = json.load(f)

# Create new data structure with full names (no short names)
new_data = []

def normalize_for_matching(name):
    """Normalize name for fuzzy matching"""
    name = name.replace('tri - ', '').strip()
    name = re.sub(r'\s+', ' ', name)
    name = name.upper()
    # Remove common variations
    name = name.replace('INDEX', '').strip()
    return name

# Create mapping from normalized full name to category
category_mapping = {}
excel_names = {}
for _, row in df.iterrows():
    full_name = str(row['Index Name']).strip()
    normalized = normalize_for_matching(full_name)
    category = row['Category']
    category_mapping[normalized] = category
    excel_names[normalized] = full_name

print(f"Created mapping for {len(category_mapping)} indices from Excel")

# Process summary data
matched = 0
unmatched = []
unmatched_details = []

for full_key, percentile in summary_data.items():
    clean_name = full_key.replace('tri - ', '').strip()
    normalized = normalize_for_matching(full_key)
    
    # Try exact match first
    if normalized in category_mapping:
        new_data.append({
            'fullName': clean_name,
            'displayName': clean_name,
            'percentile': float(percentile),
            'category': category_mapping[normalized]
        })
        matched += 1
    else:
        # Try partial matching with better logic
        found = False
        best_match = None
        best_match_len = 0
        
        for mapped_name, category in category_mapping.items():
            # Check if one is substring of other
            if mapped_name in normalized or normalized in mapped_name:
                # Prefer longer matches
                match_len = min(len(mapped_name), len(normalized))
                if match_len > best_match_len:
                    best_match = category
                    best_match_len = match_len
        
        if best_match:
            new_data.append({
                'fullName': clean_name,
                'displayName': clean_name,
                'percentile': float(percentile),
                'category': best_match
            })
            matched += 1
        else:
            # Assign to Thematic by default
            new_data.append({
                'fullName': clean_name,
                'displayName': clean_name,
                'percentile': float(percentile),
                'category': 'Thematic'
            })
            unmatched.append(clean_name)
            unmatched_details.append({'name': clean_name, 'normalized': normalized})

print(f"\nMatched: {matched}")
print(f"Unmatched: {len(unmatched)} (assigned to Thematic by default)")

if unmatched_details:
    print("\nUnmatched indices:")
    for item in unmatched_details[:15]:
        print(f"  - {item['name']}")
        print(f"    Normalized: {item['normalized']}")

# Save the new data structure
with open('data/indices_with_short_names.json', 'w') as f:
    json.dump(new_data, f, indent=2)

print(f"\nSaved {len(new_data)} indices to data/indices_with_short_names.json")

# Print category breakdown
from collections import Counter
category_counts = Counter([item['category'] for item in new_data])
print("\nCategory breakdown:")
for cat, count in category_counts.items():
    print(f"  {cat}: {count}")

# Print sample output
print("\nSample output:")
for item in new_data[:5]:
    print(f"  {item['displayName']} ({item['category']}): {item['percentile']:.4f}")
