"""
Update summary_data.json to use values from the provided Excel file
"""
import pandas as pd
import json

# Read the provided Excel file
df = pd.read_excel('data/251229_Final_summary.xlsx')

# Clean the data
df = df[df['SYMBOL'] != 'date'].dropna()

# Create dictionary
data = dict(zip(df['SYMBOL'], df['final_pct_value']))

# Save to JSON
with open('data/summary_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f'✅ Updated summary_data.json with {len(data)} indices from Excel file')
print(f'\nValue range: {min(data.values()):.4f} to {max(data.values()):.4f}')
print('\n📊 Sample values:')
for i, (k, v) in enumerate(list(data.items())[:5]):
    print(f'  {k}: {v:.4f}')

print('\n📊 Last 5 values:')
for k, v in list(data.items())[-5:]:
    print(f'  {k}: {v:.4f}')
