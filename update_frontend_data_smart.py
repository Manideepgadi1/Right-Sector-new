"""
Update frontend data with corrected values using proper name mapping
"""

import pandas as pd
import json
from pathlib import Path

def create_csv_to_excel_mapping():
    """Create mapping from CSV column names to Excel names"""
    # Common patterns
    mapping = {
        # Exact matches for special cases
        'NIFTY 50': 'tri - Nifty 50',
        'NIFTY NEXT 50': 'tri - Nifty Next 50',
        'NIFTY 100': 'tri - Nifty 100',
        'NIFTY 200': 'tri - Nifty 200',
        'NIFTY 500': 'tri - Nifty 500',
        'NIFTY MIDCAP 50': 'tri - Nifty Midcap 50',
        'NIFTY MIDCAP 100': 'tri - Nifty Midcap 100',
        'NIFTY MIDCAP 150': 'tri - Nifty Midcap 150',
        'NIFTY SMLCAP 50': 'tri - Nifty Smallcap 50',
        'NIFTY SMLCAP 100': 'tri - Nifty Smallcap 100',
        'NIFTY SMLCAP 250': 'tri - Nifty Smallcap 250',
        'NIFTY IT': 'tri - Nifty IT',
        'NIFTY BANK': 'tri - Nifty Bank',
        'NIFTY AUTO': 'tri - Nifty Auto',
        'NIFTY FINANCIAL SERVICES': 'tri - Nifty Financial Services',
        'NIFTY FMCG': 'tri - Nifty FMCG',
        'NIFTY METAL': 'tri - Nifty Metal',
        'NIFTY PHARMA': 'tri - Nifty Pharma',
        'NIFTY PSU BANK': 'tri - Nifty PSU Bank',
        'NIFTY REALTY': 'tri - Nifty Realty',
        'NIFTY PRIVATE BANK': 'tri - Nifty Private Bank',
        'NIFTY CPSE': 'tri - Nifty CPSE',
        'NIFTY ENERGY': 'tri - Nifty Energy',
        'NIFTY INFRA': 'tri - Nifty Infra',
        'NIFTY COMMODITIES': 'tri - Nifty Commodities',
        'NIFTY CONSUMPTION': 'tri - Nifty Consumption',
        'NIFTY DIVIDEND OPPORTUNITIES 50': 'tri - Nifty Dividend Opportunities 50',
        'NIFTY50 VALUE 20': 'tri - Nifty50 Value 20',
        'NIFTY ALPHA 50': 'tri - Nifty Alpha 50',
        'NIFTY HIGH BETA 50': 'tri - Nifty High Beta 50',
        'NIFTY LOW VOLATILITY 50': 'tri - Nifty Low Volatility 50',
        'NIFTY100 QUALITY 30': 'tri - Nifty100 Quality 30',
        'NIFTY MIDCAP LIQUID 15': 'tri - Nifty Midcap Liquid 15',
        'NIFTY HEALTHCARE INDEX': 'tri - Nifty Healthcare',
        'NIFTY CONSUMER DURABLES': 'tri - Nifty Consumer Durables',
        'NIFTY OIL & GAS': 'tri - Nifty Oil & Gas',
        'NIFTY MNC': 'tri - Nifty MNC',
        'NIFTY MEDIA': 'tri - Nifty Media',
        'NIFTY PSE': 'tri - Nifty PSE',
        'NIFTY500 SHARIAH': 'tri - Nifty500 Shariah',
        'NIFTY50 SHARIAH': 'tri - Nifty50 Shariah',
        'NIFTY CHEMICALS': 'tri - Nifty Chemicals',
        'NIFTY TOP 10 EQUAL WEIGHT': 'tri - Nifty Top 10 Equal Weight',
        'NIFTY100 LIQUID 15': 'tri - Nifty100 Liquid 15',
        'NIFTY500 VALUE 50': 'tri - Nifty500 Value 50',
        'Nifty200 Value 30': 'tri - Nifty200 Value 30',
        'NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP': 'tri - Nifty India Corporate Group Index - Tata Group',
        'Nifty MidSmall Financial Services': 'tri - Nifty MidSmall Financial Services',
        'Nifty Financial Services Ex Bank': 'tri - Nifty Financial Services Ex Bank',
        'KOTAK GOLD': 'tri - Kotak Gold',
        'UTI FLEX': 'tri - UTI Nifty 50 Arbitrage Fund',
        'NIFTY 10 YR BENCHMARK G-SEC': 'tri - Nifty 10 yr Benchmark G-Sec',
        'NIFTY 10 YR BENCHMARK G-SEC.1': 'tri - Nifty 10 yr Benchmark G-Sec (Clean Price)',
    }
    
    return mapping

