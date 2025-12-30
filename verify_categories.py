"""
Verify categorization of indices
"""
import json

# Load the actual data
with open('data/summary_data.json', 'r') as f:
    data = json.load(f)

# Define categories based on the user's specification
broad_market = [
    'NIFTY 50', 'NIFTY NEXT 50', 'NIFTY 100', 'NIFTY 200', 'Nifty Total Market', 'NIFTY 500',
    'NIFTY500 MULTICAP 50:25:25', 'NIFTY500 EQUAL WEIGHT', 'NIFTY MIDCAP 150', 'NIFTY MIDCAP 50',
    'Nifty Midcap Select', 'NIFTY MIDCAP 100', 'NIFTY SMALLCAP 250', 'NIFTY SMALLCAP 50',
    'NIFTY SMALLCAP 100', 'NIFTY MICROCAP 250', 'NIFTY LargeMidcap 250', 'NIFTY MIDSMALLCAP 400',
    'NIFTY MIDCAP LIQUID 15', 'NIFTY100 LIQUID 15', 'NIFTY IPO', 'NIFTY SME EMERGE'
]

sectoral = [
    'NIFTY AUTO', 'NIFTY BANK', 'NIFTY CHEMICALS', 'NIFTY FINANCIAL SERVICES',
    'NIFTY FINANCIAL SERVICES 25/50', 'Nifty Financial Services Ex Bank', 'NIFTY FMCG',
    'Nifty HEALTHCARE', 'NIFTY IT', 'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY PHARMA',
    'NIFTY PRIVATE BANK', 'NIFTY PSU BANK', 'NIFTY REALTY', 'NIFTY CONSUMER DURABLES',
    'NIFTY OIL AND GAS INDEX', 'Nifty Capital Markets', 'NIFTY COMMODITIES', 'NIFTY ENERGY',
    'NIFTY INFRASTRUCTURE', 'NIFTY SERVICES SECTOR', 'Nifty Transportation & Logistics',
    'Nifty MidSmall Financial Services', 'Nifty MidSmall Healthcare', 'Nifty MidSmall IT & Telecom'
]

strategy = [
    'NIFTY 100 EQUAL WEIGHT', 'NIFTY 100 LOW VOLATILITY 30', 'NIFTY200 MOMENTUM 30',
    'NIFTY200 ALPHA 30', 'NIFTY100 ALPHA 30', 'NIFTY ALPHA 50', 'NIFTY ALPHA LOW VOLATILITY 30',
    'NIFTY ALPHA QUALITY LOW VOLATILITY 30', 'NIFTY ALPHA QUALITY VALUE LOW-VOLATILITY 30',
    'NIFTY DIVIDEND OPPORTUNITIES 50', 'NIFTY GROWTH SECTORS 15', 'NIFTY HIGH BETA 50',
    'NIFTY LOW VOLATILITY 50', 'NIFTY TOP 10 EQUAL WEIGHT', 'NIFTY TOP 15 EQUAL WEIGHT',
    'NIFTY TOP 20 EQUAL WEIGHT', 'NIFTY100 QUALITY 30', 'NIFTY Midcap150 Momentum 50',
    'Nifty500 Flexicap Quality 30', 'NIFTY500 LOW VOLATILITY 50', 'NIFTY500 MOMENTUM 50',
    'NIFTY500 QUALITY 50', 'NIFTY500 MULTIFACTOR MQVLv 50', 'NIFTY Midcap150 Quality 50',
    'Nifty Smallcap250 Quality 50', 'NIFTY500 MULTICAP MOMENTUM QUALITY 50',
    'Nifty MidSmallcap400 Momentum Quality 100', 'Nifty Smallcap250 Momentum Quality 100',
    'NIFTY QUALITY LOW VOLATILITY 30', 'NIFTY50 EQUAL WEIGHT', 'NIFTY50 VALUE 20',
    'Nifty200 Value 30', 'NIFTY500 VALUE 50', 'NIFTY200 Quality 30'
]

# Normalize names for matching
def normalize(name):
    return name.replace('tri - ', '').replace('TRI - ', '').strip().upper()

def categorize(name):
    clean = name.replace('tri - ', '').replace('TRI - ', '').strip()
    
    # Check against each category
    for cat in broad_market:
        if clean.upper() == cat.upper():
            return 'Broad'
    
    for cat in sectoral:
        if clean.upper() == cat.upper():
            return 'Sector'
    
    for cat in strategy:
        if clean.upper() == cat.upper():
            return 'Strategy'
    
    return 'Thematic'

# Categorize all indices
categories = {'Broad': [], 'Sector': [], 'Strategy': [], 'Thematic': []}

for name in data.keys():
    cat = categorize(name)
    categories[cat].append(name)

# Print results
print("=" * 80)
print("CATEGORIZATION SUMMARY")
print("=" * 80)

for cat_name in ['Broad', 'Sector', 'Strategy', 'Thematic']:
    print(f"\n{cat_name}: {len(categories[cat_name])} indices")
    print("-" * 80)
    for idx in sorted(categories[cat_name]):
        clean_name = idx.replace('tri - ', '').replace('TRI - ', '').strip()
        print(f"  {clean_name}")

print("\n" + "=" * 80)
print(f"Total: {sum(len(v) for v in categories.values())} indices")
print("=" * 80)
