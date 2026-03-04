# Quarterly Index Constituents Update Guide

This guide provides instructions for updating the Nifty 500 and Nifty Microcap 250 stock symbols quarterly to reflect changes in index constituents.

## Update Schedule

**Frequency:** Quarterly (Every 3 months)

**Timing:** Within 1 week after NSE publishes updated index constituent lists

**Typical Update Months:** January, April, July, October

## Step-by-Step Update Process

### 1. Download Latest Index Constituent Lists

**Nifty 500:**
- Visit: https://www.niftyindices.com/IndexConstituent/ind_nifty500list.csv
- Or go to NSE India website → Indices → Nifty 500 → Download Constituent List

**Nifty Microcap 250:**
- Visit: https://www.niftyindices.com/IndexConstituent/ind_niftymicrocap250list.csv
- Or go to NSE India website → Indices → Nifty Microcap 250 → Download Constituent List

### 2. Convert Company Names to Yahoo Finance Symbols

NSE lists provide company names. You need to convert them to Yahoo Finance ticker format:

**Format:** `SYMBOL.NS` (e.g., RELIANCE.NS, TCS.NS, INFY.NS)

**Tools to help:**
- Use the existing symbol lists as reference for formatting
- Cross-check on Yahoo Finance: https://finance.yahoo.com/
- For stocks listed on NSE, append `.NS` to the trading symbol

### 3. Update scripts/update_data.py

Navigate to: https://github.com/ab-ops-commits/qullamaggie_dashboard/blob/main/scripts/update_data.py

**Line 10-60:** Update `NIFTY500_SYMBOLS` list
```python
NIFTY500_SYMBOLS = [
    'SYMBOL1.NS',
    'SYMBOL2.NS',
    # ... add all 500 symbols
]
```

**Line 62-112:** Update `MICROCAP250_SYMBOLS` list
```python
MICROCAP250_SYMBOLS = [
    'SYMBOL1.NS',
    'SYMBOL2.NS',
    # ... add all 250 symbols
]
```

### 4. Verify Symbol Changes

Compare the new lists with existing ones to identify:
- **Additions:** New stocks added to the index
- **Deletions:** Stocks removed from the index
- **No changes:** Stocks that remain in the index

### 5. Commit Changes

**Commit Message Format:**
```
Quarterly update: Index constituents for Q[X] [YEAR]

Nifty 500:
- Added: [X] stocks
- Removed: [Y] stocks

Microcap 250:
- Added: [A] stocks  
- Removed: [B] stocks
```

### 6. Test the Update

After committing:
1. Go to Actions tab: https://github.com/ab-ops-commits/qullamaggie_dashboard/actions
2. Click "Update Stock Data" workflow
3. Click "Run workflow" → Select "main" branch → Run
4. Monitor the workflow execution for errors
5. Check if data files are updated: `data/nifty500.json` and `data/microcap250.json`
6. Visit dashboard: https://ab-ops-commits.github.io/qullamaggie_dashboard/
7. Verify both universes load correctly with new stock counts

### 7. Handle Errors

**Common Issues:**

**Invalid Symbol Format:**
- Error: `No data found for symbol`  
- Solution: Verify Yahoo Finance ticker format (should be SYMBOL.NS)
- Cross-check on https://finance.yahoo.com/quote/SYMBOL.NS

**Delisted/Suspended Stocks:**
- Error: Data fetch failures for specific symbols
- Solution: Remove delisted stocks from the list
- Check NSE announcements for corporate actions

**API Rate Limits:**
- Error: Too many requests
- Solution: The script has built-in delays; if issue persists, split the update into batches

## Data Validation Checklist

After each quarterly update, verify:

- [ ] Total symbol count = 750 (500 + 250)
- [ ] Nifty 500 list has exactly 500 symbols
- [ ] Microcap 250 list has exactly 250 symbols  
- [ ] All symbols follow `.NS` format
- [ ] No duplicate symbols within or across lists
- [ ] Dashboard loads without errors
- [ ] Stock data displays correctly for both universes
- [ ] Date stamp shows today's date
- [ ] All metrics populate (ADR%, Prior Move, RS, etc.)

## Reference Links

**Official Index Pages:**
- Nifty 500: https://www.niftyindices.com/indices/equity/broad-based-indices/nifty-500
- Nifty Microcap 250: https://www.niftyindices.com/indices/equity/broad-based-indices/nifty-microcap-250

**Data Sources:**
- NSE India: https://www.nseindia.com/
- Nifty Indices: https://www.niftyindices.com/
- Yahoo Finance: https://finance.yahoo.com/

## Notes

- Index rebalancing typically occurs quarterly but check NSE announcements for exact dates
- Some quarters may have minimal changes
- Keep a log of changes for audit trail
- The daily workflow (6 PM IST) will automatically use updated symbol lists
- No need to modify GitHub Actions workflow file for symbol updates

## Quick Update Command Reference

```bash
# If running locally for testing:
git clone https://github.com/ab-ops-commits/qullamaggie_dashboard.git
cd qullamaggie_dashboard
pip install -r requirements.txt
python scripts/update_data.py
```

## Contact

For issues or questions about the update process, create an issue in the repository:
https://github.com/ab-ops-commits/qullamaggie_dashboard/issues
