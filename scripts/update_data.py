# Qullamaggie Screener for Nifty 500 & Microcap 250
# Enhanced with Volume and Market Cap metrics

import yfinance as yf
import pandas as pd
import json
from datetime import datetime
import numpy as np

# Expanded Nifty 500 symbols (top 50 + representative sample)
NIFTY500_SYMBOLS = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
    'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS',
    'LT.NS', 'HCLTECH.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS',
    'SUNPHARMA.NS', 'TITAN.NS', 'WIPRO.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS',
    'BAJFINANCE.NS', 'TECHM.NS', 'POWERGRID.NS', 'NTPC.NS', 'ONGC.NS',
    'TATAMOTORS.NS', 'COALINDIA.NS', 'M&M.NS', 'ADANIPORTS.NS', 'DIVISLAB.NS',
    'DRREDDY.NS', 'JSWSTEEL.NS', 'GRASIM.NS', 'TATACONSUM.NS', 'CIPLA.NS',
    'SBILIFE.NS', 'APOLLOHOSP.NS', 'BAJAJFINSV.NS', 'INDUSINDBK.NS', 'LTTS.NS',
    'HDFCLIFE.NS', 'ADANIENT.NS', 'HINDALCO.NS', 'TATASTEEL.NS', 'BRITANNIA.NS',
    'EICHERMOT.NS', 'PIDILITE.NS', 'TRENT.NS', 'HAVELLS.NS', 'DABUR.NS'
]

# Nifty Microcap 250 symbols (sample representatives)
MICROCAP250_SYMBOLS = [
    'NAVINFLUOR.NS', 'APLAPOLLO.NS', 'MAHSEAMLES.NS', 'SAFARI.NS', 'GRINDWELL.NS',
    'FINEORG.NS', 'MAZDOCK.NS', 'HLEGLAS.NS', 'PNCINFRA.NS', 'EASEMYTRIP.NS',
    'GPIL.NS', 'SYRMA.NS', 'MAPMYINDIA.NS', 'FUSION.NS', 'IDEAFORGE.NS',
    'KAYNES.NS', 'CLEAN.NS', 'IRCTC.NS', 'PARAS.NS', 'ROUTE.NS',
    'VERANDA.NS', 'SUZLON.NS', 'RAILTEL.NS', 'RVNL.NS', 'HBLPOWER.NS',
    'SONACOMS.NS', 'CERA.NS', 'APARINDS.NS', 'IIFL.NS', 'SHOPERSTOP.NS',
    'HUDCO.NS', 'NUVOCO.NS', 'GATEWAY.NS', 'SARDAEN.NS', 'MEDANTA.NS',
    'POLYMED.NS', 'SHYAMTEL.NS', 'KPIL.NS', 'ACE.NS', 'RAINBOW.NS',
    'YATHARTH.NS', 'NETWEB.NS', 'NSLNISP.NS', 'VIPIND.NS', 'RTNINDIA.NS',
    'ELIN.NS', 'SIGNATURE.NS', 'ANURAS.NS', 'AVANTI.NS', 'JYOTICNC.NS'
]

def calculate_adr(df, period=20):
    daily_range = ((df['High'] - df['Low']) / df['Close']) * 100
    return daily_range.tail(period).mean()

def calculate_prior_move(df, lookback_months=3):
    lookback_days = lookback_months * 21
    if len(df) < lookback_days:
        return 0
    start_price = df['Close'].iloc[-lookback_days]
    current_price = df['Close'].iloc[-1]
    return ((current_price - start_price) / start_price) * 100

def check_consolidation(df, weeks=8):
    days = weeks * 5
    if len(df) < days:
        return False, 0
    recent = df.tail(days)
    high = recent['High'].max()
    low = recent['Low'].min()
    range_pct = ((high - low) / low) * 100
    return range_pct < 15, len(recent)

def calculate_rs_rating(stock_return, index_return):
    if index_return == 0:
        return 50
    rs_ratio = stock_return / index_return
    return min(100, max(0, int(50 + (rs_ratio - 1) * 50)))

def grade_setup(adr, prior_move, rs_rating, consol_tight, price_above_ma):
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

def screen_stocks(symbols_list, index_symbol, output_file):
    print(f"Screening {len(symbols_list)} stocks...")
    
    # Get index data
    index = yf.download(index_symbol, period='6mo', progress=False)
    index_return = calculate_prior_move(index, 3)
    
    results = []
    
    for symbol in symbols_list:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period='6mo')
            
            if len(df) < 60:
                continue
            
            price = df['Close'].iloc[-1]
            if price < 20:
                continue
            
            adr = calculate_adr(df)
            if adr < 4:
                continue
            
            prior_move = calculate_prior_move(df, 3)
            if prior_move < 30:
                continue
            
            df['SMA10'] = df['Close'].rolling(10).mean()
            df['SMA20'] = df['Close'].rolling(20).mean()
            price_above_ma = price > df['SMA10'].iloc[-1] and price > df['SMA20'].iloc[-1]
            
            if not price_above_ma:
                continue
            
            consol_tight, consol_days = check_consolidation(df, 8)
            rs_rating = calculate_rs_rating(prior_move, index_return)
            grade = grade_setup(adr, prior_move, rs_rating, consol_tight, price_above_ma)
            
            if grade in ['D']:
                continue
            
            change = ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
            
            setup_notes = f"{'Tight' if consol_tight else 'Loose'} consolidation. "
            if adr > 6:
                setup_notes += "High volatility. "
            if rs_rating > 85:
                setup_notes += "Strong RS."
            
            # Get volume and market cap
            volume = df['Volume'].iloc[-1] if 'Volume' in df.columns else None
            market_cap = None
            try:
                info = ticker.info
                market_cap = info.get('marketCap', None)
            except:
                pass
            
            results.append({
                'symbol': symbol.replace('.NS', ''),
                'price': round(price, 2),
                'change': round(change, 2),
                'adr': round(adr, 2),
                'priorMove': round(prior_move, 0),
                'rsRating': rs_rating,
                'consolidationDays': consol_days,
                'grade': grade,
                'setupNotes': setup_notes,
                'volume': int(volume) if volume else None,
                'marketCap': int(market_cap) if market_cap else None
            })
            
        except Exception as e:
            print(f"Error {symbol}: {e}")
            continue
    
    grade_order = {'A+': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1}
    results.sort(key=lambda x: (grade_order.get(x['grade'], 0), x['adr']), reverse=True)
    results = results[:50]
    
    for i, stock in enumerate(results, 1):
        stock['rank'] = i
    
    output = {
        'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M IST'),
        'stocks': results
    }
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Complete. Found {len(results)} setups saved to {output_file}")

if __name__ == '__main__':
    # Screen Nifty 500
    screen_stocks(NIFTY500_SYMBOLS, '^CRSLDX', 'data/nifty500.json')
    
    # Screen Microcap 250
    screen_stocks(MICROCAP250_SYMBOLS, '^CRSLDX', 'data/microcap250.json')
    
    # Also create stocks.json for backward compatibility
    screen_stocks(NIFTY500_SYMBOLS, '^CRSLDX', 'data/stocks.json')
