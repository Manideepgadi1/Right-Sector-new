"""
Detailed Comparison for Sample Indices
Shows step-by-step calculation for verification
"""

import pandas as pd
import numpy as np
import json

print("=" * 80)
print("DETAILED CALCULATION FOR SAMPLE INDICES")
print("=" * 80)

# Read data
df_raw = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv')
df_raw['DATE'] = pd.to_datetime(df_raw['DATE'], format='%d/%m/%y')

# Read Excel values
excel_df = pd.read_excel('data/251229_Final_summary.xlsx')
excel_lookup = {}
for idx, row in excel_df.iterrows():
    name = str(row['SYMBOL']).strip()
    value = float(row['final_pct_value'])
    excel_lookup[name] = value

# Select 5 sample indices to analyze in detail
# These are the actual column names from the CSV
sample_indices = [
    'NIFTY IT',
    'NIFTY BANK',
    'NIFTY AUTO',
    'NIFTY PSU BANK',
    'NIFTY 500'
]

# Mapping to Excel names (which have "tri - " prefix)
csv_to_excel = {
    'NIFTY IT': 'tri - Nifty IT',
    'NIFTY BANK': 'tri - Nifty Bank',
    'NIFTY AUTO': 'tri - NIFTY AUTO',
    'NIFTY PSU BANK': 'tri - NIFTY PSU BANK',
    'NIFTY 500': 'tri - NIFTY 500'
}

print("\nSample indices selected for detailed analysis:")
for idx in sample_indices:
    print(f"  - {idx}")

print("\n" + "=" * 80)

for symbol in sample_indices:
    print(f"\n{'=' * 80}")
    print(f"INDEX: {symbol}")
    print(f"{'=' * 80}")
    
    # Check if column exists
    if symbol not in df_raw.columns:
        print(f"⚠️  Not found in raw data CSV")
        continue
    
    # Get the data for this index
    index_data = df_raw[['DATE', symbol]].copy()
    index_data.columns = ['DATE', 'VALUE']
    index_data = index_data.dropna()
    index_data = index_data.sort_values('DATE')
    
    print(f"\n1. RAW DATA INFO:")
    print(f"   Total data points: {len(index_data)}")
    print(f"   Date range: {index_data['DATE'].min().date()} to {index_data['DATE'].max().date()}")
    print(f"   Total days: {(index_data['DATE'].max() - index_data['DATE'].min()).days}")
    
    # Show first and last few values
    print(f"\n   First 3 values:")
    for _, row in index_data.head(3).iterrows():
        print(f"      {row['DATE'].date()}: {row['VALUE']:.2f}")
    
    print(f"\n   Last 3 values:")
    for _, row in index_data.tail(3).iterrows():
        print(f"      {row['DATE'].date()}: {row['VALUE']:.2f}")
    
    # Calculate 5-year rolling CAGR for most recent date
    print(f"\n2. CALCULATE 5-YEAR ROLLING CAGR (Most recent):")
    
    if len(index_data) >= 1825:
        latest_value = index_data.iloc[-1]['VALUE']
        value_5y_ago = index_data.iloc[-1825]['VALUE']
        latest_date = index_data.iloc[-1]['DATE']
        date_5y_ago = index_data.iloc[-1825]['DATE']
        
        cagr = (latest_value / value_5y_ago) ** (1/5) - 1
        
        print(f"   Latest date: {latest_date.date()}")
        print(f"   Latest value: {latest_value:.2f}")
        print(f"   Date 1825 days ago: {date_5y_ago.date()}")
        print(f"   Value 1825 days ago: {value_5y_ago:.2f}")
        print(f"   Formula: ({latest_value:.2f} / {value_5y_ago:.2f})^(1/5) - 1")
        print(f"   CAGR = {cagr:.6f} = {cagr*100:.2f}%")
        
        # Calculate all rolling CAGRs for past 5 years
        print(f"\n3. CALCULATE ALL ROLLING CAGRs (Past 1825 days):")
        
        all_cagrs = []
        for i in range(1825, len(index_data)):
            curr_val = index_data.iloc[i]['VALUE']
            past_val = index_data.iloc[i-1825]['VALUE']
            if past_val > 0 and curr_val > 0:
                cagr_i = (curr_val / past_val) ** (1/5) - 1
                all_cagrs.append(cagr_i)
        
        print(f"   Total CAGR values calculated: {len(all_cagrs)}")
        print(f"   CAGR range: {min(all_cagrs):.6f} to {max(all_cagrs):.6f}")
        print(f"   Mean CAGR: {np.mean(all_cagrs):.6f}")
        print(f"   Median CAGR: {np.median(all_cagrs):.6f}")
        
        # Calculate percentile rank
        print(f"\n4. CALCULATE PERCENTILE RANK:")
        
        latest_cagr = all_cagrs[-1]
        cagrs_series = pd.Series(all_cagrs)
        percentile_rank = cagrs_series.rank(pct=True).iloc[-1]
        
        print(f"   Latest CAGR: {latest_cagr:.6f}")
        print(f"   Rank among {len(all_cagrs)} values: {cagrs_series.rank().iloc[-1]:.0f}")
        print(f"   Percentile Rank: {percentile_rank:.6f}")
        print(f"   Interpretation: Current CAGR is better than {percentile_rank*100:.2f}% of past 5 years")
        
        # Compare with Excel
        print(f"\n5. COMPARISON WITH EXCEL:")
        excel_name = csv_to_excel.get(symbol, symbol)
        excel_value = excel_lookup.get(excel_name, None)
        if excel_value is not None:
            print(f"   Excel value: {excel_value:.6f}")
            print(f"   NEW calculated: {percentile_rank:.6f}")
            diff = abs(excel_value - percentile_rank)
            diff_pct = (diff / excel_value * 100) if excel_value > 0 else 0
            print(f"   Difference: {diff:.6f} ({diff_pct:.1f}%)")
            
            if diff < 0.01:
                print(f"   ✓ Values match closely")
            else:
                print(f"   ⚠️  Significant difference!")
                if excel_value < percentile_rank:
                    print(f"      Excel is LOWER (more bearish)")
                else:
                    print(f"      Excel is HIGHER (more bullish)")
        else:
            print(f"   ⚠️  Not found in Excel (searched for: {excel_name})")
        
    else:
        print(f"   ⚠️  Insufficient data: Only {len(index_data)} days (need 1825)")
        print(f"   Cannot calculate 5-year rolling CAGR")
        excel_name = csv_to_excel.get(symbol, symbol)
        excel_value = excel_lookup.get(excel_name, None)
        if excel_value is not None:
            print(f"\n   Excel shows value: {excel_value:.6f}")
            print(f"   This was likely calculated with OLD method (min_periods=1)")

print("\n" + "=" * 80)
print("SUMMARY:")
print("=" * 80)
print("""
The NEW method:
- Requires FULL 1825 days (5 years) of data
- Ranks current CAGR vs ALL historical CAGRs in 5-year window
- More strict and accurate

The OLD method (likely used in Excel):
- Uses min_periods=1, allowing partial data
- May calculate with less than 5 years
- More permissive but less accurate

If Excel values differ significantly, it means they were calculated
with incomplete data or different methodology.
""")
print("=" * 80)
