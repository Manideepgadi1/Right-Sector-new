# Indices Performance Heatmap

A beautiful, interactive web application to visualize financial indices performance using a color-coded heatmap based on 5-year rolling CAGR percentile rankings.

## 📊 Features

- **Interactive Heatmap**: Color-coded visualization from red (low performance) to green (high performance)
- **Real-time Search**: Filter indices by name instantly
- **Sorting Options**: Sort by value ascending, descending, or reset to original order
- **Statistics Dashboard**: View total indices, average values, high/low performers
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Beautiful UI**: Modern gradient design with smooth animations

## 🚀 Quick Start

### Step 1: Calculate the Summary Data

Run the Python script to calculate percentile rankings from raw data:

```bash
python calculate_summary.py
```

This will:
- Read `data/Latest_Indices_rawdata_14112025.csv`
- Calculate 5-year rolling CAGR
- Compute percentile ranks for each index
- Generate `data/summary_data.json` and `data/calculated_final_summary.xlsx`

### Step 2: Start the Web Server

```bash
python server.py
```

### Step 3: Open in Browser

Visit: http://localhost:8000/index.html

## 📁 File Structure

```
.
├── index.html                          # Main web page
├── calculate_summary.py                # Python script for data calculation
├── server.py                           # Simple HTTP server
├── data/
│   ├── Latest_Indices_rawdata_14112025.csv  # Raw daily index data
│   ├── summary_data.json               # Calculated percentile data (generated)
│   └── calculated_final_summary.xlsx   # Excel output (generated)
└── README.md                           # This file
```

## 🎨 Color Scheme

| Range | Color | Performance |
|-------|-------|------------|
| 0.00 - 0.20 | 🔴 Red | Very Low |
| 0.20 - 0.35 | 🟠 Orange | Low |
| 0.35 - 0.50 | 🟡 Yellow-Orange | Medium-Low |
| 0.50 - 0.65 | 🟡 Yellow | Medium |
| 0.65 - 0.80 | 🟢 Light Green | Medium-High |
| 0.80 - 0.90 | 🟢 Green | High |
| 0.90 - 1.00 | 🟢 Dark Green | Very High |

## 📊 How It Works

### 5-Year Rolling CAGR Calculation

The system calculates the Compound Annual Growth Rate (CAGR) over a rolling 5-year window:

$$CAGR = \left(\frac{Value_{t}}{Value_{t-1825}}\right)^{\frac{1}{5}} - 1$$

### Percentile Ranking

Each index's current CAGR is ranked against its own 5-year historical CAGR values:

$$Percentile\_Rank_t = \frac{rank(CAGR_t)}{count(CAGR_{[t-1825:t]})}$$

Where:
- Values close to **0** = index is performing poorly compared to its 5-year history
- Values close to **1** = index is performing strongly compared to its 5-year history

### Monthly Average

The final value shown is the average percentile rank for the most recent month.

## 🔧 Requirements

- Python 3.7+
- pandas
- numpy
- openpyxl (for Excel export)

Install dependencies:

```bash
pip install pandas numpy openpyxl
```

## 📝 Usage

1. **Search**: Type in the search box to filter indices
2. **Sort**: Click "Sort Ascending" or "Sort Descending" to reorder
3. **Reset**: Click "Reset" to return to original order
4. **Hover**: Hover over cells to see subtle zoom effect

## 🔄 Updating Data

When you receive new raw data:

1. Replace `data/Latest_Indices_rawdata_14112025.csv` with the new file
2. Run `python calculate_summary.py` to recalculate
3. Refresh the browser page

## 📧 Support

For issues or questions, please check the data format matches the expected CSV structure with:
- DATE column (format: dd/mm/yy)
- Multiple index columns with daily values

## 🎯 Current Statistics

Based on the latest calculation:
- **Total Indices**: 122
- **Data Range**: August 2005 - November 2025
- **Calculation Window**: 5 years (1825 days)

## 🌐 Browser Compatibility

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

---

**Made with ❤️ for financial data visualization**
