# Qullamaggie Screener for Nifty 500 & Microcap 250
# Enhanced with Volume and Market Cap metrics
import yfinance as yf
import pandas as pd
import json
from datetime import datetime
import numpy as np

# Complete Nifty 500 symbols (all 500 stocks from NSE)
NIFTY500_SYMBOLS = [
    '360ONE.NS', 'ABB.NS', 'ACC.NS', 'ACMESOLAR.NS', 'AIAENG.NS', 'APLAPOLLO.NS', 'AUBANK.NS', 'AWL.NS', 'AADHARHFC.NS', 'AARTIIND.NS', 'AAVAS.NS', 'ABBOTINDIA.NS', 'ACE.NS', 'ACUTAAS.NS', 'ADANIENSOL.NS', 'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ATGL.NS', 'ABCAPITAL.NS', 'ABREL.NS', 'ABSLAMC.NS', 'CPPLUS.NS', 'AEGISLOG.NS', 'AEGISVOPAK.NS', 'AETHER.NS', 'AFCONS.NS', 'AFFLE.NS', 'AJANTPHARM.NS', 'ALKEM.NS', 'ABDL.NS', 'ARE&M.NS', 'AMBER.NS', 'AMBUJACEM.NS', 'ANANDRATHI.NS', 'ANANTRAJ.NS', 'ANGELONE.NS', 'ANTHEM.NS', 'ANURAS.NS', 'APARINDS.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'APTUS.NS', 'ASAHIINDIA.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTERDM.NS', 'ASTRAL.NS', 'ATHERENERG.NS', 'ATUL.NS', 'AUROPHARMA.NS', 'AIIL.NS', 'AVANTIFEED.NS', 'DMART.NS', 'AXISBANK.NS', 'AZAD.NS', 'BEML.NS', 'BLS.NS', 'BSE.NS', 'BAGMANE.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BAJAJHLDNG.NS', 'BAJAJHFL.NS', 'BALKRISIND.NS', 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BANKINDIA.NS', 'MAHABANK.NS', 'BATAINDIA.NS', 'BELRISE.NS', 'BERGEPAINT.NS', 'BHARATCOAL.NS', 'BDL.NS', 'BEL.NS', 'BHARATFORG.NS', 'BHEL.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BHARTIHEXA.NS', 'GROWW.NS', 'BIOCON.NS', 'BSOFT.NS', 'BBOX.NS', 'BLUESTARCO.NS', 'BOSCHLTD.NS', 'FIRSTCRY.NS', 'BRIGADE.NS', 'BRITANNIA.NS', 'BIRET.NS', 'CCL.NS', 'CESC.NS', 'CGPOWER.NS', 'CIEINDIA.NS', 'CRISIL.NS', 'CANFINHOME.NS', 'CANBK.NS', 'CANHLIFE.NS', 'CAPLIPOINT.NS', 'CGCL.NS', 'CARBORUNIV.NS', 'CARTRADE.NS', 'CASTROLIND.NS', 'CEATLTD.NS', 'CEMPRO.NS', 'CENTRALBK.NS', 'CDSL.NS', 'CMPDI.NS', 'CHAMBLFERT.NS', 'CHENNPETRO.NS', 'CHOICEIN.NS', 'CHOLAHLDNG.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'CUB.NS', 'CLEANMAX.NS', 'CLEAN.NS', 'COALINDIA.NS', 'COCHINSHIP.NS', 'COFORGE.NS', 'COHANCE.NS', 'COLPAL.NS', 'CAMS.NS', 'CONCORDBIO.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CRAFTSMAN.NS', 'CREDITACC.NS', 'CROMPTON.NS', 'CUMMINSIND.NS', 'CUPID.NS', 'CYIENT.NS', 'DLF.NS', 'DOMS.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DATAPATTNS.NS', 'DEEPAKFERT.NS', 'DEEPAKNTR.NS', 'DELHIVERY.NS', 'DEVYANI.NS', 'DIVISLAB.NS', 'DIXON.NS', 'LALPATHLAB.NS', 'DRREDDY.NS', 'DUMMYHEG.NS', 'EIDPARRY.NS', 'EIHOTEL.NS', 'EMBASSY.NS', 'EICHERMOT.NS', 'ELECON.NS', 'ELGIEQUIP.NS', 'EMAMILTD.NS', 'EMCURE.NS', 'EMMVEE.NS', 'ENDURANCE.NS', 'ENGINERSIN.NS', 'ESCORTS.NS', 'ETERNAL.NS', 'EXIDEIND.NS', 'NYKAA.NS', 'FEDERALBNK.NS', 'FACT.NS', 'FINCABLES.NS', 'FSL.NS', 'FIVESTAR.NS', 'FORCEMOT.NS', 'FORTIS.NS', 'FRACTAL.NS', 'GAIL.NS', 'GVT&D.NS', 'GMRAIRPORT.NS', 'GABRIEL.NS', 'GALLANTT.NS', 'GRSE.NS', 'GICRE.NS', 'GILLETTE.NS', 'GLAND.NS', 'GLAXO.NS', 'GLENMARK.NS', 'MEDANTA.NS', 'GPIL.NS', 'GODFRYPHLP.NS', 'GODREJCP.NS', 'GODREJIND.NS', 'GODREJPROP.NS', 'GRANULES.NS', 'GRAPHITE.NS', 'GRASIM.NS', 'GRAVITA.NS', 'GESHIP.NS', 'FLUOROCHEM.NS', 'GMDCLTD.NS', 'HBLENGINE.NS', 'HCLTECH.NS', 'HDBFS.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEGAM.NS', 'HFCL.NS', 'HAVELLS.NS', 'HEROMOTOCO.NS', 'HEXT.NS', 'HSCL.NS', 'HINDALCO.NS', 'HAL.NS', 'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'HINDZINC.NS', 'POWERINDIA.NS', 'HOMEFIRST.NS', 'HONASA.NS', 'HONAUT.NS', 'HUDCO.NS', 'HYUNDAI.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIAMC.NS', 'ICICIPRULI.NS', 'IDBI.NS', 'IDFCFIRSTB.NS', 'IFCI.NS', 'IIFL.NS', 'INOXINDIA.NS', 'IRB.NS', 'IRCON.NS', 'ITCHOTELS.NS', 'ITC.NS', 'ITI.NS', 'INDIACEM.NS', 'INDIAMART.NS', 'INDIANB.NS', 'IEX.NS', 'INDHOTEL.NS', 'IOC.NS', 'IOB.NS', 'IRCTC.NS', 'IRFC.NS', 'IREDA.NS', 'IGL.NS', 'INDUSTOWER.NS', 'INDUSINDBK.NS', 'NAUKRI.NS', 'INFY.NS', 'INOXWIND.NS', 'INTELLECT.NS', 'INDIGO.NS', 'IGIL.NS', 'IKS.NS', 'IPCALAB.NS', 'JKCEMENT.NS', 'JBMA.NS', 'JKTYRE.NS', 'JMFINANCIL.NS', 'JSWCEMENT.NS', 'JSWENERGY.NS', 'JSWINFRA.NS', 'JSWSTEEL.NS', 'JAINREC.NS', 'JPPOWER.NS', 'J&KBANK.NS', 'JINDALSAW.NS', 'JSL.NS', 'JINDALSTEL.NS', 'JIOFIN.NS', 'JUBLFOOD.NS', 'JUBLINGREA.NS', 'JWL.NS', 'JYOTICNC.NS', 'KPRMILL.NS', 'KEI.NS', 'KPITTECH.NS', 'KSB.NS', 'KAJARIACER.NS', 'KPIL.NS', 'KALYANKJIL.NS', 'KARURVYSYA.NS', 'KAYNES.NS', 'KEC.NS', 'KFINTECH.NS', 'KIRLOSBROS.NS', 'KIRLOSENG.NS', 'KOTAKBANK.NS', 'KIMS.NS', 'LTF.NS', 'LTTS.NS', 'LGEINDIA.NS', 'LICHSGFIN.NS', 'LTFOODS.NS', 'LTM.NS', 'LT.NS', 'LAURUSLABS.NS', 'LEMONTREE.NS', 'LENSKART.NS', 'LICI.NS', 'LINDEINDIA.NS', 'LLOYDSME.NS', 'LODHA.NS', 'LUPIN.NS', 'MMTC.NS', 'MRF.NS', 'MTARTECH.NS', 'MGL.NS', 'M&MFIN.NS', 'M&M.NS', 'MANAPPURAM.NS', 'MRPL.NS', 'MANKIND.NS', 'MARICO.NS', 'MARUTI.NS', 'MFSL.NS', 'MAXHEALTH.NS', 'MAZDOCK.NS', 'MEESHO.NS', 'MINDACORP.NS', 'MSUMI.NS', 'MOTILALOFS.NS', 'MPHASIS.NS', 'MCX.NS', 'MUTHOOTFIN.NS', 'NATCOPHARM.NS', 'NBCC.NS', 'NCC.NS', 'NHPC.NS', 'NLCINDIA.NS', 'NMDC.NS', 'NSLNISP.NS', 'NTPCGREEN.NS', 'NTPC.NS', 'NH.NS', 'NATIONALUM.NS', 'NAVA.NS', 'NAVINFLUOR.NS', 'NESTLEIND.NS', 'NETWEB.NS', 'NEULANDLAB.NS', 'NAM-INDIA.NS', 'NUVAMA.NS', 'NUVOCO.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 'OIL.NS', 'OLAELEC.NS', 'OLECTRA.NS', 'PAYTM.NS', 'ONESOURCE.NS', 'OFSS.NS', 'POLICYBZR.NS', 'PCBL.NS', 'PGEL.NS', 'PIIND.NS', 'PNBHOUSING.NS', 'PTCIL.NS', 'PVRINOX.NS', 'PAGEIND.NS', 'PARADEEP.NS', 'PATANJALI.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PHOENIXLTD.NS', 'PWL.NS', 'PIDILITIND.NS', 'PINELABS.NS', 'PIRAMALFIN.NS', 'PPLPHARMA.NS', 'POLYMED.NS', 'POLYCAB.NS', 'POONAWALLA.NS', 'PFC.NS', 'POWERGRID.NS', 'PREMIERENE.NS', 'PRESTIGE.NS', 'PFOCUS.NS', 'PRIVISCL.NS', 'PNB.NS', 'RRKABEL.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RHIM.NS', 'RITES.NS', 'RADICO.NS', 'RVNL.NS', 'RAILTEL.NS', 'RAINBOW.NS', 'RKFORGE.NS', 'REDINGTON.NS', 'RELIANCE.NS', 'RPOWER.NS', 'RUBICON.NS', 'SBICARD.NS', 'SBILIFE.NS', 'SJVN.NS', 'SHRIPISTON.NS', 'SRF.NS', 'SAGILITY.NS', 'SAILIFE.NS', 'SAMMAANCAP.NS', 'MOTHERSON.NS', 'SANSERA.NS', 'SARDAEN.NS', 'SCHAEFFLER.NS', 'SCHNEIDER.NS', 'SCI.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SHYAMMETL.NS', 'ENRIN.NS', 'SIEMENS.NS', 'SIGNATURE.NS', 'SOBHA.NS', 'SOLARINDS.NS', 'SONACOMS.NS', 'STARHEALTH.NS', 'SBIN.NS', 'SAIL.NS', 'STLTECH.NS', 'SUMICHEM.NS', 'SUNPHARMA.NS', 'SUNTV.NS', 'SUNDARMFIN.NS', 'SUPREMEIND.NS', 'SUZLON.NS', 'SWANCORP.NS', 'SWIGGY.NS', 'SYNGENE.NS', 'SYRMA.NS', 'TBOTEK.NS', 'TDPOWERSYS.NS', 'TVSMOTOR.NS', 'TATACAP.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TCS.NS', 'TATACONSUM.NS', 'TATAELXSI.NS', 'TATAINVEST.NS', 'TMCV.NS', 'TMPV.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TATATECH.NS', 'TTML.NS', 'TECHM.NS', 'TECHNOE.NS', 'TEGA.NS', 'TEJASNET.NS', 'TENNIND.NS', 'THANGAMAYL.NS', 'NIACL.NS', 'RAMCOCEM.NS', 'THERMAX.NS', 'TIMKEN.NS', 'TITAGARH.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TORNTPOWER.NS', 'TARIL.NS', 'TRENT.NS', 'TRIDENT.NS', 'TRITURBINE.NS', 'TIINDIA.NS', 'UCOBANK.NS', 'UNOMINDA.NS', 'UPL.NS', 'UTIAMC.NS', 'ULTRACEMCO.NS', 'UNIONBANK.NS', 'UBL.NS', 'UNITDSPR.NS', 'URBANCO.NS', 'USHAMART.NS', 'VTL.NS', 'VBL.NS', 'VAML.NS', 'VISL.NS', 'VEDL.NS', 'VOGL.NS', 'VEDPOWER.NS', 'VIJAYA.NS', 'VMM.NS', 'IDEA.NS', 'VOLTAS.NS', 'WAAREEENER.NS', 'WELCORP.NS', 'WELSPUNLIV.NS', 'WHIRLPOOL.NS', 'WIPRO.NS', 'WOCKPHARMA.NS', 'YESBANK.NS', 'ZFCVINDIA.NS', 'ZEEL.NS', 'ZENTEC.NS', 'ZENSARTECH.NS', 'ZYDUSLIFE.NS', 'ZYDUSWELL.NS', 'ECLERX.NS'
]

