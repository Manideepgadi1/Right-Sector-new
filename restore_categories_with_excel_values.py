"""
Keep the GOOD categories from before, but use EXCEL values
"""

import pandas as pd
import json
from pathlib import Path

print("="*80)
print("KEEPING PREVIOUS CATEGORIES + USING EXCEL VALUES")
print("="*80)
print()

# Load Excel values
excel_file = Path('data/251229_Final_summary.xlsx')
df_excel = pd.read_excel(excel_file, skiprows=1)

excel_values = {}

# Get first value from columns
first_name = df_excel.columns[0]
first_value = df_excel.columns[1] if len(df_excel.columns) > 1 else None

if first_name and first_value is not None:
    excel_values[first_name] = float(first_value)

# Get rest from rows
for _, row in df_excel.iterrows():
    name = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''
    value = row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else None
    
    if name and value is not None:
        excel_values[name] = float(value)

print(f"✓ Loaded {len(excel_values)} values from Excel")

# Load the PREVIOUS good category mapping from indices_with_short_names_backup.json
# Or from Git history if needed
backup_file = Path('data/indices_with_short_names_backup.json')

# If backup doesn't exist, run create_proper_mapping.py first
if not backup_file.exists():
    print("Running create_proper_mapping.py to get good categories...")
    import subprocess
    subprocess.run([
        "D:/Right sector new/.venv/Scripts/python.exe",
        "create_proper_mapping.py"
    ])

# Now load it
with open('data/indices_with_short_names.json', 'r') as f:
    previous_data = json.load(f)

print(f"✓ Loaded {len(previous_data)} previous mappings with good categories")

# Update percentile values with Excel values
updated_data = []
matched = 0
unmatched = []

for item in previous_data:
    full_name = item['fullName']  # Clean name (no "tri - ")
    
    # Try to match with Excel values (Excel has "tri - " prefix)
    excel_key = f"tri - {full_name}"
    
    if excel_key in excel_values:
        # Found match with "tri - " prefix
        updated_data.append({
            'fullName': full_name,
            'displayName': item['displayName'],
            'percentile': round(excel_values[excel_key], 6),
            'category': item['category']
        })
        matched += 1
    elif full_name in excel_values:
        # Found direct match (no prefix)
        updated_data.append({
            'fullName': full_name,
            'displayName': item['displayName'],
            'percentile': round(excel_values[full_name], 6),
            'category': item['category']
        })
        matched += 1
    else:
        # Keep original value if not found in Excel
        updated_data.append(item)
        unmatched.append(full_name)

print(f"\n✓ Updated {matched}/{len(previous_data)} with Excel values")

if unmatched:
    print(f"⚠ {len(unmatched)} kept original values (not in Excel):")
    for name in unmatched[:5]:
        print(f"   - {name}")

# Save
output_file = Path('data/indices_with_short_names.json')
with open(output_file, 'w') as f:
    json.dump(updated_data, f, indent=2)

print(f"\n✓ Saved {len(updated_data)} indices")

# Show stats
from collections import Counter
category_counts = Counter([item['category'] for item in updated_data])

print("\n" + "="*80)
print("CATEGORY BREAKDOWN (KEPT PREVIOUS GOOD CATEGORIES)")
print("="*80)
for cat in ['Broad Market', 'Sectoral', 'Strategy', 'Thematic']:
    if cat in category_counts:
        print(f"{cat}: {category_counts[cat]} indices")

print("\n" + "="*80)
print("✓ Done! Previous categories restored + Excel values used")
print("="*80)
