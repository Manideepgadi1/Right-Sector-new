"""
Compare Excel (251229_Final_summary.xlsx) vs NEW Calculation Method
This shows whether the Excel values match the improved calculation
"""

import pandas as pd
import numpy as np
import json

print("=" * 80)
print("EXCEL vs NEW CALCULATION METHOD COMPARISON")
print("=" * 80)

# ============================================================================
# 1. Load Excel file (your "correct" data)
# ============================================================================
print("\n1. Loading Excel file (251229_Final_summary.xlsx)...")
excel_df = pd.read_excel('data/251229_Final_summary.xlsx')
print(f"   Excel loaded: {len(excel_df)} indices")

# Create lookup dictionary from Excel (remove "tri - " prefix for matching)
excel_lookup = {}
excel_original_names = {}
for idx, row in excel_df.iterrows():
    symbol = str(row['SYMBOL']).strip()
    if symbol.lower() == 'date':  # Skip the date row if present
        continue
    clean_symbol = symbol.replace('tri - ', '').strip()
    value = float(row['final_pct_value'])
    excel_lookup[clean_symbol] = value
    excel_original_names[clean_symbol] = symbol

print(f"   Excel lookup created for {len(excel_lookup)} indices")

# ============================================================================
# 2. Run NEW calculation method
# ============================================================================
print("\n2. Running NEW calculation method...")

# Read raw data
df = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv')
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y')
print(f"   Raw data loaded: {len(df)} rows, {len(df.columns)} columns")

def calculate_new_method(df_with_daily_values, date_column='DATE'):
    """NEW calculation method with all improvements"""
    
    df_melted = df_with_daily_values.melt(
        id_vars=[date_column], 
        var_name='SYMBOL', 
        value_name='VALUE'
    )
    df_melted = df_melted.dropna()
    df_melted['VALUE'] = pd.to_numeric(df_melted['VALUE'], errors='coerce')
    df_melted = df_melted.dropna()
    
    # Sort by DATE and SYMBOL
    df_melted = df_melted.sort_values([date_column, 'SYMBOL']).reset_index(drop=True)
    
    # Calculate 5-Year Rolling CAGR
    pr_cagr = 1825
    
    def calculate_cagr(x):
        if len(x) < pr_cagr:
            return np.nan
        first_val = x.iloc[0]
        last_val = x.iloc[-1]
        if first_val <= 0 or last_val <= 0:
            return np.nan
        return (last_val / first_val) ** (1/5) - 1
    
    df_melted['Rolling_CAGR'] = (
        df_melted.groupby('SYMBOL')['VALUE']
        .rolling(window=pr_cagr, min_periods=pr_cagr)
        .apply(calculate_cagr, raw=False)
        .reset_index(level=0, drop=True)
    )
    
    # Calculate Percentile Rank
    pr_rank = 1825
    
    def percentile_rank(x):
        if len(x) < pr_rank:
            return np.nan
        x_clean = pd.Series(x).dropna()
        if len(x_clean) == 0:
            return np.nan
        return x_clean.rank(pct=True).iloc[-1]
    
    df_melted['Percentile_Rank'] = (
        df_melted.groupby('SYMBOL')['Rolling_CAGR']
        .rolling(window=pr_rank, min_periods=pr_rank)
        .apply(percentile_rank, raw=False)
        .reset_index(level=0, drop=True)
    )
    
    df_melted = df_melted.dropna(subset=['Percentile_Rank'])
    
    df_processed = df_melted.pivot_table(
        values='Percentile_Rank', 
        index=date_column, 
        columns='SYMBOL'
    )
    
    df_processed['year'] = df_processed.index.year
    df_processed['month'] = df_processed.index.month
    df_month_mean = df_processed.groupby(['year', 'month']).mean(numeric_only=True)
    df_month_mean.sort_values(by=['year', 'month'], ascending=False, inplace=True)
    
    df_final_summary = df_month_mean.reset_index()
    df_final_summary = df_final_summary.iloc[0:1, :].transpose()
    df_final_summary.columns = ["final_pct_value"]
    df_final_summary.drop(["year", "month"], inplace=True)
    
    df_final_summary['final_pct_value'] = pd.to_numeric(
        df_final_summary['final_pct_value'], 
        errors='coerce'
    )
    df_final_summary = df_final_summary.dropna()
    df_final_summary.sort_values(by='final_pct_value', ascending=True, inplace=True)
    
    return df_final_summary

df_new = calculate_new_method(df)
print(f"   ✓ NEW calculation completed: {len(df_new)} indices")

# ============================================================================
# 3. Compare Excel vs NEW calculation
# ============================================================================
print("\n" + "=" * 80)
print("COMPARISON RESULTS")
print("=" * 80)

# Find matching indices
excel_symbols = set(excel_lookup.keys())
new_symbols = set(df_new.index)
common_symbols = excel_symbols.intersection(new_symbols)

print(f"\nIndices in Excel: {len(excel_symbols)}")
print(f"Indices from NEW calculation: {len(new_symbols)}")
print(f"Common indices: {len(common_symbols)}")

# Indices only in Excel
only_excel = excel_symbols - new_symbols
if only_excel:
    print(f"\n⚠️  Indices in Excel but NOT in NEW calculation ({len(only_excel)}):")
    for sym in sorted(only_excel)[:10]:
        print(f"   - {sym}")