def normalize_name(name):
    """Normalize name for fuzzy matching"""
    return name.upper().replace('TRI - ', '').replace('-', ' ').strip()

def main():
    print("="*80)
    print("UPDATING FRONTEND WITH CORRECTED VALUES (SMART MAPPING)")
    print("="*80)
    print()
    
    # Load corrected values
    corrected_file = Path('data/CORRECTED_METHOD1_summary.xlsx')
    df_corrected = pd.read_excel(corrected_file)
    df_corrected.columns = ['Index', 'Percentile']
    print(f"✓ Loaded {len(df_corrected)} corrected values")
    
    # Load existing mapping
    mapping_file = Path('data/indices_with_short_names.json')
    with open(mapping_file, 'r') as f:
        existing_data = json.load(f)
    print(f"✓ Loaded {len(existing_data)} existing mappings")
    
    # Create name mappings
    csv_to_excel = create_csv_to_excel_mapping()
    
    # Create lookup from existing data
    existing_lookup = {}
    for item in existing_data:
        existing_lookup[item['fullName']] = {
            'displayName': item['displayName'],
            'category': item['category']
        }
    
    # Also create normalized lookup for fuzzy matching
    normalized_lookup = {}
    for item in existing_data:
        norm_name = normalize_name(item['fullName'])
        normalized_lookup[norm_name] = item['fullName']
    
    # Merge data
    updated_data = []
    matched_exact = 0
    matched_fuzzy = 0
    unmatched = []
    
    for _, row in df_corrected.iterrows():
        csv_name = row['Index']
        percentile = row['Percentile']
        
        # Try exact mapping first
        excel_name = csv_to_excel.get(csv_name)
        
        if excel_name and excel_name in existing_lookup:
            updated_data.append({
                'fullName': excel_name,
                'displayName': existing_lookup[excel_name]['displayName'],
                'percentile': round(percentile, 6),
                'category': existing_lookup[excel_name]['category']
            })
            matched_exact += 1
        else:
            # Try fuzzy matching
            norm_csv = normalize_name(csv_name)
            if norm_csv in normalized_lookup:
                matched_excel_name = normalized_lookup[norm_csv]
                updated_data.append({
                    'fullName': matched_excel_name,
                    'displayName': existing_lookup[matched_excel_name]['displayName'],
                    'percentile': round(percentile, 6),
                    'category': existing_lookup[matched_excel_name]['category']
                })
                matched_fuzzy += 1
            else:
                unmatched.append(csv_name)
    
    print(f"\n✓ Matched {matched_exact} exactly")
    print(f"✓ Matched {matched_fuzzy} via fuzzy matching")
    print(f"✓ Total matched: {len(updated_data)}/{len(df_corrected)}")
    
    if unmatched:
        print(f"\n⚠ {len(unmatched)} indices not matched:")
        for name in unmatched[:10]:
            print(f"   - {name}")
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
            print(f"  Min: {min(percentiles):.4f} - {[x['displayName'] for x in category_data if x['percentile'] == min(percentiles)][0]}")
            print(f"  Max: {max(percentiles):.4f} - {[x['displayName'] for x in category_data if x['percentile'] == max(percentiles)][0]}")
    
    print("\n" + "="*80)
    print("✓ Frontend data updated successfully!")
    print("✓ Refresh your browser (http://localhost:8000) to see the new values")
    print("="*80)

if __name__ == "__main__":
    main()
