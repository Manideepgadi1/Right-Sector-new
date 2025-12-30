"""
NEW CALCULATION METHOD - STRICT 5-YEAR ROLLING CAGR WITH PERCENTILE RANKING

This script implements the improved calculation methodology:
1. Calculates 5-year rolling CAGR for each index
2. Requires FULL 1825 days (5 years) of data - NO partial calculations
3. Ranks current CAGR against ALL historical 5-year CAGRs
4. Produces percentile ranking (0.0 to 1.0)

Key Difference from OLD method:
- OLD: min_periods=1 (allows calculations with incomplete data)
- NEW: min_periods=1825 (requires full 5 years of data)

This produces more accurate and reliable rankings.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def calculate_rolling_cagr(df, column, periods=1825):
    """
    Calculate 5-year rolling CAGR for a specific column.
    
    Args:
        df: DataFrame with DATE index
        column: Column name to calculate CAGR for
        periods: Number of days for rolling window (default: 1825 = 5 years)
    
    Returns:
        Series with CAGR values
    """
    # Get the values
    values = df[column]
    
    # Calculate CAGR: (Value_t / Value_t-periods)^(1/5) - 1
    # Only calculate when we have full 5 years of data
    cagr = (values / values.shift(periods)).pow(1/5) - 1
    
    return cagr

def calculate_percentile_rank(series):
    """
    Calculate percentile rank for the latest value against all historical values.
    
    Args:
        series: Series with CAGR values
    
    Returns:
        Float: Percentile rank of latest value (0.0 to 1.0)
    """
    # Remove NaN values
    valid_values = series.dropna()
    
    if len(valid_values) == 0:
        return np.nan
    
    # Get the latest value
    latest_value = valid_values.iloc[-1]
    
    # Calculate how many historical values are less than current
    rank = (valid_values < latest_value).sum()
    
    # Convert to percentile (0.0 to 1.0)
    percentile = rank / len(valid_values)
    
    return percentile

def main():
    print("="*80)
    print("NEW CALCULATION METHOD - STRICT 5-YEAR ROLLING CAGR")
    print("="*80)
    print()
    
    # Load data
    csv_file = Path('data/Latest_Indices_rawdata_14112025.csv')
    if not csv_file.exists():
        print(f"Error: {csv_file} not found!")
        return
    
    print(f"Loading data from: {csv_file}")
    df = pd.read_csv(csv_file)
    
    # Convert DATE to datetime and set as index
    df['DATE'] = pd.to_datetime(df['DATE'])
    df = df.set_index('DATE')
    df = df.sort_index()
    
    print(f"Data loaded: {len(df)} rows")
    print(f"Date range: {df.index.min()} to {df.index.max()}")
    print(f"Total columns: {len(df.columns)}")
    print()
    
    # Calculate for all indices
    results = []
    
    print("Calculating 5-year rolling CAGR with min_periods=1825...")
    print("(This requires FULL 5 years of data - more strict)")
    print()
    
    for col in df.columns:
        # Skip if column has no data
        if df[col].isna().all():
            continue
        
        try:
            # Calculate 5-year rolling CAGR (1825 days = 5 years)
            # CRITICAL: min_periods=1825 means we REQUIRE full 5 years
            cagr_series = calculate_rolling_cagr(df, col, periods=1825)
            
            # Only proceed if we have valid CAGR values
            valid_cagrs = cagr_series.dropna()
            if len(valid_cagrs) == 0:
                continue
            
            # Calculate percentile rank
            percentile = calculate_percentile_rank(cagr_series)
            
            if not np.isnan(percentile):
                results.append({
                    'Index': col,
                    'Percentile': round(percentile, 6),
                    'Latest_CAGR': round(valid_cagrs.iloc[-1], 6),
                    'Mean_CAGR': round(valid_cagrs.mean(), 6),
                    'Median_CAGR': round(valid_cagrs.median(), 6),
                    'Min_CAGR': round(valid_cagrs.min(), 6),
                    'Max_CAGR': round(valid_cagrs.max(), 6),
                    'Data_Points': len(valid_cagrs)
                })
                
                print(f"✓ {col}: {percentile:.4f} (CAGR: {valid_cagrs.iloc[-1]:.4f})")
        
        except Exception as e:
            print(f"✗ {col}: Error - {str(e)}")
            continue
    
    print()
    print("="*80)
    print(f"RESULTS: {len(results)} indices calculated")
    print("="*80)
    
    # Create DataFrame and sort by percentile
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Percentile', ascending=False)
    
    # Save to Excel
    output_file = 'data/NEW_METHOD_summary.xlsx'
    results_df.to_excel(output_file, index=False)
    print(f"\nResults saved to: {output_file}")
    
    # Show top 10 and bottom 10
    print("\nTOP 10 INDICES (Highest Percentile):")
    print(results_df.head(10)[['Index', 'Percentile', 'Latest_CAGR']].to_string(index=False))
    
    print("\nBOTTOM 10 INDICES (Lowest Percentile):")
    print(results_df.tail(10)[['Index', 'Percentile', 'Latest_CAGR']].to_string(index=False))
    
    # Statistics
    print("\n" + "="*80)
    print("STATISTICS:")
    print("="*80)
    print(f"Total indices: {len(results_df)}")
    print(f"Average percentile: {results_df['Percentile'].mean():.4f}")
    print(f"Median percentile: {results_df['Percentile'].median():.4f}")
    print(f"Average data points: {results_df['Data_Points'].mean():.0f}")
    print()

if __name__ == "__main__":
    main()
