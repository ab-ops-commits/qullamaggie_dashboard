# Qullamaggie EOD Stock Screener Dashboard

An automated daily screening dashboard for Indian equity markets, identifying high-quality Qullamaggie-style trading setups across Nifty 500 and Nifty Microcap 250 stocks.

## 🎯 Overview

This dashboard automatically screens **750 stocks daily** (Nifty 500 + Microcap 250) for momentum trading opportunities based on Qullamaggie methodology. It identifies stocks with:

- Strong relative strength vs Nifty 500
- Tight consolidation patterns
- High average daily range (volatility)
- Recent price momentum
- Quality grading system (A+, A, B, C)

**Live Dashboard:** [https://ab-ops-commits.github.io/qullamaggie_dashboard/](https://ab-ops-commits.github.io/qullamaggie_dashboard/)

## 📊 Features

### Dual Universe Screening
- **Nifty 500:** Large & mid-cap stocks with higher liquidity
- **Nifty Microcap 250:** Small-cap stocks with higher growth potential
- Switch between universes instantly via dropdown selector

### Key Metrics Displayed
- **ADR % (Average Daily Range):** Volatility measure over 20 days
- **Prior Move:** Recent price momentum (20-day gain)
- **RS (Relative Strength):** Performance vs Nifty 500 index
- **Consolidation Days:** Number of days in tight range
- **Volume:** Average daily trading volume
- **Market Cap:** Company market capitalization
- **Grade:** Quality rating (A+, A, B, C) based on combined factors

### Automatic Daily Updates
- Runs automatically every day at **6:00 PM IST** (after market close)
- Fetches fresh OHLCV data via Yahoo Finance
- Updates both JSON data files
- GitHub Pages auto-deploys updated dashboard

### Grading System

**Grade A+ (Best Setups):**
- ADR > 3.5%
- Recent move > 15%
- RS > 110 (outperforming market)
- Consolidation: 5-15 days

**Grade A:**
- ADR > 3%
- Recent move > 10%
- RS > 105
- Consolidation: 5-20 days

**Grade B:**
- ADR > 2%
- Recent move > 5%
- RS > 100
- Some consolidation

**Grade C:**
- Meets minimum criteria but lower scores

## 🏗️ Project Structure

```
qullamaggie_dashboard/
├── index.html              # Dashboard UI with interactive table
├── data/
│   ├── nifty500.json      # Screened Nifty 500 stocks data
│   └── microcap250.json   # Screened Microcap 250 stocks data
├── scripts/
│   └── update_data.py     # Python screening logic
├── .github/workflows/
│   └── update_data.yml    # GitHub Actions automation
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── QUARTERLY_UPDATE_GUIDE.md  # Maintenance instructions
```

## 🚀 How It Works

### 1. Data Collection
- Uses `yfinance` Python library to fetch historical price data
- Calculates technical indicators (ATR, moving averages, consolidation patterns)
- Computes relative strength vs Nifty 500 index

### 2. Screening Logic
For each stock:
```python
# Calculate ADR (Average Daily Range)
adr = ((high - low) / close).rolling(20).mean() * 100

# Prior move (20-day price change)
prior_move = (close / close.shift(20) - 1) * 100

# Relative Strength vs Nifty 500
rs = (stock_return / nifty_return) * 100

# Consolidation detection
# Identifies periods where price stays within tight range
```

### 3. Grading & Filtering
- Assigns quality grades based on multiple criteria
- Picks **top 50 stocks** from each universe (500 + 250)
- Exports to JSON files for web display

### 4. Automation
- **GitHub Actions** runs the Python script daily at 6 PM IST
- Commits updated JSON files to repository
- GitHub Pages automatically publishes changes

## 📅 Maintenance

### Quarterly Index Updates
Nifty 500 and Microcap 250 constituents change quarterly. Update symbol lists in `scripts/update_data.py`:

**See detailed instructions:** [QUARTERLY_UPDATE_GUIDE.md](QUARTERLY_UPDATE_GUIDE.md)

**Quick checklist:**
1. Download latest constituent lists from NSE
2. Update `NIFTY500_SYMBOLS` and `MICROCAP250_SYMBOLS` arrays
3. Verify total = 750 stocks (500 + 250)
4. Test workflow execution
5. Commit with descriptive message

## 🛠️ Local Development

### Prerequisites
- Python 3.8+
- Git

### Setup
```bash
# Clone repository
git clone https://github.com/ab-ops-commits/qullamaggie_dashboard.git
cd qullamaggie_dashboard

# Install dependencies
pip install -r requirements.txt

# Run screening script
python scripts/update_data.py

# Open dashboard locally
# Open index.html in your browser
```

### Testing Changes
```bash
# Modify update_data.py as needed
python scripts/update_data.py

# Check generated JSON files
cat data/nifty500.json
cat data/microcap250.json

# Commit and push
git add .
git commit -m "Your changes"
git push origin main
```

## 📈 Usage Tips

### For Traders
1. **Focus on Grade A+ and A stocks** - Highest probability setups
2. **Check consolidation days** - 5-15 days ideal for breakouts
3. **Verify volume** - Ensure adequate liquidity for your position size
4. **Compare universes** - Nifty 500 for safety, Microcap 250 for aggressive plays
5. **Cross-reference with charts** - Use TradingView or your platform to confirm patterns

### Dashboard Features
- **Sort columns:** Click column headers to sort
- **Search:** Type in search box to filter stocks
- **Universe selector:** Toggle between Nifty 500 and Microcap 250
- **Mobile responsive:** Works on phones and tablets

## 🔧 Technical Details

### Dependencies
```
yfinance==0.2.28     # Yahoo Finance data fetching
pandas==2.0.3        # Data manipulation
numpy==1.24.3        # Numerical calculations
python-dateutil==2.8.2  # Date handling
```

### Data Refresh Schedule
- **Frequency:** Daily
- **Time:** 6:00 PM IST (12:30 PM UTC)
- **Trigger:** GitHub Actions cron job
- **Runtime:** ~10-15 minutes for 750 stocks

### API Rate Limits
- Yahoo Finance: Free tier, reasonable limits
- Built-in delays to avoid throttling
- Retries for failed requests

## 🤝 Contributing

This is a personal trading tool, but suggestions are welcome:

1. Open an issue to discuss changes
2. Fork the repository
3. Create a feature branch
4. Submit a pull request

## ⚠️ Disclaimer

**This tool is for educational and informational purposes only.**

- Not financial advice - do your own research
- Past performance ≠ future results
- Trading involves risk of loss
- Verify all data independently
- Screen output is not a buy/sell signal

The author is not responsible for trading decisions or losses incurred using this tool.

## 📚 Resources

### Qullamaggie Trading Methodology
- Focus on stocks with strong momentum
- Look for tight consolidations after big moves
- High relative strength vs market
- Enter on breakouts with volume confirmation

### Data Sources
- **Yahoo Finance:** Historical OHLCV data
- **NSE India:** Index constituent lists
- **Nifty Indices:** Official index data

### Related Links
- [Nifty 500 Index Info](https://www.niftyindices.com/indices/equity/broad-based-indices/nifty-500)
- [Nifty Microcap 250 Index Info](https://www.niftyindices.com/indices/equity/broad-based-indices/nifty-microcap-250)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 📧 Contact

For issues or questions:
- Open an issue in this repository
- Check [QUARTERLY_UPDATE_GUIDE.md](QUARTERLY_UPDATE_GUIDE.md) for maintenance help

## 📄 License

This project is provided as-is for personal use.

---

**Dashboard URL:** https://ab-ops-commits.github.io/qullamaggie_dashboard/

**Last Updated:** Automated daily at 6 PM IST
