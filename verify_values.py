"""
Verify values match between Excel and webpage
"""
import pandas as pd
import json

# Read Excel
df = pd.read_excel('data/251229_Final_summary.xlsx')
df = df[df['SYMBOL'] != 'date'].dropna()

# Read JSON (what webpage uses)
with open('data/summary_data.json', 'r') as f:
    json_data = json.load(f)

print("=" * 70)
print("VERIFICATION: Excel vs Webpage Values")
print("=" * 70)

# Check some indices visible in the heatmap image
test_indices = [
    'Nifty50', 'NIFTY BANK', 'NIFTY AUTO', 'NIFTY PHARMA', 
    'NIFTY IT', 'NIFTY METAL', 'NIFTY ENERGY', 'NIFTY FMCG',
    'NIFTY REALTY', 'NIFTY MEDIA', 'PSU BANK'
]

print("\n📊 Sample Index Values:")
print("-" * 70)
for search_term in test_indices:
    matches = df[df['SYMBOL'].str.contains(search_term, case=False, na=False)]
    if len(matches) > 0:
        symbol = matches.iloc[0]['SYMBOL']
        excel_val = matches.iloc[0]['final_pct_value']
        webpage_val = json_data.get(symbol, 'NOT FOUND')
        match = "✅" if excel_val == webpage_val else "❌"
        print(f"{match} {symbol}")
        if webpage_val != 'NOT FOUND':
            print(f"   Excel: {excel_val:.4f} | Webpage: {webpage_val:.4f}")
        else:
            print(f"   Excel: {excel_val:.4f} | Webpage: {webpage_val}")

print("\n" + "=" * 70)
print(f"Total indices in Excel: {len(df)}")
print(f"Total indices in Webpage JSON: {len(json_data)}")
print(f"Match: {'✅ YES' if len(df) == len(json_data) else '❌ NO'}")
print("=" * 70)

# Show value distribution
print(f"\n📈 Value Distribution:")
print(f"  Min: {df['final_pct_value'].min():.4f}")
print(f"  Max: {df['final_pct_value'].max():.4f}")
print(f"  Median: {df['final_pct_value'].median():.4f}")
print(f"  Mean: {df['final_pct_value'].mean():.4f}")
