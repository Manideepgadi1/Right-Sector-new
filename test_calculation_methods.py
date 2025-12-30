"""
TEST SCRIPT: Compare OLD vs NEW calculation methods
This will NOT modify the website - just for verification
"""

import pandas as pd
import numpy as np
import json

print("=" * 80)
print("CALCULATION COMPARISON TEST")
print("=" * 80)

# Read the raw data
print("\nReading raw data...")
df = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv')
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y')
print(f"Data loaded: {len(df)} rows, {len(df.columns)} columns")
print(f"Date range: {df['DATE'].min()} to {df['DATE'].max()}")

# ============================================================================
# OLD METHOD (Current)
# ============================================================================
def calculate_old_method(df_with_daily_values, date_column='DATE'):
    """OLD calculation method"""
    
    df_melted = df_with_daily_values.melt(
        id_vars=[date_column], 
        var_name='SYMBOL', 
        value_name='VALUE'
    )
    df_melted = df_melted.dropna()
    df_melted['VALUE'] = pd.to_numeric(df_melted['VALUE'], errors='coerce')
    df_melted = df_melted.dropna()
    
    # OLD: Calculate 5-Year Rolling CAGR without proper sorting
    pr_cagr = 1825
    df_melted['Rolling_CAGR'] = (
        df_melted.groupby(['SYMBOL'])['VALUE']
        .rolling(pr_cagr)
        .apply(lambda x: (x.iloc[-1]/x.iloc[0])**(1/5) - 1 if len(x) >= pr_cagr and x.iloc[0] > 0 else np.nan, raw=False)
        .round(5)
        .reset_index(0, drop=True)
    )
    
    # OLD: Calculate Percentile Rank
    pr_rank = 5 * 365
    def percentile_rank(x):
        if len(x) > 0:
            return pd.Series(x).rank(pct=True).iloc[-1]
        return np.nan
    
    df_melted['Percentile_Rank'] = (
        df_melted.groupby(['SYMBOL'])['Rolling_CAGR']
        .rolling(pr_rank, min_periods=1)
        .apply(percentile_rank, raw=False)
        .round(5)
        .reset_index(0, drop=True)
    )
    
    df_melted = df_melted.dropna(subset=['Percentile_Rank'])
    
    df_processed = df_melted.pivot_table(
        values='Percentile_Rank', 
        index=date_column, 
        columns='SYMBOL'
    )
    
    df_processed['year'] = df_processed.index.year
    df_processed['month'] = df_processed.index.month
    df_month_mean = df_processed.groupby(['year', 'month']).mean()
    df_month_mean.sort_values(by=['year', 'month'], ascending=False, inplace=True)
    
    df_final_summary = df_month_mean.reset_index()
    df_final_summary = df_final_summary.iloc[0:1, :].transpose()
    df_final_summary.columns = ["final_pct_value"]
    df_final_summary.drop(["year", "month"], inplace=True)
    
    df_final_summary['final_pct_value'] = pd.to_numeric(
        df_final_summary['final_pct_value'], 
        errors='coerce'
    )
    df_final_summary.sort_values(by='final_pct_value', ascending=True, inplace=True)
    
    return df_final_summary


# ============================================================================
# NEW METHOD (Your proposed changes)
# ============================================================================
def calculate_new_method(df_with_daily_values, date_column='DATE'):
    """NEW calculation method with fixes"""
    
    df_melted = df_with_daily_values.melt(
        id_vars=[date_column], 
        var_name='SYMBOL', 
        value_name='VALUE'
    )
    df_melted = df_melted.dropna()
    df_melted['VALUE'] = pd.to_numeric(df_melted['VALUE'], errors='coerce')
    df_melted = df_melted.dropna()
    
    # NEW: Sort by SYMBOL and DATE to ensure proper rolling window
    df_melted = df_melted.sort_values([date_column, 'SYMBOL']).reset_index(drop=True)
    
    # NEW: Calculate 5-Year Rolling CAGR with stricter requirements
    pr_cagr = 1825
    
    def calculate_cagr(x):
        """Calculate CAGR safely"""
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
    
    # NEW: Calculate Percentile Rank with full window requirement
    pr_rank = 1825
    
    def percentile_rank(x):
        """Calculate percentile rank of the most recent value"""
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


