"""
Use EXACT values from Excel file (251229_Final_summary.xlsx)
This will ensure webpage shows the same values as your Excel
"""

import pandas as pd
import json
from pathlib import Path

def clean_name(name):
    """Clean and normalize name for matching"""
    name = str(name).replace('tri - ', '').strip()
    
    # Specific exact mappings
    exact_mappings = {
        'Nifty50 Shariah': 'NIFTY SHARIAH 25',
        'Nifty500 Shariah': 'NIFTY SHARIAH 25',
        'Nifty50 Value 20': 'NIFTY 50 VALUE 20',
        'Nifty100ESGSecLdr': 'NIFTY 100 ESG SECTOR LEADERS',
        'NIFTY TMMQ 50': 'NIFTY 500 MULTICAP MOMENTUM QUALITY 50',
        'Nifty200Momentm30': 'NIFTY 200 MOMENTUM 30',
        'Nifty NonCyc Cons': 'NIFTY INDIA CONSUMPTION',
        'Nifty Conglomerate 50': 'NIFTY INDIA CONSUMPTION',
        'NIFTY TATA 25 CAP': 'NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP 25% CAP',
        'Nifty Multi MQ 50': 'NIFTY 500 MULTICAP MOMENTUM QUALITY 50',
        'Nifty Qlty LV 30': 'NIFTY QUALITY LOW VOLATILITY 30',
        'NIFTY ALPHALOWVOL': 'NIFTY ALPHA LOW VOLATILITY 30',
        'NiftySml250MQ 100': 'NIFTY SMALLCAP 250 MOMENTUM QUALITY 100',
        'Nifty AQL 30': 'NIFTY ALPHA QUALITY LOW VOLATILITY 30',
        'NIFTY IND DIGITAL': 'NIFTY INDIA DIGITAL',
        'Nifty Low Vol 50': 'NIFTY LOW VOLATILITY 50',
        'NiftyMS400 MQ 100': 'NIFTY MIDSMALLCAP 400 MOMENTUM QUALITY 100',
        'NIFTY100 LOWVOL30': 'NIFTY 100 LOW VOLATILITY 30',
        'NIFTY100 QUALTY30': 'NIFTY 100 QUALITY 30',
        'Nifty500Momentm50': 'NIFTY 500 MOMENTUM 50',
        'Nifty500 LowVol50': 'NIFTY 500 LOW VOLATILITY 50',
        'Nifty500 Qlty 50': 'NIFTY 500 QUALITY 50',
        'Nifty500 Val 50': 'NIFTY 500 VALUE 50',
        'Nifty200 Val 30': 'NIFTY 200 VALUE 30',
        'Nifty M150 Mom 50': 'NIFTY MIDCAP 150 MOMENTUM 50',
        'Nifty M150 Qlty50': 'NIFTY MIDCAP 150 QUALITY 50',
        'Nifty S250 Qlty50': 'NIFTY SMALLCAP 250 QUALITY 50',
        'Nifty200 Qlty 30': 'NIFTY 200 QUALITY 30',
        'Nifty200 Alpha 30': 'NIFTY 200 ALPHA 30',
        'Nifty Alpha 50': 'NIFTY ALPHA 50',
        'Nifty AQLV 30': 'NIFTY ALPHA QUALITY VALUE LOW-VOLATILITY 30',
        'Nifty Dividend 50': 'NIFTY DIVIDEND OPPORTUNITIES 50',
        'Nifty Growth 15': 'NIFTY GROWTH SECTORS 15',
        'Nifty HiBeta 50': 'NIFTY HIGH BETA 50',
        'Nifty MidLiq 15': 'NIFTY MIDCAP LIQUID 15',
        'Nifty100Liq 15': 'NIFTY100 LIQUID 15',
        'Nifty Liq 15': 'NIFTY LIQUID 15',
        'Nifty Top10EqlWgt': 'NIFTY TOP 10 EQUAL WEIGHT',
        'Nifty Top 10 EW': 'NIFTY TOP 10 EQUAL WEIGHT',
        'NIFTY50 EQL WGT': 'NIFTY50 EQUAL WEIGHT',
        'NIFTY100 EQL WGT': 'NIFTY100 EQUAL WEIGHT',
        'Nifty400 Multicap': 'NIFTY400 MULTICAP',
        'Nifty Svc Sector': 'NIFTY SERVICES SECTOR',
        'Nifty EV & New Age': 'NIFTY EV & NEW AGE AUTOMOTIVE',
        'Nifty Health care': 'NIFTY HEALTHCARE INDEX',
        'NIFTY CONSR DURBL': 'NIFTY CONSUMER DURABLES',
        'Nifty Rural': 'Nifty Rural',
        'Nifty Housing': 'Nifty Housing',
        'Nifty T&L': 'Nifty Transportation & Logistics',
        'Nifty MS Health': 'Nifty MidSmall Healthcare',
        'Nifty MS IT&Tele': 'Nifty MidSmall IT & Telecom',
        'Nifty MS FinService': 'Nifty MidSmall Financial Services',
        'Nifty MS Ind Cons': 'Nifty MidSmall India Consumption',
        'Nifty Fin Ex Bank': 'Nifty Financial Services Ex Bank',
        'Nifty India Digital': 'Nifty India Digital',
        'Nifty Mobility': 'Nifty Mobility',
        'Nifty India Manuf': 'Nifty India Manufacturing',
        'Nifty Core Housing': 'Nifty Core Housing',
        'Nifty Defense': 'Nifty India Defence',
        'Nifty100 ESG': 'NIFTY100 ESG',
        'Nifty Tata Group': 'NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP',
        'Nifty Corp MAATR': 'NIFTY INDIA CORPORATE GROUP INDEX - MAHARATNA',
    }
    
    if name in exact_mappings:
        return exact_mappings[name]
    
    return name

