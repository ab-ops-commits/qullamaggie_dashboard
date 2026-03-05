# Qullamaggie Screener for Nifty 500 & Microcap 250
# Enhanced with Volume and Market Cap metrics

import yfinance as yf
import pandas as pd
import json
from datetime import datetime
import numpy as np

# Complete Nifty 500 symbols (all 500 stocks from NSE)
NIFTY500_SYMBOLS = [
    '360ONE.NS', '3MINDIA.NS', 'ABB.NS', 'ACC.NS', 'ACMESOLAR.NS',
    'AIAENG.NS', 'APLAPOLLO.NS', 'AUBANK.NS', 'AWL.NS', 'AADHARHFC.NS',
    'AARTIIND.NS', 'AAVAS.NS', 'ABBOTINDIA.NS', 'ACE.NS', 'ADANIENSOL.NS',
    'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ATGL.NS',
    'ABCAPITAL.NS', 'ABFRL.NS', 'ABLBL.NS', 'ABREL.NS', 'ABSLAMC.NS',
    'AEGISLOG.NS', 'AEGISVOPAK.NS', 'AFCONS.NS', 'AFFLE.NS', 'AJANTPHARM.NS',
    'AKUMS.NS', 'AKZOINDIA.NS', 'APLLTD.NS', 'ALKEM.NS', 'ALKYLAMINE.NS',
    'ALOKINDS.NS', 'AREM.NS', 'AMBER.NS', 'AMBUJACEM.NS', 'ANANDRATHI.NS',
    'ANANTRAJ.NS', 'ANGELONE.NS', 'APARINDS.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS',
    'APTUS.NS', 'ASAHIINDIA.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTERDM.NS',
    'ASTRAZEN.NS', 'ASTRAL.NS', 'ATHERENERG.NS', 'ATUL.NS', 'AUROPHARM.NS', 'AIIL.NS', 'DMART.NS',
    'AXISBANK.NS', 'BASF.NS', 'BEML.NS', 'BLS.NS', 'BSE.NS',
    'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BAJAJHLDNG.NS', 'BAJAJHFL.NS',
    'BALKRISIND.NS', 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BANKINDIA.NS',
    'MAHABANK.NS', 'BATAINDIA.NS', 'BAYERCROP.NS', 'BERGEPAINT.NS', 'BDL.NS',
    'BEL.NS', 'BHARATFORG.NS', 'BHEL.NS', 'BPCL.NS', 'BHARTIARTL.NS',
    'BHARTIHEXA.NS', 'BIKAJI.NS', 'BIOCON.NS', 'BSOFT.NS', 'BLUEDART.NS',
    'BLUEJET.NS', 'BLUESTARCO.NS', 'BBTC.NS', 'BOSCHLTD.NS', 'FIRSTCRY.NS',
    'BRIGADE.NS', 'BRITANNIA.NS', 'MAPMYINDIA.NS', 'CCL.NS', 'CESC.NS',
    'CGPOWER.NS', 'CRISIL.NS', 'CAMPUS.NS', 'CANFINHOME.NS', 'CANBK.NS',
    'CAPLIPOINT.NS', 'CGCL.NS', 'CARBORUNIV.NS', 'CASTROLIND.NS', 'CEATLTD.NS',
    'CENTRALBK.NS', 'CDSL.NS', 'CENTURYPLY.NS', 'CERA.NS', 'CHALET.NS',
    'CHAMBLFERT.NS', 'CHENNPETRO.NS', 'CHOICEIN.NS', 'CHOLAHLDNG.NS', 'CHOLAFIN.NS',
    'CIPLA.NS', 'CUB.NS', 'CLEAN.NS', 'COALINDIA.NS', 'COCHINSHIP.NS',
    'COFORGE.NS', 'COHANCE.NS', 'COLPAL.NS', 'CAMS.NS', 'CONCORDBIO.NS',
    'CONCOR.NS', 'COROMANDEL.NS', 'CRAFTSMAN.NS', 'CREDITACC.NS', 'CROMPTON.NS',
    'CUMMINSIND.NS', 'CYIENT.NS', 'DCMSHRIRAM.NS', 'DLF.NS', 'DOMS.NS',
    'DABUR.NS', 'DALBHARAT.NS', 'DATAPATTNS.NS', 'DEEPAKFERT.NS', 'DEEPAKNTR.NS',
    'DELHIVERY.NS', 'DEVYANI.NS', 'DIVISLAB.NS', 'DIXON.NS', 'AGARWALEYE.NS',
    'LALPATHLAB.NS', 'DRREDDY.NS', 'EIDPARRY.NS', 'EIHOTEL.NS', 'EICHERMOT.NS',
    'ELECON.NS', 'ELGIEQUIP.NS', 'EMAMILTD.NS', 'EMCURE.NS', 'ENDURANCE.NS',
    'ENGINEERSIN.NS', 'ERIS.NS', 'ESCORTS.NS', 'ETERNAL.NS', 'EXIDEIND.NS',
    'NYKAA.NS', 'FEDERALBNK.NS', 'FACT.NS', 'FINCABLES.NS', 'FINPIPE.NS',
    'FSL.NS', 'FIVESTAR.NS', 'FORCEMOT.NS', 'FORTIS.NS', 'GAIL.NS',
    'GVTD.NS', 'GMRAIRPORT.NS', 'GRSE.NS', 'GICRE.NS', 'GILLETTE.NS',
    'GLAND.NS', 'GLAXO.NS', 'GLENMARK.NS', 'MEDANTA.NS', 'GODIGIT.NS',
    'GPIL.NS', 'GODFRYPHLP.NS', 'GODREJAGRO.NS', 'GODREJCP.NS', 'GODREJIND.NS',
    'GODREJPROP.NS', 'GRANULES.NS', 'GRAPHITE.NS', 'GRASIM.NS', 'GRAVITA.NS',
    'GESHIP.NS', 'FLUOROCHEM.NS', 'GUJGASLTD.NS', 'GMDCLTD.NS', 'GSPL.NS',
    'HEG.NS', 'HBLENGINE.NS', 'HCLTECH.NS', 'HDFCAMC.NS', 'HDFCBANK.NS',
    'HDFCLIFE.NS', 'HFCL.NS', 'HAPPSTMNDS.NS', 'HAVELLS.NS', 'HEROMOTOCO.NS',
    'HEXT.NS', 'HSCL.NS', 'HINDALCO.NS', 'HAL.NS', 'HINDCOPPER.NS',
    'HINDPETRO.NS', 'HINDUNILVR.NS', 'HINDZINC.NS', 'POWERINDIA.NS', 'HOMEFIRST.NS',
    'HONASA.NS', 'HONAUT.NS', 'HUDCO.NS', 'HYUNDAI.NS', 'ICICIBANK.NS',
    'ICICIGI.NS', 'ICICIPRULIFE.NS', 'IDBI.NS', 'IDFCFIRSTB.NS', 'IFCI.NS',
    'IIFL.NS', 'INOXINDIA.NS', 'IRB.NS', 'IRCON.NS', 'ITCHOTELS.NS',
    'ITC.NS', 'ITI.NS', 'INDGEN.NS', 'INDIACEM.NS', 'INDIAMART.NS',
    'INDIANB.NS', 'IEX.NS', 'INDHOTEL.NS', 'IOC.NS', 'IOB.NS',
    'IRCTC.NS', 'IRFC.NS', 'IREDA.NS', 'IGL.NS', 'INDUSTOWER.NS',
    'INDUSINDBK.NS', 'NAUKRI.NS', 'INFY.NS', 'INOXWIND.NS', 'INTELLECT.NS',
    'INDIGO.NS', 'IGIL.NS', 'IKS.NS', 'IPCALAB.NS', 'JBCHEPHARM.NS',
    'JKCEMENT.NS', 'JBMA.NS', 'JKTYRE.NS', 'JMFINANCIL.NS', 'JSWCEMENT.NS',
    'JSWENERGY.NS', 'JSWINFRA.NS', 'JSWSTEEL.NS', 'JPPOWER.NS', 'JKBANK.NS',
    'JINDALSAW.NS', 'JSL.NS', 'JINDSTEL.NS', 'JIOFIN.NS', 'JUBLFOOD.NS',
    'JUBLINGREA.NS', 'JUBLPHARMA.NS', 'JWL.NS', 'JYOTHYLAB.NS', 'JYOTICNC.NS',
    'KPRMILL.NS', 'KEI.NS', 'KPITTECH.NS', 'KSB.NS', 'KAJARIACERE.NS',
    'KPIL.NS', 'KALYANKJIL.NS', 'KARURVYSYA.NS', 'KAYNES.NS', 'KEC.NS',
    'KFINTECH.NS', 'KIRLBROS.NS', 'KIRLOSENG.NS', 'KOTAKBANK.NS', 'KIMS.NS',
    'LTF.NS', 'LTTS.NS', 'LICHSGFIN.NS', 'LTFOODS.NS', 'LTM.NS',
    'LT.NS', 'LATENTVIEW.NS', 'LAURUSLABS.NS', 'THELEELA.NS', 'LEMONTREE.NS',
    'LICI.NS', 'LINDEINDIA.NS', 'LLOYDSME.NS', 'LODHA.NS', 'LUPIN.NS',
    'MMTC.NS', 'MRF.NS', 'MGL.NS', 'MAHSCOOTER.NS', 'MAHSEAMLES.NS',
    'MMFIN.NS', 'M&M.NS', 'MANAPPURAM.NS', 'MRPL.NS', 'MANKIND.NS',
    'MARICO.NS', 'MARUTI.NS', 'MFSL.NS', 'MAXHEALTH.NS', 'MAZDOCK.NS',
    'METROPOLIS.NS', 'MINDACORP.NS', 'MSUMI.NS', 'MOTILALOSWF.NS', 'MPHASIS.NS',
    'MCX.NS', 'MUTHOOTFIN.NS', 'NATCOPHARM.NS', 'NBCC.NS', 'NCC.NS',
    'NHPC.NS', 'NLCINDIA.NS', 'NMDC.NS', 'NSLNISP.NS', 'NTPCGREEN.NS',
    'NTPC.NS', 'NH.NS', 'NATIONALUM.NS', 'NAVA.NS', 'NAVINFLUOR.NS',
    'NESTLEIND.NS', 'NETWEB.NS', 'NEULANDLAB.NS', 'NEWGEN.NS', 'NAM-INDIA.NS',
    'NIVABUPA.NS', 'NUVAMA.NS', 'NUVOCO.NS', 'OBEROIRLTY.NS', 'ONGC.NS',
    'OIL.NS', 'OLAELEC.NS', 'OLECTRA.NS', 'PAYTM.NS', 'ONESOURCE.NS',
    'OFSS.NS', 'POLICYBZR.NS', 'PCBL.NS', 'PGEL.NS', 'PIIND.NS',
    'PNBHOUSING.NS', 'PTCIL.NS', 'PVRINOX.NS', 'PAGEIND.NS', 'PATANJALI.NS',
    'PERSISTENT.NS', 'PETRONET.NS', 'PFIZER.NS', 'PHOENIXLTD.NS', 'PIDILITIND.NS',
    'PPLPHARMA.NS', 'POLYMED.NS', 'POLYCAB.NS', 'POONAWALLA.NS', 'PFC.NS',
    'POWERGRID.NS', 'PRAJIND.NS', 'PREMIERENE.NS', 'PRESTIGE.NS', 'PGHH.NS',
    'PNB.NS', 'RRKABEL.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RHIM.NS',
    'RITES.NS', 'RADICO.NS', 'RVNL.NS', 'RAILTEL.NS', 'RAINBOW.NS',
    'RKFORGE.NS', 'RCF.NS', 'REDINGTON.NS', 'RELIANCE.NS', 'RELINFRABE.NS',
    'RPOWER.NS', 'SBFC.NS', 'SBICARD.NS', 'SBILIFE.NS', 'SJVN.NS',
    'SRF.NS', 'SAGILITY.NS', 'SAILIFE.NS', 'SAMMAANCAP.NS', 'MOTHERSON.NS',
    'SAPPHIRE.NS', 'SARDAENE.NS', 'SAREGAMA.NS', 'SCHAEFFLER.NS', 'SCHNEIDERB.NS',
    'SCI.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SHYAMMETL.NS', 'ENRINE.NS',
    'SIEMENS.NS', 'SIGNATURE.NS', 'SOBHA.NS', 'SOLARINDS.NS', 'SONACOMS.NS',
    'SONATSOFT.NS', 'STARHEALTH.NS', 'SBIN.NS', 'SAIL.NS', 'SUMICHEM.NS',
    'SUNPHARMA.NS', 'SUNTV.NS', 'SUNDRMFIN.NS', 'SUNDRMFAST.NS', 'SUPREMEIND.NS',
    'SUZLON.NS', 'SWANCORP.NS', 'SWIGGY.NS', 'SYNGENE.NS', 'SYRMA.NS',
    'TBOTEK.NS', 'TVSMOTOR.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TCS.NS',
    'TATACONSUM.NS', 'TATAELXSI.NS', 'TATAINVEST.NS', 'TMPV.NS', 'TATAPOWER.NS',
    'TATASTEEL.NS', 'TATATECH.NS', 'TTML.NS', 'TECHM.NS', 'TECHNOE.NS',
    'TEJASNET.NS', 'NIACL.NS', 'RAMCOCEM.NS', 'THERMAX.NS', 'TIMKEN.NS',
    'TITAGARH.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TORNTPOWER.NS', 'TARIL.NS',
    'TRENT.NS', 'TRIDENT.NS', 'TRIVENI.NS', 'TRITURBINE.NS', 'TIINDIA.NS',
    'UCOBANK.NS', 'UNOMINDA.NS', 'UPL.NS', 'UTIAMC.NS', 'ULTRACEMCO.NS',
    'UNIONBANK.NS', 'UBL.NS', 'UNITDSPR.NS', 'USHAMART.NS', 'VGUARD.NS',
    'DBREALTY.NS', 'VTL.NS', 'VBL.NS', 'MANYAVAR.NS', 'VEDL.NS',
    'VENTIVE.NS', 'VIJAYA.NS', 'VMM.NS', 'IDEA.NS', 'VOLTAS.NS',
    'WAAREEENER.NS', 'WELCORP.NS', 'WELSPUNLIV.NS', 'WHIRLPOOL.NS', 'WIPRO.NS',
    'WOCKPHARMA.NS', 'YESBANK.NS', 'ZFCVINDIA.NS', 'ZEEL.NS', 'ZENTEC.NS',
    'ZENSARTECH.NS', 'ZYDUSLIFE.NS', 'ECLERX.NS'
]

# Nifty Microcap 250 symbols (Complete list - All 250 stocks from NSE)
MICROCAP250_SYMBOLS = [
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