# ============================================================================
# RUN BOTH METHODS
# ============================================================================

print("\n" + "=" * 80)
print("RUNNING OLD METHOD...")
print("=" * 80)
try:
    df_old = calculate_old_method(df.copy())
    print(f"✓ Old method completed: {len(df_old)} indices")
except Exception as e:
    print(f"✗ Old method failed: {e}")
    df_old = None

print("\n" + "=" * 80)
print("RUNNING NEW METHOD...")
print("=" * 80)
try:
    df_new = calculate_new_method(df.copy())
    print(f"✓ New method completed: {len(df_new)} indices")
except Exception as e:
    print(f"✗ New method failed: {e}")
    df_new = None

# ============================================================================
# COMPARE RESULTS
# ============================================================================

if df_old is not None and df_new is not None:
    print("\n" + "=" * 80)
    print("COMPARISON RESULTS")
    print("=" * 80)
    
    # Compare counts
    print(f"\nIndices count:")
    print(f"  Old method: {len(df_old)}")
    print(f"  New method: {len(df_new)}")
    print(f"  Difference: {len(df_old) - len(df_new)}")
    
    # Find common indices
    common_indices = set(df_old.index).intersection(set(df_new.index))
    print(f"\n  Common indices: {len(common_indices)}")
    
    if len(common_indices) > 0:
        # Compare values for common indices
        differences = []
        for idx in common_indices:
            old_val = df_old.loc[idx, 'final_pct_value']
            new_val = df_new.loc[idx, 'final_pct_value']
            diff = abs(old_val - new_val)
            if diff > 0.0001:  # More than 0.01% difference
                differences.append({
                    'index': idx,
                    'old': old_val,
                    'new': new_val,
                    'diff': diff
                })
        
        if differences:
            print(f"\n⚠️  SIGNIFICANT DIFFERENCES FOUND: {len(differences)} indices")
            print("\nTop 10 largest differences:")
            differences.sort(key=lambda x: x['diff'], reverse=True)
            for item in differences[:10]:
                print(f"  {item['index']}")
                print(f"    Old: {item['old']:.6f}  New: {item['new']:.6f}  Diff: {item['diff']:.6f}")
        else:
            print("\n✓ All values match (within 0.0001 tolerance)")
    
    # Sample comparison
    print("\n" + "=" * 80)
    print("SAMPLE VALUES (First 10 common indices)")
    print("=" * 80)
    sample_indices = list(common_indices)[:10]
    print(f"\n{'Index':<50} {'Old':<12} {'New':<12} {'Diff':<12}")
    print("-" * 86)
    for idx in sample_indices:
        old_val = df_old.loc[idx, 'final_pct_value']
        new_val = df_new.loc[idx, 'final_pct_value']
        diff = old_val - new_val
        print(f"{idx:<50} {old_val:<12.6f} {new_val:<12.6f} {diff:<12.6f}")

print("\n" + "=" * 80)
print("KEY IMPROVEMENTS IN NEW METHOD:")
print("=" * 80)
print("""
1. ✓ Explicit sorting by DATE and SYMBOL before rolling calculations
2. ✓ Require full 1825-day window (no min_periods=1 which was risky)
3. ✓ Safer CAGR calculation with explicit length checks
4. ✓ Better handling of edge cases (negative/zero values)
5. ✓ Cleaner percentile_rank function with NaN handling
6. ✓ Added numeric_only=True to avoid pandas warnings

RECOMMENDATION:
- If differences are minimal (< 0.01), new method is more robust
- If differences are significant, investigate which is correct
- New method is stricter and more reliable for production use
""")

print("=" * 80)
print("Test complete. No files were modified.")
print("=" * 80)
