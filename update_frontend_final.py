"""
Update frontend data by loading full mapping from Excel file
"""

import pandas as pd
import json
from pathlib import Path

def create_csv_to_excel_mapping():
    """Load the full mapping from create_proper_mapping.py logic"""
    exact_mappings = {
        'Nifty50 Shariah': 'NIFTY50 SHARIAH',
        'Nifty500 Shariah': 'NIFTY500 SHARIAH',
        'Nifty LargeMidcap 250': 'NIFTY LARGEMIDCAP 250',
        'Nifty Midcap150 Quality 50': 'NIFTY MIDCAP150 QUALITY 50',
        'Nifty50 Value 20': 'NIFTY50 VALUE 20',
        'Nifty50 Equal Weight': 'NIFTY50 EQUAL WEIGHT',
        'Nifty100 Quality 30': 'NIFTY100 QUALITY 30',
        'Nifty100 Equal Weight': 'NIFTY100 EQUAL WEIGHT',
        'Nifty Midcap50': 'NIFTY MIDCAP 50',
        'Nifty Midcap 100': 'NIFTY MIDCAP 100',
        'Nifty Midcap 150': 'NIFTY MIDCAP 150',
        'Nifty Smallcap50': 'NIFTY SMLCAP 50',
        'Nifty Smallcap 100': 'NIFTY SMLCAP 100',
        'Nifty Smallcap 250': 'NIFTY SMLCAP 250',
        'Nifty Midsmallcap 400': 'NIFTY MIDSMALLCAP 400',
        'Nifty Auto': 'NIFTY AUTO',
        'Nifty Bank': 'NIFTY BANK',
        'Nifty Energy': 'NIFTY ENERGY',
        'Nifty Financial Services': 'NIFTY FINANCIAL SERVICES',
        'Nifty FMCG': 'NIFTY FMCG',
        'Nifty IT': 'NIFTY IT',
        'Nifty Media': 'NIFTY MEDIA',
        'Nifty Metal': 'NIFTY METAL',
        'Nifty Pharma': 'NIFTY PHARMA',
        'Nifty PSU Bank': 'NIFTY PSU BANK',
        'Nifty Private Bank': 'NIFTY PRIVATE BANK',
        'Nifty Realty': 'NIFTY REALTY',
        'Nifty Healthcare': 'NIFTY HEALTHCARE INDEX',
        'Nifty Consumer Durables': 'NIFTY CONSUMER DURABLES',
        'Nifty Oil & Gas': 'NIFTY OIL & GAS',
        'Nifty Commodities': 'NIFTY COMMODITIES',
        'Nifty Consumption': 'NIFTY CONSUMPTION',
        'Nifty CPSE': 'NIFTY CPSE',
        'Nifty Infra': 'NIFTY INFRA',
        'Nifty MNC': 'NIFTY MNC',
        'Nifty PSE': 'NIFTY PSE',
        'Nifty Alpha 50': 'NIFTY ALPHA 50',
        'Nifty High Beta 50': 'NIFTY HIGH BETA 50',
        'Nifty Low Volatility 50': 'NIFTY LOW VOLATILITY 50',
        'Nifty Dividend Opportunities 50': 'NIFTY DIVIDEND OPPORTUNITIES 50',
        'Nifty Midcap Liquid 15': 'NIFTY MIDCAP LIQUID 15',
        'Nifty200 Momentum 30': 'NIFTY200 MOMENTUM 30',
        'Nifty400 Multicap': 'NIFTY400 MULTICAP',
        'Nifty Top 10 Equal Weight': 'NIFTY TOP 10 EQUAL WEIGHT',
        'Nifty100 Liquid 15': 'NIFTY100 LIQUID 15',
        'Nifty500 Value 50': 'NIFTY500 VALUE 50',
        'Nifty500 Multicap 50:25:25': 'NIFTY500 MULTICAP 50:25:25',
        'Nifty Microcap 250': 'NIFTY MICROCAP 250',
        'Nifty Total Market': 'NIFTY TOTAL MARKET',
        'Nifty100 Low Volatility 30': 'NIFTY100 LOW VOLATILITY 30',
        'Nifty India Defence': 'Nifty India Defence',
        'Nifty Rural': 'Nifty Rural',
        'Nifty Housing': 'Nifty Housing',
        'Nifty Transportation & Logistics': 'Nifty Transportation & Logistics',
        'Nifty MidSmall Healthcare': 'Nifty MidSmall Healthcare',
        'Nifty MidSmall IT & Telecom': 'Nifty MidSmall IT & Telecom',
        'Nifty MidSmall Financial Services': 'Nifty MidSmall Financial Services',
        'Nifty MidSmall India Consumption': 'Nifty MidSmall India Consumption',
        'Nifty Financial Services Ex Bank': 'Nifty Financial Services Ex Bank',
        'Nifty200 Value 30': 'Nifty200 Value 30',
        'Nifty Mobility': 'Nifty Mobility',
        'Nifty India Manufacturing': 'Nifty India Manufacturing',
        'Nifty Non-Cyclical Consumer': 'Nifty Non-Cyclical Consumer',
        'Nifty Core Housing': 'Nifty Core Housing',
        'Nifty100 ESG': 'NIFTY100 ESG',
        'Nifty India Corporate Group Index - Tata Group': 'NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP',
        'Nifty Chemicals': 'NIFTY CHEMICALS',
        'UTI Nifty 50 Arbitrage Fund': 'UTI FLEX',
        'Kotak Gold': 'KOTAK GOLD',
        'Nifty 10 yr Benchmark G-Sec': 'NIFTY 10 YR BENCHMARK G-SEC',
        'Nifty 10 yr Benchmark G-Sec (Clean Price)': 'NIFTY 10 YR BENCHMARK G-SEC.1',
    }
    return exact_mappings

