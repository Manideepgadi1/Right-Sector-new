"""
Create comprehensive Excel file with corrected calculation values
"""

import pandas as pd
from pathlib import Path

def main():
    print("Creating comprehensive Excel file with corrected values...")
    print("="*80)
    
    # Load the corrected summary
    summary_file = Path('data/CORRECTED_METHOD1_summary.xlsx')
    if not summary_file.exists():
        print(f"Error: {summary_file} not found!")
        return
    
    df_summary = pd.read_excel(summary_file)
    df_summary.columns = ['Index', 'Percentile']
    
    print(f"✓ Loaded {len(df_summary)} indices")
    
    # Sort by percentile descending
    df_summary = df_summary.sort_values('Percentile', ascending=False)
    
    # Round percentile to 6 decimal places
    df_summary['Percentile'] = df_summary['Percentile'].round(6)
    
    # Add rank column
    df_summary.insert(0, 'Rank', range(1, len(df_summary) + 1))
    
    # Add interpretation column
    def get_interpretation(pct):
        if pct >= 0.8:
            return "Very Bullish"
        elif pct >= 0.6:
            return "Bullish"
        elif pct >= 0.4:
            return "Neutral"
        elif pct >= 0.2:
            return "Bearish"
        else:
            return "Very Bearish"
    
    df_summary['Interpretation'] = df_summary['Percentile'].apply(get_interpretation)
    
    # Create Excel writer with multiple sheets
    output_file = 'data/CORRECTED_VALUES_FULL.xlsx'
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Sheet 1: Full summary sorted by percentile
        df_summary.to_excel(writer, sheet_name='All Indices', index=False)
        
        # Sheet 2: Top 20
        df_summary.head(20).to_excel(writer, sheet_name='Top 20 Bullish', index=False)
        
        # Sheet 3: Bottom 20
        df_summary.tail(20).to_excel(writer, sheet_name='Bottom 20 Bearish', index=False)
        
        # Sheet 4: By category
        categories = {
            'Very Bullish (>0.8)': df_summary[df_summary['Percentile'] >= 0.8],
            'Bullish (0.6-0.8)': df_summary[(df_summary['Percentile'] >= 0.6) & (df_summary['Percentile'] < 0.8)],
            'Neutral (0.4-0.6)': df_summary[(df_summary['Percentile'] >= 0.4) & (df_summary['Percentile'] < 0.6)],
            'Bearish (0.2-0.4)': df_summary[(df_summary['Percentile'] >= 0.2) & (df_summary['Percentile'] < 0.4)],
            'Very Bearish (<0.2)': df_summary[df_summary['Percentile'] < 0.2]
        }
        
        # Create summary by category
        category_summary = pd.DataFrame([
            {'Category': cat, 'Count': len(df), 'Avg Percentile': df['Percentile'].mean()}
            for cat, df in categories.items()
        ])
        category_summary.to_excel(writer, sheet_name='Category Summary', index=False)
        
        # Sheet 5: Statistics
        stats = pd.DataFrame({
            'Metric': [
                'Total Indices',
                'Mean Percentile',
                'Median Percentile',
                'Min Percentile',
                'Max Percentile',
                'Std Dev',
                'Very Bullish Count (>0.8)',
                'Bullish Count (0.6-0.8)',
                'Neutral Count (0.4-0.6)',
                'Bearish Count (0.2-0.4)',
                'Very Bearish Count (<0.2)'
            ],
            'Value': [
                len(df_summary),
                round(df_summary['Percentile'].mean(), 4),
                round(df_summary['Percentile'].median(), 4),
                round(df_summary['Percentile'].min(), 4),
                round(df_summary['Percentile'].max(), 4),
                round(df_summary['Percentile'].std(), 4),
                len(df_summary[df_summary['Percentile'] >= 0.8]),
                len(df_summary[(df_summary['Percentile'] >= 0.6) & (df_summary['Percentile'] < 0.8)]),
                len(df_summary[(df_summary['Percentile'] >= 0.4) & (df_summary['Percentile'] < 0.6)]),
                len(df_summary[(df_summary['Percentile'] >= 0.2) & (df_summary['Percentile'] < 0.4)]),
                len(df_summary[df_summary['Percentile'] < 0.2])
            ]
        })
        stats.to_excel(writer, sheet_name='Statistics', index=False)
    
    print(f"\n✓ Excel file created: {output_file}")
    print("\nSheets created:")
    print("  1. All Indices - Complete list sorted by percentile")
    print("  2. Top 20 Bullish - Strongest performers")
    print("  3. Bottom 20 Bearish - Weakest performers")
    print("  4. Category Summary - Breakdown by performance category")
    print("  5. Statistics - Overall statistics")
    
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    print(f"Total Indices: {len(df_summary)}")
    print(f"Mean Percentile: {df_summary['Percentile'].mean():.4f}")
    print(f"Median Percentile: {df_summary['Percentile'].median():.4f}")
    print(f"\nDistribution:")
    print(f"  Very Bullish (>0.8):  {len(df_summary[df_summary['Percentile'] >= 0.8])} indices")
    print(f"  Bullish (0.6-0.8):    {len(df_summary[(df_summary['Percentile'] >= 0.6) & (df_summary['Percentile'] < 0.8)])} indices")
    print(f"  Neutral (0.4-0.6):    {len(df_summary[(df_summary['Percentile'] >= 0.4) & (df_summary['Percentile'] < 0.6)])} indices")
    print(f"  Bearish (0.2-0.4):    {len(df_summary[(df_summary['Percentile'] >= 0.2) & (df_summary['Percentile'] < 0.4)])} indices")
    print(f"  Very Bearish (<0.2):  {len(df_summary[df_summary['Percentile'] < 0.2])} indices")
    
    print("\n" + "="*80)
    print("TOP 10 INDICES")
    print("="*80)
    print(df_summary.head(10)[['Rank', 'Index', 'Percentile', 'Interpretation']].to_string(index=False))
    
    print("\n" + "="*80)
    print("BOTTOM 10 INDICES")
    print("="*80)
    print(df_summary.tail(10)[['Rank', 'Index', 'Percentile', 'Interpretation']].to_string(index=False))
    
    print("\n✓ Done!")

if __name__ == "__main__":
    main()
