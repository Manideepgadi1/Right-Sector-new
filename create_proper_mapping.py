import pandas as pd
import json
import re

# Read the Excel file
df = pd.read_excel('data/NIFTY_Index_Short_Names.xlsx')

# Read the existing summary data
with open('data/summary_data.json', 'r') as f:
    summary_data = json.load(f)

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
        'Nifty HighBeta 50': 'NIFTY HIGH BETA 50',
        'Nifty Fin Service': 'NIFTY FINANCIAL SERVICES',
        'Nifty MS Ind Cons': 'NIFTY INDIA CONSUMPTION',
        'NIFTY500 HEALTH': 'NIFTY HEALTHCARE',
        'NIFTY TOTAL MKT': 'NIFTY TOTAL MARKET',
        'Nifty500 Qlty50': 'NIFTY 500 QUALITY 50',
        'Nifty Sml250 Q50': 'NIFTY SMALLCAP 250 QUALITY 50',
        'NIFTYM150MOMNTM50': 'NIFTY MIDCAP 150 MOMENTUM 50',
        'Nifty500 MQVLv50': 'NIFTY 500 MULTIFACTOR MQVLV 50',
        'NIFTY LARGEMID250': 'NIFTY LARGEMIDCAP 250',
        'Nifty Pvt Bank': 'NIFTY PRIVATE BANK',
        'Nifty FinSer ExBnk': 'NIFTY FINANCIAL SERVICES EX BANK',
        'Nifty MS Fin Serv': 'NIFTY MIDSMALL FINANCIAL SERVICES',
        'Nifty Midcap Sel': 'NIFTY MIDCAP SELECT',
        'Nifty Trans Log': 'NIFTY TRANSPORTATION & LOGISTICS',
        'Nifty Cap Markets': 'NIFTY CAPITAL MARKETS',
        'Nifty MidSml400': 'NIFTY MIDSMALLCAP 400',
        'Nifty Top 15 EW': 'NIFTY TOP 15 EQUAL WEIGHT',
        'Nifty Top 20 EW': 'NIFTY TOP 20 EQUAL WEIGHT',
        'NIFTY SMLCAP 250': 'NIFTY SMALLCAP 250',
        'Nifty500 LMS Eql': 'NIFTY 500 EQUAL WEIGHT',
        'NIFTY MIDSML 400': 'NIFTY MIDSMALLCAP 400',
        'Nifty Ind Tourism': 'NIFTY INDIA TOURISM',
        'NIFTY INFRALOG': 'NIFTY INDIA INFRASTRUCTURE & LOGISTICS',
        'NIFTY100 EQL WGT': 'NIFTY 100 EQUAL WEIGHT',
        'NIFTY FINSRV25 50': 'NIFTY FINANCIAL SERVICES 25/50',
        'NIFTY MULTI MFG': 'NIFTY INDIA MANUFACTURING',
        'NIFTY SMLCAP 100': 'NIFTY SMALLCAP 100',
        'Nifty Div Opps 50': 'NIFTY DIVIDEND OPPORTUNITIES 50',
        'Nifty MidSmCap400': 'NIFTY MIDSMALLCAP 400',
        'Nifty SmallCap250': 'NIFTY SMALLCAP 250',
        'Nifty SmallCap100': 'NIFTY SMALLCAP 100',
        'Nifty MidCap Liq': 'NIFTY MIDCAP LIQUID 15',
        'NIFTY MULTI INFRA': 'NIFTY INDIA INFRASTRUCTURE',
        'NIFTY SMLCAP 50': 'NIFTY SMALLCAP 50',
        'Nifty Consumption': 'NIFTY INDIA CONSUMPTION',
        'NIFTY MICROCAP250': 'NIFTY MICROCAP 250',
        'NIFTY50 EQL WGT': 'NIFTY 50 EQUAL WEIGHT',
        'NIFTY INDIA MFG': 'NIFTY INDIA MANUFACTURING',
        'NIFTY MID SELECT': 'NIFTY MIDCAP SELECT',
        'Nifty New Consump': 'NIFTY INDIA NEW AGE CONSUMPTION',
        'Nifty GrowSect 15': 'NIFTY GROWTH SECTORS 15',
        'Nifty Mid Liq 15': 'NIFTY MIDCAP LIQUID 15',
        'NIFTY50 EQL WGT': 'NIFTY 50 EQUAL WEIGHT',
        'Nifty FinSerExBnk': 'NIFTY FINANCIAL SERVICES EX BANK',
        'Nifty GS 10Yr Cln': 'NIFTY 10 YR BENCHMARK G-SEC',
        'Nifty100 Liq 15': 'NIFTY 100 LIQUID 15',
    }
    
    # Check exact mappings first
    for key in exact_mappings:
        if key.upper() in name.upper():
            return exact_mappings[key].upper()
    
    # Common pattern replacements
    replacements = {
        'CONSR DURBL': 'CONSUMER DURABLES',
        'EQL WGT': 'EQUAL WEIGHT',
        'Corp MAATR': 'INDIA SELECT 5 CORPORATE GROUPS (MAATR)',
        'MIDSML HLTH': 'MIDSMALL HEALTHCARE',
        'M150 QLTY50': 'MIDCAP150 QUALITY 50',
        'ESGSecLdr': 'ESG SECTOR LEADERS',
        'Serv Sector': 'SERVICES SECTOR',
        'MS IT Telcm': 'MIDSMALL IT & TELECOM',
        'Enh ESG': 'Enhanced ESG',
        'CoreHousing': 'Core Housing',
        'TMMQ': 'MULTICAP MOMENTUM QUALITY',
        'Momentm': 'MOMENTUM',
        'NonCyc Cons': 'INDIA CONSUMPTION',
        ' EW': ' EQUAL WEIGHT',
        'Shariah': 'SHARIAH 25',
        'FLEXICAP': 'FLEXICAP QUALITY 30',
        'Alpha 30': 'ALPHA 30',
        'Value 20': 'VALUE 20',
        'FUTURES TR INDEX': '',
    }
    
    for old, new in replacements.items():
        if old in name:
            name = name.replace(old, new)
    
    # Handle number formatting
    name = name.replace('Nifty50 ', 'NIFTY 50 ')
    name = name.replace('Nifty100 ', 'NIFTY 100 ')
    name = name.replace('Nifty200 ', 'NIFTY 200 ')
    name = name.replace('Nifty500 ', 'NIFTY 500 ')
    name = name.replace('NIFTY100 ', 'NIFTY 100 ')
    name = name.replace('NIFTY200 ', 'NIFTY 200 ')
    name = name.replace('NIFTY500 ', 'NIFTY 500 ')
    name = name.replace('NIFTY50 ', 'NIFTY 50 ')
    name = name.replace('NIFTY100', 'NIFTY 100')
    name = name.replace('NIFTY50', 'NIFTY 50')
    
    # Normalize spacing and case
    name = re.sub(r'\s+', ' ', name).strip().upper()
    return name

