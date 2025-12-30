"""
FINAL COMPARISON: Excel (Your Correct Data) vs NEW Calculation
Uses the name mapping we created to properly match indices
"""

import pandas as pd
import numpy as np
import json

print("=" * 80)
print("EXCEL (CORRECT) vs NEW CALCULATION - PROPER COMPARISON")
print("=" * 80)

# Load Excel (your correct data)
excel_df = pd.read_excel('data/251229_Final_summary.xlsx')
excel_df = excel_df[excel_df['SYMBOL'].str.lower() != 'date']  # Remove 'date' row
print(f"\n1. Excel loaded: {len(excel_df)} indices")

# Load NEW calculation results
print("\n2. Running NEW calculation...")
df_raw = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv')
df_raw['DATE'] = pd.to_datetime(df_raw['DATE'], format='%d/%m/%y')

def calculate_new_method(df_with_daily_values, date_column='DATE'):
    df_melted = df_with_daily_values.melt(
        id_vars=[date_column], var_name='SYMBOL', value_name='VALUE'
    )
    df_melted = df_melted.dropna()
    df_melted['VALUE'] = pd.to_numeric(df_melted['VALUE'], errors='coerce')
    df_melted = df_melted.dropna()
    df_melted = df_melted.sort_values([date_column, 'SYMBOL']).reset_index(drop=True)
    
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
        values='Percentile_Rank', index=date_column, columns='SYMBOL'
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
        df_final_summary['final_pct_value'], errors='coerce'
    )
    df_final_summary = df_final_summary.dropna()
    return df_final_summary

df_new = calculate_new_method(df_raw)
print(f"   NEW calculation: {len(df_new)} indices")

# Get our name mapping from create_proper_mapping.py
# This maps Excel abbreviated names to CSV column names
import sys
sys.path.append('.')
exec(open('create_proper_mapping.py').read().split('# Process summary data')[0])

# Now compare
print("\n" + "=" * 80)
print("COMPARISON USING NAME MAPPING")
print("=" * 80)

comparison_results = []

for idx, row in excel_df.iterrows():
    excel_symbol = str(row['SYMBOL']).strip()
    excel_value = float(row['final_pct_value'])
    
    # Try to find corresponding NEW value using name cleaning
    cleaned = clean_name(excel_symbol)
    
    # Check if this cleaned name exists in NEW calculation
    found_new_value = None
    for new_symbol in df_new.index:
        if cleaned.upper() in new_symbol.upper() or new_symbol.upper() in cleaned.upper():
            if len(new_symbol) > 10 and len(cleaned) > 10:  # Avoid short false matches
                found_new_value = df_new.loc[new_symbol, 'final_pct_value']
                matched_symbol = new_symbol
                break
    
    if found_new_value is not None:
        diff = excel_value - found_new_value
        comparison_results.append({
            'excel_name': excel_symbol,
            'new_name': matched_symbol,
            'excel_value': excel_value,
            'new_value': found_new_value,
            'difference': diff,
            'abs_diff': abs(diff),
            'pct_diff': abs(diff) / excel_value * 100 if excel_value != 0 else 0
        })

print(f"\nMatched: {len(comparison_results)} out of {len(excel_df)} Excel indices")

if len(comparison_results) > 0:
    # Statistics
    exact_match = sum(1 for x in comparison_results if x['abs_diff'] < 0.0001)
    close_match = sum(1 for x in comparison_results if 0.0001 <= x['abs_diff'] < 0.01)
    significant = sum(1 for x in comparison_results if x['abs_diff'] >= 0.01)
    
    print(f"\nMatch Quality:")
    print(f"  Exact (< 0.0001):     {exact_match:3d} ({exact_match/len(comparison_results)*100:.1f}%)")
    print(f"  Close (0.0001-0.01):  {close_match:3d} ({close_match/len(comparison_results)*100:.1f}%)")
    print(f"  Different (> 0.01):   {significant:3d} ({significant/len(comparison_results)*100:.1f}%)")
    
    # Save comparison
    comp_df = pd.DataFrame(comparison_results)
    comp_df = comp_df.sort_values('abs_diff', ascending=False)
    comp_df.to_excel('data/FINAL_excel_vs_new_comparison.xlsx', index=False)
    print(f"\n✓ Saved detailed comparison to: data/FINAL_excel_vs_new_comparison.xlsx")
    
    # Show top 15 differences
    print("\n" + "=" * 80)
    print("TOP 15 DIFFERENCES (Excel vs NEW)")
    print("=" * 80)
    print(f"\n{'Excel Name':<45} {'Excel':<9} {'NEW':<9} {'Diff':<9} {'%Diff'}")
    print("-" * 90)
    for item in comp_df.head(15).to_dict('records'):
        name = item['excel_name'].replace('tri - ', '')[:43]
        print(f"{name:<45} {item['excel_value']:<9.6f} {item['new_value']:<9.6f} {item['difference']:<9.6f} {item['pct_diff']:>6.1f}%")
    
    # Conclusion
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    
    avg_diff = comp_df['abs_diff'].mean()
    
    if exact_match == len(comparison_results):
        print("\n✅ PERFECT MATCH! Excel values match NEW calculation exactly.")
        print("   Your Excel file uses the improved calculation method.")
    elif exact_match / len(comparison_results) > 0.9:
        print(f"\n✅ MOSTLY MATCHES! {exact_match}/{len(comparison_results)} indices match exactly.")
        print(f"   Small differences likely due to rounding or data updates.")
    else:
        print(f"\n❌ SIGNIFICANT DIFFERENCES DETECTED")
        print(f"   Only {exact_match}/{len(comparison_results)} exact matches")
        print(f"   Average difference: {avg_diff:.6f}")
        print(f"   {significant} indices have differences > 0.01")
        print(f"\n   This suggests your Excel was calculated with:")
        print(f"   - OLD method (min_periods=1, allows incomplete data)")
        print(f"   \n   While NEW method uses:")
        print(f"   - Full 1825-day requirement (more strict, more accurate)")

print("\n" + "=" * 80)