def load_excel_categories():
    """Load categories from Excel file"""
    excel_file = Path('data/251229_Final_summary.xlsx')
    if not excel_file.exists():
        return {}
    
    df = pd.read_excel(excel_file, skiprows=1)
    
    categories = {}
    current_category = None
    
    for _, row in df.iterrows():
        symbol = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''
        
        if symbol in ['Broad Market Indices', 'Sectoral Indices', 'Strategy Indices', 'Thematic Indices']:
            if 'Broad' in symbol:
                current_category = 'Broad Market'
            elif 'Sectoral' in symbol:
                current_category = 'Sectoral'
            elif 'Strategy' in symbol:
                current_category = 'Strategy'
            elif 'Thematic' in symbol:
                current_category = 'Thematic'
        elif symbol and current_category and symbol not in ['Broad Market Indices', 'Sectoral Indices', 'Strategy Indices', 'Thematic Indices']:
            categories[symbol] = current_category
    
    return categories

def main():
    print("="*80)
    print("UPDATING FRONTEND WITH CORRECTED VALUES (FULL MAPPING)")
    print("="*80)
    print()
    
    # Load corrected values
    corrected_file = Path('data/CORRECTED_METHOD1_summary.xlsx')
    df_corrected = pd.read_excel(corrected_file)
    df_corrected.columns = ['Index', 'Percentile']
    print(f"✓ Loaded {len(df_corrected)} corrected values")
    
    # Load Excel categories
    categories = load_excel_categories()
    print(f"✓ Loaded {len(categories)} categories from Excel")
    
    # Create CSV to Excel mapping
    excel_to_csv = create_csv_to_excel_mapping()
    csv_to_excel = {v: k for k, v in excel_to_csv.items()}
    
    # Create updated data
    updated_data = []
    matched = 0
    unmatched = []
    
    for _, row in df_corrected.iterrows():
        csv_name = row['Index']
        percentile = row['Percentile']
        
        # Find Excel name
        excel_name = csv_to_excel.get(csv_name, csv_name)
        
        # Add "tri - " prefix for category lookup
        excel_lookup_name = f"tri - {excel_name}"
        
        # Get category
        category = categories.get(excel_lookup_name)
        
        if category:
            # Use Excel name as display name (without "tri - " prefix)
            updated_data.append({
                'fullName': excel_lookup_name,
                'displayName': excel_name,
                'percentile': round(percentile, 6),
                'category': category
            })
            matched += 1
        else:
            unmatched.append((csv_name, excel_name, excel_lookup_name))
    
    print(f"\n✓ Matched {matched}/{len(df_corrected)} indices")
    
    if unmatched:
        print(f"\n⚠ {len(unmatched)} indices not matched:")
        for csv, excel, lookup in unmatched[:10]:
            print(f"   CSV: {csv}")
            print(f"   Excel: {excel}")
            print(f"   Lookup: {lookup}")
            print()
        if len(unmatched) > 10:
            print(f"   ... and {len(unmatched) - 10} more")
    
    # Sort by category and percentile
    category_order = {
        'Broad Market': 1,
        'Sectoral': 2,
        'Strategy': 3,
        'Thematic': 4
    }
    
    updated_data.sort(key=lambda x: (category_order.get(x['category'], 5), -x['percentile']))
    
    # Save updated JSON
    output_file = Path('data/indices_with_short_names.json')
    with open(output_file, 'w') as f:
        json.dump(updated_data, f, indent=2)
    
    print(f"\n✓ Saved {len(updated_data)} indices to: {output_file}")
    
    # Statistics by category
    print("\n" + "="*80)
    print("STATISTICS BY CATEGORY")
    print("="*80)
    
    for category in ['Broad Market', 'Sectoral', 'Strategy', 'Thematic']:
        category_data = [x for x in updated_data if x['category'] == category]
        if category_data:
            percentiles = [x['percentile'] for x in category_data]
            print(f"\n{category}:")
            print(f"  Count: {len(category_data)}")
            print(f"  Mean: {sum(percentiles)/len(percentiles):.4f}")
            top = max(category_data, key=lambda x: x['percentile'])
            bottom = min(category_data, key=lambda x: x['percentile'])
            print(f"  Top: {top['displayName']} ({top['percentile']:.4f})")
            print(f"  Bottom: {bottom['displayName']} ({bottom['percentile']:.4f})")
    
    print("\n" + "="*80)
    print("✓ Frontend data updated successfully!")
    print("✓ Your webpage now shows the CORRECTED calculation values")
    print("✓ Refresh your browser at: http://localhost:8000")
    print("="*80)

if __name__ == "__main__":
    main()