# Create mapping from cleaned name to category
excel_mapping = {}
for _, row in df.iterrows():
    cleaned = clean_name(row['Index Name'])
    category = row['Category']
    excel_mapping[cleaned] = {'category': category, 'original': row['Index Name']}

print(f"Created mapping for {len(excel_mapping)} indices from Excel")

# Process summary data
new_data = []
matched = 0
unmatched = []

for full_key, percentile in summary_data.items():
    clean_display_name = full_key.replace('tri - ', '').strip()
    cleaned = clean_name(full_key)
    
    # Try exact match
    if cleaned in excel_mapping:
        new_data.append({
            'fullName': clean_display_name,
            'displayName': clean_display_name,
            'percentile': float(percentile),
            'category': excel_mapping[cleaned]['category']
        })
        matched += 1
    else:
        # Try fuzzy matching
        found = False
        best_match = None
        best_score = 0
        
        for excel_name, info in excel_mapping.items():
            # Calculate similarity score
            if excel_name in cleaned or cleaned in excel_name:
                score = min(len(excel_name), len(cleaned))
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
            unmatched.append({'original': full_key, 'cleaned': cleaned})

print(f"\nMatched: {matched}/{len(summary_data)}")
print(f"Unmatched: {len(unmatched)} (assigned to Thematic)")

if unmatched:
    print("\nUnmatched indices:")
    for item in unmatched[:10]:
        print(f"  - {item['original']}")

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
