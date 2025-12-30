"""
CORRECTED CALCULATION METHOD - ROLLING 5-YEAR PERCENTILE RANKING
(Matches the notebook methodology)

This script implements the CORRECT calculation methodology:
1. Calculates 5-year rolling CAGR for each index
2. Requires FULL 1825 days (5 years) of data for CAGR calculation
3. Ranks current CAGR against LAST 1825 DAYS of historical CAGRs (rolling window)
4. Produces percentile ranking (0.0 to 1.0)

Key Implementation:
- CAGR Window: 1825 days (5 years) - min_periods=1825
- Percentile Window: 1825 days (5 years) - min_periods=1825
- Ranking: Today's CAGR vs. recent 5-year CAGR history (NOT all history)
"""

import pandas as pd
import numpy as np
from pathlib import Path

def calculate_final_summary_v2(df, date_column='DATE'):
    """
    Calculate percentile rank using rolling 5-year window method.
    This matches the notebook implementation.
    
    Args:
        df: DataFrame with date column and index value columns
        date_column: Name of the date column
    
    Returns:
        DataFrame with final percentile rankings for the latest month
    """
    
    print("Step 1: Melting dataframe to long format...")
    # Melt to long format
    df_melted = df.melt(
        id_vars=[date_column], 
        var_name='SYMBOL', 
        value_name='VALUE'
    )
    df_melted = df_melted.dropna()
    df_melted['VALUE'] = pd.to_numeric(df_melted['VALUE'], errors='coerce')
    df_melted = df_melted.dropna()
    
    # Sort by SYMBOL and DATE
    df_melted = df_melted.sort_values(['SYMBOL', date_column]).reset_index(drop=True)
    
    print(f"   Data points: {len(df_melted)}")
    print(f"   Unique symbols: {df_melted['SYMBOL'].nunique()}")
    
    print("\nStep 2: Calculating 5-year rolling CAGR (1825 days)...")
    # Calculate 5-year rolling CAGR
    pr_cagr = 1825
    
    def calc_cagr(x):
        """Calculate CAGR: (Value_t / Value_t-1825)^(1/5) - 1"""
        if len(x) < pr_cagr:
            return np.nan
        first, last = x.iloc[0], x.iloc[-1]
        if first <= 0 or last <= 0:
            return np.nan
        return (last / first) ** (1/5) - 1
    
    df_melted['Rolling_CAGR'] = (
        df_melted.groupby('SYMBOL')['VALUE']
        .rolling(pr_cagr, min_periods=pr_cagr)  # Require full 5 years
        .apply(calc_cagr, raw=False)
        .reset_index(level=0, drop=True)
    )
    
    # Check how many valid CAGRs we have
    valid_cagr_count = df_melted['Rolling_CAGR'].notna().sum()
    print(f"   Valid CAGR values: {valid_cagr_count}")
    
    print("\nStep 3: Calculating percentile rank (rolling 1825-day window)...")
    # Calculate percentile rank against rolling 5-year window
    pr_rank = 1825
    
    def percentile_rank_rolling(x):
        """
        Rank the LATEST CAGR value against the last 1825 days of CAGR values.
        This is the KEY difference from the all-history method.
        """
        if len(x) < pr_rank:
            return np.nan
        x_clean = pd.Series(x).dropna()
        if len(x_clean) == 0:
            return np.nan
        # Rank the most recent value against the window
        return x_clean.rank(pct=True).iloc[-1]
    
    df_melted['Percentile_Rank'] = (
        df_melted.groupby('SYMBOL')['Rolling_CAGR']
        .rolling(pr_rank, min_periods=pr_rank)  # Require full 5-year window
        .apply(percentile_rank_rolling, raw=False)
        .reset_index(level=0, drop=True)
    )
    
    df_melted = df_melted.dropna(subset=['Percentile_Rank'])
    
    valid_rank_count = len(df_melted)
    print(f"   Valid percentile ranks: {valid_rank_count}")
    
    print("\nStep 4: Pivoting back to wide format...")
    # Pivot back to wide format
    df_processed = df_melted.pivot_table(
        values='Percentile_Rank', 
        index=date_column, 
        columns='SYMBOL'
    )
    
    print(f"   Shape: {df_processed.shape}")
    
    print("\nStep 5: Calculating monthly averages...")
    # Calculate monthly averages
    df_processed['year'] = df_processed.index.year
    df_processed['month'] = df_processed.index.month
    df_month_mean = df_processed.groupby(['year', 'month']).mean(numeric_only=True)
    df_month_mean.sort_values(by=['year', 'month'], ascending=False, inplace=True)
    
    print(f"   Months available: {len(df_month_mean)}")
    
    print("\nStep 6: Extracting latest month summary...")
    # Extract most recent month and transpose
    df_final_summary = df_month_mean.reset_index()
    latest_year = df_final_summary.iloc[0]['year']
    latest_month = df_final_summary.iloc[0]['month']
    print(f"   Latest month: {int(latest_year)}-{int(latest_month):02d}")
    
    df_final_summary = df_final_summary.iloc[0:1, :].transpose()
    df_final_summary.columns = ["final_pct_value"]
    df_final_summary.drop(["year", "month"], inplace=True)
    
    # Convert to numeric and sort
    df_final_summary['final_pct_value'] = pd.to_numeric(
        df_final_summary['final_pct_value'], 
        errors='coerce'
    )
    df_final_summary = df_final_summary.dropna()
    df_final_summary.sort_values(by='final_pct_value', ascending=True, inplace=True)
    
    print(f"\nFinal summary: {len(df_final_summary)} indices")
    
    return df_final_summary


def main():
    print("="*80)
    print("CORRECTED METHOD: Rolling 5-Year Percentile Ranking")
    print("(Matches notebook implementation)")
    print("="*80)
    print()
    
    # Load data
    csv_file = Path('data/Latest_Indices_rawdata_14112025.csv')
    if not csv_file.exists():
        print(f"Error: {csv_file} not found!")
        return
    
    print(f"Loading data from: {csv_file}")
    df = pd.read_csv(csv_file)
    
    # Convert DATE to datetime
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y')
    df = df.sort_values('DATE')
    
    print(f"Data loaded: {len(df)} rows, {len(df.columns)-1} index columns")
    print(f"Date range: {df['DATE'].min()} to {df['DATE'].max()}")
    print()
    
    # Calculate summary
    print("Starting calculation...")
    print("-"*80)
    df_final_summary = calculate_final_summary_v2(df, date_column='DATE')
    print("-"*80)
    
    # Save results
    output_file = 'data/CORRECTED_METHOD1_summary.xlsx'
    df_final_summary.to_excel(output_file)
    print(f"\n✓ Results saved to: {output_file}")
    
    # Display results
    print("\n" + "="*80)
    print("TOP 10 INDICES (Strongest Recent Performance)")
    print("="*80)
    print(df_final_summary.tail(10).to_string())
    
    print("\n" + "="*80)
    print("BOTTOM 10 INDICES (Weakest Recent Performance)")
    print("="*80)
    print(df_final_summary.head(10).to_string())
    
    # Statistics
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Total indices: {len(df_final_summary)}")
    print(f"Mean percentile: {df_final_summary['final_pct_value'].mean():.4f}")
    print(f"Median percentile: {df_final_summary['final_pct_value'].median():.4f}")
    print(f"Min percentile: {df_final_summary['final_pct_value'].min():.4f}")
    print(f"Max percentile: {df_final_summary['final_pct_value'].max():.4f}")
    print()


if __name__ == "__main__":
    main()
