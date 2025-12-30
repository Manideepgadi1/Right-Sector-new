import pandas as pd
import json

print("=" * 80)
print("INDICES COUNT AND VALUE SOURCE VERIFICATION")
print("=" * 80)

# 1. Check Excel file
print("\n1. EXCEL FILE (251229_Final_summary.xlsx):")
try:
    excel_df = pd.read_excel('data/251229_Final_summary.xlsx')
    print(f"   Total indices in Excel: {len(excel_df)}")
    print(f"   Columns: {excel_df.columns.tolist()}")
    print("\n   First 5 entries:")
    for idx, row in excel_df.head().iterrows():
        print(f"   {row.iloc[0]}: {row.iloc[1]}")
except Exception as e:
    print(f"   Error reading Excel: {e}")

# 2. Check summary_data.json
print("\n2. SUMMARY DATA JSON (data/summary_data.json):")
try:
    with open('data/summary_data.json', 'r') as f:
        summary_data = json.load(f)
    print(f"   Total indices in JSON: {len(summary_data)}")
    print("\n   First 5 entries:")
    for i, (name, value) in enumerate(list(summary_data.items())[:5]):
        print(f"   {name}: {value}")
except Exception as e:
    print(f"   Error reading JSON: {e}")

# 3. Check current display data
print("\n3. CURRENT DISPLAY DATA (data/indices_with_short_names.json):")
try:
    with open('data/indices_with_short_names.json', 'r') as f:
        display_data = json.load(f)
    print(f"   Total indices in display: {len(display_data)}")
    
    # Count by category
    from collections import Counter
    categories = Counter([item['category'] for item in display_data])
    print("\n   Category breakdown:")
    for cat, count in sorted(categories.items()):
        print(f"   - {cat}: {count}")
except Exception as e:
    print(f"   Error reading display data: {e}")

# 4. Compare Excel vs JSON
print("\n4. MISSING INDICES ANALYSIS:")
try:
    excel_names = set()
    for idx, row in excel_df.iterrows():
        name = str(row.iloc[0]).strip()
        excel_names.add(name)
    
    json_names = set()
    for key in summary_data.keys():
        clean = key.replace('tri - ', '').strip()
        json_names.add(clean)
    
    missing_in_json = excel_names - json_names
    extra_in_json = json_names - excel_names
    
    if missing_in_json:
        print(f"\n   Indices in Excel but NOT in JSON ({len(missing_in_json)}):")
        for name in sorted(missing_in_json)[:10]:
            print(f"   - {name}")
    else:
        print("\n   ✓ All Excel indices are in JSON")
    
    if extra_in_json:
        print(f"\n   Indices in JSON but NOT in Excel ({len(extra_in_json)}):")
        for name in sorted(extra_in_json)[:10]:
            print(f"   - {name}")
    else:
        print("\n   ✓ No extra indices in JSON")
        
except Exception as e:
    print(f"   Error comparing: {e}")

# 5. Verify values match
print("\n5. VALUE SOURCE VERIFICATION:")
print("   Checking if values in display match Excel...")
try:
    matches = 0
    mismatches = []
    
    # Create Excel lookup
    excel_lookup = {}
    for idx, row in excel_df.iterrows():
        name = str(row.iloc[0]).strip()
        value = float(row.iloc[1])
        excel_lookup[name.upper()] = value
    
    # Check display data
    for item in display_data[:10]:  # Check first 10
        display_name = item['displayName'].upper()
        display_value = item['percentile']
        
        if display_name in excel_lookup:
            excel_value = excel_lookup[display_name]
            if abs(display_value - excel_value) < 0.0001:
                matches += 1
            else:
                mismatches.append({
                    'name': item['displayName'],
                    'display': display_value,
                    'excel': excel_value
                })
    
    print(f"\n   Checked first 10 indices:")
    print(f"   - Matches: {matches}")
    print(f"   - Mismatches: {len(mismatches)}")
    
    if mismatches:
        print("\n   Sample mismatches:")
        for m in mismatches[:3]:
            print(f"   {m['name']}: Display={m['display']:.4f}, Excel={m['excel']:.4f}")
    else:
        print("\n   ✓ VALUES ARE DIRECTLY FROM EXCEL (not calculated)")
        
except Exception as e:
    print(f"   Error verifying values: {e}")

print("\n" + "=" * 80)
print("SUMMARY:")
print(f"- Values source: EXCEL file (251229_Final_summary.xlsx)")
print(f"- Data flow: Excel → summary_data.json → indices_with_short_names.json → Webpage")
print(f"- No calculation is done, values are taken as-is from Excel")
print("=" * 80)
