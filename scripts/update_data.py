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

# Nifty Microcap 250 symbols (Complete list - All 250 stocks from NSE)MICROCAP250_SYMBOLS = [
        'AGI.NS', 'ASKAUTOLTD.NS', 'AARTIDRUGS.NS', 'AARTIPHARM.NS', 'ACUTAAS.NS',
    'ADVENZYMES.NS', 'AETHER.NS', 'AHLUCONT.NS', 'AJAXENGG.NS', 'ALIVUS.NS',
    'ALLCARGO.NS', 'ABDL.NS', 'ANURAS.NS', 'PARKHOTELS.NS', 'ACI.NS',
    'ARVINDFASN.NS', 'ARVIND.NS', 'ASHOKA.NS', 'ASTRAMICRO.NS', 'AURIONPRO.NS',
    'AVALON.NS', 'AVANTIFEED.NS', 'CCAVENUE.NS', 'AWFIS.NS', 'AZAD.NS',
    'BAJAJELEC.NS', 'BALAMINES.NS', 'BALUFORGE.NS', 'BANCOINDIA.NS', 'BELRISE.NS',
    'BBL.NS', 'BIRLACORPN.NS', 'BLACKBUCK.NS', 'BORORENEW.NS', 'BOSCH-HCI.NS',
    'CIEINDIA.NS', 'CMSINFO.NS', 'CSBBANK.NS', 'CARTRADE.NS', 'CEIGALL.NS',
    'CELLO.NS', 'CEMPRO.NS', 'CIGNITIITEC.NS', 'CYIENTDLM.NS', 'DCBBANK.NS',
    'DATAMATICS.NS', 'DHANUKA.NS', 'DIACABS.NS', 'DBL.NS', 'DCAL.NS',
    'DODLA.NS', 'DUMMYALCARE.NS', 'DYNAMATECH.NS', 'EPL.NS', 'EASEMYTRIP.NS',
    'EDELWEISS.NS', 'EMIL.NS', 'ELECTCAST.NS', 'EMBDLB.NS', 'ENTERO.NS',
    'EIEL.NS', 'EPIGRAL.NS', 'EQUITASBNK.NS', 'ETHOSLTD.NS', 'EUREKAFORB.NS',
    'FDC.NS', 'FIEMIND.NS', 'FINEORG.NS', 'GRINFRA.NS', 'GHCL.NS',
    'GMMPFAUDLR.NS', 'GMRPUI.NS', 'GABRIEL.NS', 'GALLANTT.NS', 'GANESHOU.NS',
    'GANECOS.NS', 'GRWRHITECH.NS', 'GARFIBRES.NS', 'GATEWAY.NS', 'GOKEX.NS',
    'GREAVESCOT.NS', 'GREENPANEL.NS', 'GAEL.NS', 'GNFC.NS', 'GPPL.NS',
    'GSFC.NS', 'GULFOILLUB.NS', 'HGINFRA.NS', 'HCG.NS', 'HEMIPROP.NS',
    'HERITGFOOD.NS', 'HIKAL.NS', 'HCC.NS', 'IFBIND.NS', 'IIFLCAPS.NS',
    'IMAGICAA.NS', 'INDIAGLYO.NS', 'INDIASHLT.NS', 'IMFA.NS', 'INDIGOPNTS.NS',
    'ICIL.NS', 'INGERRAND.NS', 'INNOVACAP.NS', 'INOXGREEN.NS', 'IONEXCHANGE.NS',
    'ISGEC.NS', 'JKIL.NS', 'JKLAKSHMI.NS', 'JKPAPER.NS', 'JAIBALAJI.NS',
    'JISLJALEQS.NS', 'JAMNAAUTO.NS', 'JSFB.NS', 'JINDWORLD.NS', 'JUSTDIAL.NS',
    'KNRCON.NS', 'KPIGREEN.NS', 'KRBL.NS', 'KRN.NS', 'KSL.NS',
    'KANSAINER.NS', 'KTKBANK.NS', 'KSCL.NS', 'KIRLPNU.NS', 'KITEX.NS',
    'LMW.NS', 'LXCHEM.NS', 'IXIGO.NS', 'LLOYDSENG.NS', 'LLOYDSENT.NS',
    'LUMAXTECH.NS', 'LUXIND.NS', 'MOIL.NS', 'MSTCLTD.NS', 'MTARTECH.NS',
    'MAHLIFE.NS', 'MANINFRA.NS', 'MANORAMA.NS', 'MARKSANS.NS', 'MASTEK.NS',
    'MAXESTATES.NS', 'MEDPLUS.NS', 'MIDHANI.NS', 'BECTORFOOD.NS', 'NEOGEN.NS',
    'NESCO.NS', 'NFL.NS', 'NAZARA.NS', 'NETWORK18.NS', 'OPTIEMUS.NS',
    'ORCHPHARMA.NS', 'ORIENTCEM.NS', 'OSWALPUMPS.NS', 'PNGJL.NS', 'PCJEWELLER.NS',
    'PNCINFRA.NS', 'PTC.NS', 'PARADEEP.NS', 'PARAS.NS', 'PATELENG.NS',
    'PGIL.NS', 'POLYPLEX.NS', 'POWERMECH.NS', 'PRICOLLLTD.NS', 'PRINCEPIPE.NS',
    'PRSMJOHNSN.NS', 'PRIVISCL.NS', 'PRUDENT.NS', 'PURVA.NS', 'QUESS.NS',
    'RAIN.NS', 'RALLIS.NS', 'RATEGAIN.NS', 'RATNAMANI.NS', 'RTNINDIA.NS',
    'RTNPOWER.NS', 'RAYMONDLSL.NS', 'REFEX.NS', 'RELAXO.NS', 'RELIGARE.NS',
    'RBA.NS', 'ROUTE.NS', 'SKYGOLD.NS', 'SAFARI.NS', 'SAMHI.NS',
    'SANDUMA.NS', 'SANOFICON.NS', 'SANOFI.NS', 'SANSERA.NS', 'SENCO.NS',
    'SHAILY.NS', 'SHAKTIPUMP.NS', 'SHARDACROP.NS', 'SHARDAMOTR.NS', 'SHAREINDIA.NS',
    'SFL.NS', 'SHILPAMED.NS', 'RENUKA.NS', 'SHRIPISTON.NS', 'SKIPPER.NS',
    'SOUTHBANK.NS', 'STARCEMENT.NS', 'SWSOLAR.NS', 'STLTECH.NS', 'STAR.NS',
    'STYRENIX.NS', 'SUBROS.NS', 'SUDARSCHEM.NS', 'SPARC.NS', 'SUNFLAG.NS',
    'SUNTECK.NS', 'SUPRIYA.NS', 'SURYAROSNI.NS', 'SYMPHONY.NS', 'TARC.NS',
    'TDPOWERSYS.NS', 'TSFINV.NS', 'TVSCSB.NS', 'TANLA.NS', 'TEAMLEASE.NS',
    'TEGA.NS', 'TEXRAIL.NS', 'THANGAMAYL.NS', 'ANUP.NS', 'THOMASCOOK.NS',
    'THYROCARE.NS', 'TI.NS', 'TIMETECHNO.NS', 'TIPSMUSIC.NS', 'TRANSRAILLL.NS',
    'UJJIVANSFB.NS', 'UNIMECH.NS', 'VMART.NS', 'VIPIND.NS', 'V2RETAIL.NS',
    'VSTIND.NS', 'WABAG.NS', 'VAIBHAVGBL.NS', 'VARROC.NS', 'VESUVIUS.NS',
    'VINATIORGA.NS', 'VIYASH.NS', 'VOLTAMP.NS', 'WAARERTL.NS', 'WEBELSOLAR.NS',
    'WELENT.NS', 'WESTLIFE.NS', 'YATHARTH.NS', 'ZAGGLE.NS', 'ZYDUSWELL.NS',
    'EMUDHRA.NS'

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