# Nifty Microcap 250 symbols (Complete list - All 250 stocks from NSE)
MICROCAP250_SYMBOLS = [
    'AXISCADES.NS', 'AARTIPHARM.NS', 'ABFRL.NS', 'ABLBL.NS', 'AVL.NS', 'ADVENZYMES.NS', 'AEQUS.NS', 'AEROFLEX.NS', 'AKUMS.NS', 'ALKYLAMINE.NS', 'AMAGI.NS', 'APOLLO.NS', 'ACI.NS', 'ARVINDFASN.NS', 'ARVIND.NS', 'ASHAPURMIN.NS', 'ASHOKA.NS', 'ASTRAMICRO.NS', 'ATLANTAELE.NS', 'AURIONPRO.NS', 'AVALON.NS', 'CCAVENUE.NS', 'BAJAJCON.NS', 'BALAMINES.NS', 'BALUFORGE.NS', 'BANCOINDIA.NS', 'BIRLACORPN.NS', 'BLACKBUCK.NS', 'BLUEJET.NS', 'BLUESTONE.NS', 'BORORENEW.NS', 'MAPMYINDIA.NS', 'CMRGREEN.NS', 'CMSINFO.NS', 'CSBBANK.NS', 'CAMPUS.NS', 'CRAMC.NS', 'CAPILLARY.NS', 'CEIGALL.NS', 'CELLO.NS', 'CENTUM.NS', 'CERA.NS', 'CHALET.NS', 'DCBBANK.NS', 'DATAMATICS.NS', 'DIACABS.NS', 'DBL.NS', 'DUMMYINGL1.NS', 'DUMMYINGL2.NS', 'DUMMYINXGN.NS', 'DYNAMATECH.NS', 'E2E.NS', 'EPL.NS', 'EDELWEISS.NS', 'EMIL.NS', 'ELECTCAST.NS', 'ELLEN.NS', 'EMBDL.NS', 'ENTERO.NS', 'EIEL.NS', 'EQUITASBNK.NS', 'ERIS.NS', 'FEDFINA.NS', 'FIEMIND.NS', 'FINPIPE.NS', 'UTLSOLAR.NS', 'GMRP&UI.NS', 'EBGNG.NS', 'GRWRHITECH.NS', 'GENUSPOWER.NS', 'GODREJAGRO.NS', 'GOKEX.NS', 'GOKULAGRO.NS', 'GOLDIAM.NS', 'GREAVESCOT.NS', 'GRINDWELL.NS', 'GUJALKALI.NS', 'GAEL.NS', 'GNFC.NS', 'GPPL.NS', 'GSFC.NS', 'HGINFRA.NS', 'HAPPSTMNDS.NS', 'HAPPYFORGE.NS', 'HCG.NS', 'HERITGFOOD.NS', 'HCC.NS', 'IFBIND.NS', 'IIFLCAPS.NS', 'INDGN.NS', 'INDIAGLYCO.NS', 'IMFA.NS', 'INDIGOPNTS.NS', 'ICIL.NS', 'IONEXCHANG.NS', 'JAIBALAJI.NS', 'JKPAPER.NS', 'JAMNAAUTO.NS', 'JSFB.NS', 'JAYNECOIND.NS', 'JSLL.NS', 'JUBLPHARMA.NS', 'JUSTDIAL.NS', 'JYOTHYLAB.NS', 'KNRCON.NS', 'KPIGREEN.NS', 'KRBL.NS', 'KRN.NS', 'KANSAINER.NS', 'KTKBANK.NS', 'KSCL.NS', 'KIRLPNU.NS', 'KITEX.NS', 'KMEW.NS', 'KWIL.NS', 'LATENTVIEW.NS', 'LXCHEM.NS', 'IXIGO.NS', 'THELEELA.NS', 'LLOYDSENGG.NS', 'LLOYDSENT.NS', 'LUMAXTECH.NS', 'LUMAXIND.NS', 'MOIL.NS', 'MSTCLTD.NS', 'MBAPL.NS', 'MANORAMA.NS', 'MARKSANS.NS', 'MASTEK.NS', 'MEDPLUS.NS', 'METROPOLIS.NS', 'MIDHANI.NS', 'BECTORFOOD.NS', 'NEOGEN.NS', 'NFL.NS', 'NAZARA.NS', 'NEPHROPLUS.NS', 'NETWORK18.NS', 'NEWGEN.NS', 'NIVABUPA.NS', 'NORTHARC.NS', 'OMNI.NS', 'KISSHT.NS', 'OSWALPUMPS.NS', 'PNGJL.NS', 'PCJEWELLER.NS', 'PDSL.NS', 'PNCINFRA.NS', 'PTC.NS', 'PAISALO.NS', 'PARAS.NS', 'PARKHOSPS.NS', 'PGIL.NS', 'PICCADIL.NS', 'POWERMECH.NS', 'POWERICA.NS', 'PRAJIND.NS', 'PRECWIRE.NS', 'PRICOLLTD.NS', 'PGHL.NS', 'PURVA.NS', 'QPOWER.NS', 'QUESS.NS', 'RAIN.NS', 'RALLIS.NS', 'RCF.NS', 'RATEGAIN.NS', 'RATNAMANI.NS', 'RTNPOWER.NS', 'RAYMONDLSL.NS', 'REFEX.NS', 'RELAXO.NS', 'RELIGARE.NS', 'RESPONIND.NS', 'RBA.NS', 'ROUTE.NS', 'SJS.NS', 'SBFC.NS', 'SEDEMAC.NS', 'SGMART.NS', 'SIGMAADV.NS', 'SKYGOLD.NS', 'SMLMAH.NS', 'LOTUSDEV.NS', 'SAFARI.NS', 'SAMHI.NS', 'SANDUMA.NS', 'SAPPHIRE.NS', 'SAREGAMA.NS', 'SENCO.NS', 'SENORES.NS', 'SHADOWFAX.NS', 'SHAILY.NS', 'SHAKTIPUMP.NS', 'SHARDACROP.NS', 'SHAREINDIA.NS', 'SFL.NS', 'SHILCTECH.NS', 'SHILPAMED.NS', 'RENUKA.NS', 'SHREEJISPG.NS', 'SKIPPER.NS', 'SONATSOFTW.NS', 'SOUTHBANK.NS', 'SWSOLAR.NS', 'STAR.NS', 'STYLAMIND.NS', 'SUBROS.NS', 'SUDARSCHEM.NS', 'SUDEEPPHRM.NS', 'SPARC.NS', 'SUNDRMFAST.NS', 'SUNFLAG.NS', 'SUNTECK.NS', 'SPLPETRO.NS', 'SUPRIYA.NS', 'SURYAROSNI.NS', 'SUVEN.NS', 'TARC.NS', 'TTKPRESTIG.NS', 'TVSSCS.NS', 'TMB.NS', 'TANLA.NS', 'TEXRAIL.NS', 'THOMASCOOK.NS', 'THYROCARE.NS', 'TI.NS', 'TIMETECHNO.NS', 'TIMEX.NS', 'TIPSMUSIC.NS', 'TRANSRAILL.NS', 'TRIVENIPT.NS', 'UJJIVANSFB.NS', 'UNIMECH.NS', 'VGUARD.NS', 'VMART.NS', 'VIPIND.NS', 'V2RETAIL.NS', 'DBREALTY.NS', 'WABAG.NS', 'VAIBHAVGBL.NS', 'MANYAVAR.NS', 'VESUVIUS.NS', 'VIKRAMSOLR.NS', 'VIYASH.NS', 'VOLTAMP.NS', 'WAAREERTL.NS', 'WAKEFIT.NS', 'WEWORK.NS', 'WEBELSOLAR.NS', 'WELENT.NS', 'WESTLIFE.NS', 'YATHARTH.NS', 'ZAGGLE.NS'
]

