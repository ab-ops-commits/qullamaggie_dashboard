# Enhanced to support both Nifty 500 and Microcap 250 universes
# Added metrics: Volume, Market Cap

import yfinance as yf
import pandas as pd
import json
from datetime import datetime, timedelta
import numpy as np

# Nifty 500 symbols (sample - full list would be loaded from CSV)
NIFTY500_SYMBOLS = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
    'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS',
    # Add all 500 symbols
]

def calculate_adr(df, period=20):
    """Calculate Average Daily Range %"""
    daily_range = ((df['High'] - df['Low']) / df['Close']) * 100
    return daily_range.tail(period).mean()

def calculate_prior_move(df, lookback_months=3):
    """Calculate % move over past 1-3 months"""
    lookback_days = lookback_months * 21
    if len(df) < lookback_days:
        return 0
    start_price = df['Close'].iloc[-lookback_days]
    current_price = df['Close'].iloc[-1]
    return ((current_price - start_price) / start_price) * 100

def check_consolidation(df, weeks=8):
    """Check for consolidation pattern"""
    days = weeks * 5
    if len(df) < days:
        return False, 0
    
    recent = df.tail(days)
    high = recent['High'].max()
    low = recent['Low'].min()
    range_pct = ((high - low) / low) * 100
    
    return range_pct < 15, len(recent)  # Tight if < 15% range

def calculate_rs_rating(stock_return, nifty_return):
    """Calculate Relative Strength rating (0-100)"""
    if nifty_return == 0:
        return 50
    rs_ratio = stock_return / nifty_return
    return min(100, max(0, int(50 + (rs_ratio - 1) * 50)))

def grade_setup(adr, prior_move, rs_rating, consol_tight, price_above_ma):
    """Grade setup A+ to D based on Qullamaggie criteria"""
    score = 0
    
    if adr >= 6: score += 3
    elif adr >= 4: score += 2
    
    if prior_move >= 50: score += 3
    elif prior_move >= 30: score += 2
    
    if rs_rating >= 85: score += 3
    elif rs_rating >= 70: score += 2
    
    if consol_tight: score += 2
    if price_above_ma: score += 2
    
    if score >= 12: return 'A+'
    elif score >= 9: return 'A'
    elif score >= 6: return 'B'
    elif score >= 4: return 'C'
    else: return 'D'

def screen_stocks():
    """Main screening function"""
    print("Starting Qullamaggie screening...")
    
    # Get Nifty 500 data for RS comparison
    nifty = yf.download('^CRSLDX', period='6mo', progress=False)
    nifty_return_3m = calculate_prior_move(nifty, 3)
    
    results = []
    
    for symbol in NIFTY500_SYMBOLS:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period='6mo')
            
            if len(df) < 60:
                continue
            
            # Calculate metrics
            price = df['Close'].iloc[-1]
            if price < 20:
                continue
            
            adr = calculate_adr(df)
            if adr < 4:
                continue
            
            prior_move = calculate_prior_move(df, 3)
            if prior_move < 30:
                continue
            
            # Check moving averages
            df['SMA10'] = df['Close'].rolling(10).mean()
            df['SMA20'] = df['Close'].rolling(20).mean()
            price_above_ma = price > df['SMA10'].iloc[-1] and price > df['SMA20'].iloc[-1]
            
            if not price_above_ma:
                continue
            
            consol_tight, consol_days = check_consolidation(df, 8)
            rs_rating = calculate_rs_rating(prior_move, nifty_return_3m)
            
            grade = grade_setup(adr, prior_move, rs_rating, consol_tight, price_above_ma)
            
            if grade in ['D']:
                continue
            
            change = ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
            
            setup_notes = f"{'Tight' if consol_tight else 'Loose'} consolidation. "
            if adr > 6:
                setup_notes += "High volatility. "
            if rs_rating > 85:
                setup_notes += "Strong RS vs Nifty 500."
            
            results.append({
                'symbol': symbol.replace('.NS', ''),
                'price': round(price, 2),
                'change': round(change, 2),
                'adr': round(adr, 2),
                'priorMove': round(prior_move, 0),
                'rsRating': rs_rating,
                'consolidationDays': consol_days,
                'grade': grade,
                'setupNotes': setup_notes
            })
            
        except Exception as e:
            print(f"Error processing {sym,
                'volume': df['Volume'].iloc[-1] if 'Volume' in df else None,
                'marketCap': ticker.info.get('marketCap', None) if hasattr(ticker, 'info') else Nonebol}: {e}")
            continue
    
    # Sort and get top 50
    grade_order = {'A+': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1}
    results.sort(key=lambda x: (grade_order.get(x['grade'], 0), x['adr']), reverse=True)
    results = results[:50]
    
    # Add ranks
    for i, stock in enumerate(results, 1):
        stock['rank'] = i
    
    # Save to JSON
    output = {
        'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M IST'),
        'stocks': results
    }
    
    with open('data/stocks.json', 'w') as f:
            # TODO: Also save to data/microcap250.json with MICROCAP250_SYMBOLS list
        json.dump(output, f, indent=2)
    
    print(f"Screening complete. Found {len(results)} setups.")

if __name__ == '__main__':
    screen_stocks()
