"""
CALCULATION METHODOLOGY FOR CROSS-CHECKING

This document explains the exact calculation steps used to generate the percentile values.
"""

print("=" * 80)
print("CALCULATION METHODOLOGY - FOR CROSS-CHECKING")
print("=" * 80)

print("""
SOURCE DATA:
- File: data/Latest_Indices_rawdata_14112025.csv
- Contains: Daily values for each index over multiple years
- Date range: Multiple years of historical data

CALCULATION STEPS:
==================

STEP 1: Calculate 5-Year Rolling CAGR (Compound Annual Growth Rate)
--------------------------------------------------------------------
Formula: Rolling_CAGR = (Value_today / Value_5years_ago)^(1/5) - 1

Where:
- Value_today = Current day's index value
- Value_5years_ago = Index value from 1825 days ago (5 years × 365 days)
- Window = 1825 days (5 years)

Example:
If Nifty 50 today = 19500 and 5 years ago = 12000
Rolling_CAGR = (19500 / 12000)^(1/5) - 1 = (1.625)^0.2 - 1 = 0.1024 = 10.24%

STEP 2: Calculate Percentile Rank over 5-Year History
------------------------------------------------------
For each index, compare its current CAGR to its own 5-year CAGR history:

Formula: Percentile_Rank = Rank(current_CAGR) / Total_observations_in_5years

Where:
- Window = 1825 days (5 years of rolling CAGR values)
- Rank is calculated using pandas rank(pct=True) which gives percentile rank
- Range: 0.0 (worst) to 1.0 (best)

Example:
If current CAGR is better than 73.42% of all CAGR values in past 5 years:
Percentile_Rank = 0.7342

INTERPRETATION:
- 0.00 - 0.20: Very weak (bottom 20% of historical performance)
- 0.20 - 0.40: Below average
- 0.40 - 0.60: Average
- 0.60 - 0.80: Above average  
- 0.80 - 1.00: Very strong (top 20% of historical performance)

STEP 3: Monthly Average
------------------------
Average the percentile ranks for all trading days in the most recent month

STEP 4: Final Output
--------------------
The final percentile value shown on the webpage is the monthly average from
the most recent month in the dataset.

KEY NOTES:
==========
1. Each index is compared to its OWN historical performance (not vs other indices)
2. Higher percentile = Current performance is strong relative to its history
3. Lower percentile = Current performance is weak relative to its history
4. This is NOT a comparison between different indices
5. An index can have low absolute returns but high percentile if it's doing
   better than its own historical average

CROSS-CHECKING:
===============
To verify calculations manually:

1. Take any index (e.g., "Nifty Bank")
2. Get its daily values from Latest_Indices_rawdata_14112025.csv
3. For the latest date, calculate 5-year CAGR:
   CAGR = (Latest_Value / Value_1825_days_ago)^(1/5) - 1
4. Calculate all rolling CAGRs for past 5 years
5. Rank the latest CAGR among all these values (percentile)
6. Average for the month

CURRENT STATUS:
===============
❌ We are NOT using these calculated values
✅ We are using values DIRECTLY from Excel file: 251229_Final_summary.xlsx
   - This Excel file was provided by you with pre-calculated percentile values
   - The webpage displays these exact values without any recalculation

DATA FLOW:
==========
Option 1 (Original - not currently used):
Raw CSV → calculate_summary.py → calculated_final_summary.xlsx

Option 2 (Current - what we're using):
Your Excel (251229_Final_summary.xlsx) → update_from_excel.py → 
summary_data.json → create_proper_mapping.py → 
indices_with_short_names.json → Webpage

""")

print("=" * 80)
print("\nTo run the calculation yourself:")
print("  python calculate_summary.py")
print("\nTo verify values match your Excel:")
print("  python verify_values.py")
print("=" * 80)