def calculate_adr(df, period=20):
    daily_range = ((df['High'] - df['Low']) / df['Close']) * 100
    return daily_range.tail(period).mean()

def calculate_prior_move(df, lookback_months=3):
    lookback_days = lookback_months * 21
    if len(df) < lookback_days:
        return 0
    start_price = float(df['Close'].iloc[-lookback_days])
    current_price = float(df['Close'].iloc[-1])
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
    # ADR scoring
    if adr >= 6:
        score += 3
    elif adr >= 4:
        score += 2
    elif adr >= 3:      # NEW: lower tier for relaxed threshold
        score += 1
    # Prior move scoring
    if prior_move >= 50:
        score += 3
    elif prior_move >= 30:
        score += 2
    elif prior_move >= 20:  # NEW: lower tier for relaxed threshold
        score += 1
    # RS Rating scoring
    if rs_rating >= 85:
        score += 3
    elif rs_rating >= 70:
        score += 2
    # Consolidation
    if consol_tight:
        score += 2
    # MA trend
    if price_above_ma:
        score += 2
    if score >= 12:
        return 'A+'
    elif score >= 9:
        return 'A'
    elif score >= 6:
        return 'B'
    elif score >= 4:
        return 'C'
    else:
        return 'D'

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
            price = float(df['Close'].iloc[-1])
            if price < 20:
                continue
            adr = calculate_adr(df)
            if adr < 3:             # CHANGED: was 4
                continue
            prior_move = calculate_prior_move(df, 3)
            if prior_move < 20:     # CHANGED: was 30
                continue
            df['SMA10'] = df['Close'].rolling(10).mean()
            df['SMA20'] = df['Close'].rolling(20).mean()
            price_above_ma = float(price) > float(df['SMA10'].iloc[-1]) and float(price) > float(df['SMA20'].iloc[-1])
            if not price_above_ma:
                continue
            consol_tight, consol_days = check_consolidation(df, 8)
            rs_rating = calculate_rs_rating(prior_move, index_return)
            grade = grade_setup(adr, prior_move, rs_rating, consol_tight, price_above_ma)
            if grade in ['D']:
                continue
            change = ((price - float(df['Close'].iloc[-2])) / float(df['Close'].iloc[-2])) * 100
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
    screen_stocks(NIFTY500_SYMBOLS, '^NSEI', 'data/nifty500.json')
    # Screen Microcap 250
    screen_stocks(MICROCAP250_SYMBOLS, '^NSEI', 'data/microcap250.json')
    # Also create stocks.json for backward compatibility
    screen_stocks(NIFTY500_SYMBOLS, '^NSEI', 'data/stocks.json')
