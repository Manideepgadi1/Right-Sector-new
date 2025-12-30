"""
Update frontend data with corrected calculation values
"""

import pandas as pd
import json
from pathlib import Path

def main():
    print("="*80)
    print("UPDATING FRONTEND WITH CORRECTED VALUES")
    print("="*80)
    print()
    
    # Load corrected values
    corrected_file = Path('data/CORRECTED_METHOD1_summary.xlsx')
    if not corrected_file.exists():
        print(f"Error: {corrected_file} not found!")
        return
    
    df_corrected = pd.read_excel(corrected_file)
    df_corrected.columns = ['Index', 'Percentile']
    print(f"✓ Loaded {len(df_corrected)} corrected values")
    
    # Load existing mapping (has displayName and category)
    mapping_file = Path('data/indices_with_short_names.json')
    if not mapping_file.exists():
        print(f"Error: {mapping_file} not found!")
        return
    
    with open(mapping_file, 'r') as f:
        existing_data = json.load(f)
    
    print(f"✓ Loaded {len(existing_data)} existing mappings")
    
    # Create lookup dictionaries
    corrected_lookup = {}
    for _, row in df_corrected.iterrows():
        corrected_lookup[row['Index']] = row['Percentile']
    
    existing_lookup = {}
    for item in existing_data:
        existing_lookup[item['fullName']] = {
            'displayName': item['displayName'],
            'category': item['category']
        }
    
    # Merge data
    updated_data = []
    matched_count = 0
    unmatched = []
    
    for csv_name, percentile in corrected_lookup.items():
        if csv_name in existing_lookup:
            updated_data.append({
                'fullName': csv_name,
                'displayName': existing_lookup[csv_name]['displayName'],
                'percentile': round(percentile, 6),
                'category': existing_lookup[csv_name]['category']
            })
            matched_count += 1
        else:
            unmatched.append(csv_name)
    
    print(f"\n✓ Matched {matched_count}/{len(corrected_lookup)} indices")
    
    if unmatched:
        print(f"\n⚠ {len(unmatched)} indices not found in mapping:")
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
    
    # Show sample from each category
    print("\n" + "="*80)
    print("SAMPLE DATA BY CATEGORY")
    print("="*80)
    
    for category in ['Broad Market', 'Sectoral', 'Strategy', 'Thematic']:
        category_data = [x for x in updated_data if x['category'] == category]
        print(f"\n{category} ({len(category_data)} indices):")
        for item in category_data[:3]:
            print(f"  {item['displayName']}: {item['percentile']:.4f}")
    
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
            print(f"  Min: {min(percentiles):.4f}")
            print(f"  Max: {max(percentiles):.4f}")
    
    print("\n" + "="*80)
    print("✓ Frontend data updated successfully!")
    print("✓ Refresh your browser to see the new values")
    print("="*80)

if __name__ == "__main__":
    main()
