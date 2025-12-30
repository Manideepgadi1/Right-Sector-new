"""
Update frontend JSON with corrected calculation values
Based on create_proper_mapping.py logic but using CORRECTED_METHOD1_summary.xlsx
"""

import pandas as pd
import json

# Read the Excel file with categories
df = pd.read_excel('data/NIFTY_Index_Short_Names.xlsx')

# Read the CORRECTED summary data (instead of old summary)
df_corrected = pd.read_excel('data/CORRECTED_METHOD1_summary.xlsx')
df_corrected.columns = ['Index', 'Percentile']

# Create corrected summary dict
corrected_summary = {}
for _, row in df_corrected.iterrows():
    corrected_summary[row['Index']] = row['Percentile']

print(f"Loaded {len(corrected_summary)} corrected values")

def clean_name(name):
    """Clean and normalize name for matching"""
    name = str(name).replace('tri - ', '').strip()
    
    # Specific exact mappings first
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
        'NIFTY50 EQL WGT': 'NIFTY50 EQUAL WEIGHT',
        'NIFTY100 EQL WGT': 'NIFTY100 EQUAL WEIGHT',
        'Nifty400 Multicap': 'NIFTY400 MULTICAP',
        'Nifty Svc Sector': 'NIFTY SERVICES SECTOR',
        'Nifty EV & New Age': 'NIFTY EV & NEW AGE AUTOMOTIVE',
        'Nifty Health care': 'NIFTY HEALTHCARE INDEX',
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
    }
    
    if name in exact_mappings:
        return exact_mappings[name]
    
    return name

# Create a mapping of Excel data
excel_mapping = {}

for _, row in df.iterrows():
    index_name = str(row['Index Name']).strip() if pd.notna(row['Index Name']) else ''
    category = str(row['Category']).strip() if pd.notna(row['Category']) else ''
    
    if index_name and category:
        clean_display_name = clean_name(index_name)
        excel_mapping[clean_display_name] = {
            'category': category,
            'display_name': index_name
        }

print(f"Created mapping for {len(excel_mapping)} indices from Excel")

# Match corrected values with Excel mapping
new_data = []
matched = 0
unmatched = []

for csv_name, percentile in corrected_summary.items():
    # Clean the CSV name
    clean_display_name = clean_name(csv_name)
    
    # Try to find in Excel mapping
    if clean_display_name in excel_mapping:
        info = excel_mapping[clean_display_name]
        new_data.append({
            'fullName': clean_display_name,
            'displayName': clean_display_name,
            'percentile': float(percentile),
            'category': info['category']
        })
        matched += 1
    else:
        # Try fuzzy matching
        cleaned = clean_display_name.upper().replace(' ', '').replace('-', '')
        best_match = None
        best_score = 0
        
        for excel_name, info in excel_mapping.items():
            excel_cleaned = excel_name.upper().replace(' ', '').replace('-', '')
            # Calculate similarity score
            if excel_cleaned in cleaned or cleaned in excel_cleaned:
                score = min(len(excel_cleaned), len(cleaned))
                if score > best_score:
                    best_score = score
                    best_match = info
        
        if best_match and best_score > 10:  # Minimum match length
            new_data.append({
                'fullName': clean_display_name,
                'displayName': clean_display_name,
                'percentile': float(percentile),
                'category': best_match['category']
            })
            matched += 1
        else:
            # Default to Thematic
            new_data.append({
                'fullName': clean_display_name,
                'displayName': clean_display_name,
                'percentile': float(percentile),
                'category': 'Thematic'
            })
            unmatched.append(csv_name)

print(f"\nMatched: {matched}/{len(corrected_summary)}")
print(f"Unmatched: {len(unmatched)} (assigned to Thematic)")

if unmatched:
    print("\nUnmatched indices:")
    for item in unmatched[:10]:
        print(f"  - {item}")

# Save the new data structure
with open('data/indices_with_short_names.json', 'w') as f:
    json.dump(new_data, f, indent=2)

print(f"\nSaved {len(new_data)} indices")

# Print category breakdown
from collections import Counter
category_counts = Counter([item['category'] for item in new_data])
print("\nCategory breakdown:")
for cat, count in sorted(category_counts.items()):
    print(f"  {cat}: {count}")

print("\n" + "="*80)
print("✓ Frontend data updated with CORRECTED VALUES!")
print("✓ Refresh your browser at: http://localhost:8000")
print("="*80)