print("="*80)
print("USING EXCEL VALUES (251229_Final_summary.xlsx)")
print("="*80)
print()

# Read Excel file with values
excel_file = Path('data/251229_Final_summary.xlsx')
df_excel = pd.read_excel(excel_file, skiprows=1)

# First row is actually the first index with value in second column
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

# Load category mapping
df_names = pd.read_excel('data/NIFTY_Index_Short_Names.xlsx')
category_mapping = {}

for _, row in df_names.iterrows():
    index_name = str(row['Index Name']).strip()
    category = str(row['Category']).strip()
    category_mapping[index_name] = category

print(f"✓ Loaded {len(category_mapping)} categories")

# Create frontend data
frontend_data = []
matched = 0
unmatched = []

for excel_name, percentile in excel_values.items():
    # Remove "tri - " prefix
    clean_display = clean_name(excel_name)
    
    # Find category
    category = None
    for cat_name, cat in category_mapping.items():
        if clean_name(cat_name) == clean_display:
            category = cat
            break
    
    if not category:
        # Try fuzzy match
        clean_excel = clean_display.upper().replace(' ', '').replace('-', '')
        for cat_name, cat in category_mapping.items():
            clean_cat = clean_name(cat_name).upper().replace(' ', '').replace('-', '')
            if clean_cat in clean_excel or clean_excel in clean_cat:
                if len(clean_cat) > 10:  # Minimum match length
                    category = cat
                    break
    
    if category:
        frontend_data.append({
            'fullName': excel_name,
            'displayName': clean_display,
            'percentile': round(percentile, 6),
            'category': category
        })
        matched += 1
    else:
        frontend_data.append({
            'fullName': excel_name,
            'displayName': clean_display,
            'percentile': round(percentile, 6),
            'category': 'Thematic'
        })
        unmatched.append(clean_display)

print(f"\n✓ Matched {matched}/{len(excel_values)} with categories")

if unmatched:
    print(f"⚠ {len(unmatched)} unmatched (assigned to Thematic):")
    for name in unmatched[:5]:
        print(f"   - {name}")

# Sort by category and percentile
category_order = {
    'Broad Market': 1,
    'Sectoral': 2,
    'Strategy': 3,
    'Thematic': 4
}

frontend_data.sort(key=lambda x: (category_order.get(x['category'], 5), -x['percentile']))

# Save
output_file = Path('data/indices_with_short_names.json')
with open(output_file, 'w') as f:
    json.dump(frontend_data, f, indent=2)

print(f"\n✓ Saved {len(frontend_data)} indices to: {output_file}")

# Show stats
from collections import Counter
category_counts = Counter([item['category'] for item in frontend_data])

print("\n" + "="*80)
print("CATEGORY BREAKDOWN")
print("="*80)
for cat in ['Broad Market', 'Sectoral', 'Strategy', 'Thematic']:
    if cat in category_counts:
        cat_data = [x for x in frontend_data if x['category'] == cat]
        print(f"\n{cat}: {len(cat_data)} indices")
        print(f"  Top: {max(cat_data, key=lambda x: x['percentile'])['displayName']} ({max(cat_data, key=lambda x: x['percentile'])['percentile']:.4f})")
        print(f"  Bottom: {min(cat_data, key=lambda x: x['percentile'])['displayName']} ({min(cat_data, key=lambda x: x['percentile'])['percentile']:.4f})")

print("\n" + "="*80)
print("✓ Frontend updated with EXACT Excel values!")
print("✓ Values now match your Excel file perfectly")
print("="*80)