# Indices only in NEW
only_new = new_symbols - excel_symbols
if only_new:
    print(f"\n⚠️  Indices in NEW calculation but NOT in Excel ({len(only_new)}):")
    for sym in sorted(only_new)[:10]:
        print(f"   - {sym}")

# ============================================================================
# 4. Detailed comparison for common indices
# ============================================================================
print("\n" + "=" * 80)
print("VALUE COMPARISON (Common indices)")
print("=" * 80)

comparison_data = []
for symbol in common_symbols:
    excel_val = excel_lookup[symbol]
    new_val = df_new.loc[symbol, 'final_pct_value']
    diff = excel_val - new_val
    abs_diff = abs(diff)
    pct_diff = (abs_diff / excel_val * 100) if excel_val != 0 else 0
    
    comparison_data.append({
        'symbol': symbol,
        'excel': excel_val,
        'new': new_val,
        'diff': diff,
        'abs_diff': abs_diff,
        'pct_diff': pct_diff
    })

# Sort by absolute difference
comparison_data.sort(key=lambda x: x['abs_diff'], reverse=True)

# Count matches and mismatches
if len(comparison_data) > 0:
    exact_matches = sum(1 for x in comparison_data if x['abs_diff'] < 0.0001)
    close_matches = sum(1 for x in comparison_data if 0.0001 <= x['abs_diff'] < 0.01)
    significant_diff = sum(1 for x in comparison_data if x['abs_diff'] >= 0.01)

    print(f"\nMatch Analysis:")
    print(f"  Exact matches (diff < 0.0001):      {exact_matches:3d} ({exact_matches/len(comparison_data)*100:.1f}%)")
    print(f"  Close matches (diff 0.0001-0.01):   {close_matches:3d} ({close_matches/len(comparison_data)*100:.1f}%)")
    print(f"  Significant differences (>0.01):    {significant_diff:3d} ({significant_diff/len(comparison_data)*100:.1f}%)")

    if exact_matches == len(comparison_data):
        print("\n✅ PERFECT MATCH! Excel and NEW calculation produce identical values!")
    else:
        print(f"\n⚠️  Values DO NOT MATCH. {significant_diff} indices have significant differences.")
else:
    print("\n❌ NO COMMON INDICES FOUND - Cannot compare values")
    exact_matches = 0
    close_matches = 0
    significant_diff = 0

# ============================================================================
# 5. Show top differences
# ============================================================================
if len(comparison_data) > 0:
    print("\n" + "=" * 80)
    print("TOP 20 LARGEST DIFFERENCES")
    print("=" * 80)
    print(f"\n{'Index':<50} {'Excel':<10} {'NEW':<10} {'Diff':<10} {'%Diff':<8}")
    print("-" * 98)

    for item in comparison_data[:20]:
        symbol_short = item['symbol'][:48] if len(item['symbol']) > 48 else item['symbol']
        print(f"{symbol_short:<50} {item['excel']:<10.6f} {item['new']:<10.6f} {item['diff']:<10.6f} {item['pct_diff']:<8.2f}%")

# ============================================================================
# 6. Save comparison to Excel
# ============================================================================
if len(comparison_data) > 0:
    print("\n" + "=" * 80)
    print("SAVING COMPARISON REPORT")
    print("=" * 80)

    comparison_df = pd.DataFrame(comparison_data)
    comparison_df = comparison_df.sort_values('abs_diff', ascending=False)
    comparison_df.to_excel('data/excel_vs_new_comparison.xlsx', index=False)
    print("✓ Saved to: data/excel_vs_new_comparison.xlsx")

# ============================================================================
# 7. Summary and Recommendation
# ============================================================================
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

if len(comparison_data) == 0:
    print("""
❌ NO COMPARISON POSSIBLE - No common indices found
   - Check if Excel symbol names match the raw data column names
   - Verify "tri - " prefix handling
""")
elif exact_matches == len(comparison_data):
    print("""
✅ CONCLUSION: Excel values MATCH the NEW calculation method perfectly!
   - The Excel file appears to use the improved calculation logic
   - Safe to use NEW method going forward
   - No changes needed
""")
elif exact_matches > len(comparison_data) * 0.9:
    print(f"""
⚠️  CONCLUSION: Excel values MOSTLY match NEW calculation ({exact_matches}/{len(comparison_data)})
   - Minor differences found in {len(comparison_data) - exact_matches} indices
   - Likely due to rounding or minor data differences
   - Review the comparison Excel file for details
""")
else:
    avg_diff = sum(x['abs_diff'] for x in comparison_data) / len(comparison_data)
    print(f"""
❌ CONCLUSION: Excel values DO NOT match NEW calculation method
   - {significant_diff}/{len(comparison_data)} indices have significant differences
   - Average difference: {avg_diff:.6f}
   - Excel might be using the OLD calculation method (with min_periods=1)
   
RECOMMENDATION:
   1. Review data/excel_vs_new_comparison.xlsx for detailed differences
   2. Decide which method is "correct" for your use case:
      - Excel values (current) - may have incomplete data issues
      - NEW method values - more strict, requires full 5-year history
   3. If NEW method is correct, regenerate Excel using the NEW calculation
""")

print("=" * 80)
