"""
Calculate percentile rank summary for indices
This script processes the raw data and generates the final summary
"""

import pandas as pd
import numpy as np
import json

def calculate_final_summary(df_with_daily_values, date_column='DATE'):
    """
    Calculate percentile rank summary for the most recent month
    
    Parameters:
    -----------
    df_with_daily_values : DataFrame
        Must have a date column and multiple columns with daily index values
    date_column : str
        Name of the date column (default: 'DATE')
    
    Returns:
    --------
    DataFrame with percentile ranks for each index in the most recent month
    """
    
    # Step 1: Melt dataframe to long format
    df_melted = df_with_daily_values.melt(
        id_vars=[date_column], 
        var_name='SYMBOL', 
        value_name='VALUE'
    )
    df_melted = df_melted.dropna()
    df_melted['VALUE'] = pd.to_numeric(df_melted['VALUE'], errors='coerce')
    df_melted = df_melted.dropna()
    
    # Step 2: Calculate 5-Year Rolling CAGR
    # Formula: (Value_now / Value_5_years_ago)^(1/5) - 1
    pr_cagr = 1825  # 5 years in days
    df_melted['Rolling_CAGR'] = (
        df_melted.groupby(['SYMBOL'])['VALUE']
        .rolling(pr_cagr)
        .apply(lambda x: (x.iloc[-1]/x.iloc[0])**(1/5) - 1 if len(x) >= pr_cagr and x.iloc[0] > 0 else np.nan, raw=False)
        .round(5)
        .reset_index(0, drop=True)
    )
    
    # Step 3: Calculate Percentile Rank over last 5 years
    # This ranks each index's current CAGR against its own 5-year history
    pr_rank = 5 * 365  # 5 years
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
    
    # Step 4: Pivot back to wide format
    df_processed = df_melted.pivot_table(
        values='Percentile_Rank', 
        index=date_column, 
        columns='SYMBOL'
    )
    
    # Step 5: Calculate monthly averages
    df_processed['year'] = df_processed.index.year
    df_processed['month'] = df_processed.index.month
    df_month_mean = df_processed.groupby(['year', 'month']).mean()
    df_month_mean.sort_values(by=['year', 'month'], ascending=False, inplace=True)
    
    # Step 6: Extract most recent month and transpose
    df_final_summary = df_month_mean.reset_index()
    df_final_summary = df_final_summary.iloc[0:1, :].transpose()
    df_final_summary.columns = ["final_pct_value"]
    df_final_summary.drop(["year", "month"], inplace=True)
    
    # Step 7: Convert to numeric and sort
    df_final_summary['final_pct_value'] = pd.to_numeric(
        df_final_summary['final_pct_value'], 
        errors='coerce'
    )
    df_final_summary.sort_values(by='final_pct_value', ascending=True, inplace=True)
    
    return df_final_summary


if __name__ == "__main__":
    # Read the raw data
    print("Reading raw data...")
    df = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv')
    
    # Convert DATE column to datetime
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y')
    
    print(f"Data loaded: {len(df)} rows, {len(df.columns)} columns")
    print(f"Date range: {df['DATE'].min()} to {df['DATE'].max()}")
    
    # Calculate summary
    print("\nCalculating percentile rank summary...")
    df_final_summary = calculate_final_summary(df, date_column='DATE')
    
    print(f"\nFinal summary calculated for {len(df_final_summary)} indices")
    
    # Save to Excel
    df_final_summary.to_excel('data/calculated_final_summary.xlsx')
    print("Saved to data/calculated_final_summary.xlsx")
    
    # Also save as JSON for web use
    summary_dict = df_final_summary['final_pct_value'].to_dict()
    with open('data/summary_data.json', 'w') as f:
        json.dump(summary_dict, f, indent=2)
    print("Saved to data/summary_data.json")
    
    # Display top 10 and bottom 10
    print("\n=== BOTTOM 10 (Weakest Performance) ===")
    print(df_final_summary.head(10))
    
    print("\n=== TOP 10 (Strongest Performance) ===")
    print(df_final_summary.tail(10))
