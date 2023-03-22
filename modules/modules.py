import pandas as pd
import plotly.graph_objs as go
from dash import Dash

import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
from datetime import datetime

# external css static
external_stylesheets = [dbc.themes.SLATE]

# dash app with external stylesheet
app = Dash(__name__, external_stylesheets=external_stylesheets)

# all symbols to be retrieved in dashboard
stocks = {
    "A (Agilent Technologies)": "A",  "AAL (American Airlines Group)": "AAL", "AAP (Advance Auto Parts)": "AAP",
    "AAPL (Apple)": "AAPL", "ABBV (AbbVie)": "ABBV", "ABC (AmerisourceBergen)": "ABC", "ABT (Abbott Laboratories)": "ABT", 
    "ACGL (Arch Capital Group)": "ACGL", "ACN (Accenture)": "ACN", "ADBE (Adobe)": "ADBE", "ADI (Analog Devices)": "ADI", 
    "ADM (Archer Daniels Midland)": "ADM", "ADP (ADP)": "ADP", "ADSK (Autodesk)": "ADSK", "AEE (Ameren)": "AEE", 
    "AEP (American Electric Power)": "AEP", "AES (AES)": "AES", "AFL (Aflac)": "AFL", "AIG (American)": "AIG", 
    "AIZ (Assurant)": "AIZ", "AJG (Arthur J Gallagher)": "AJG", "AKAM (Akamai Technologies)": "AKAM", "ALB (Albemarle)": "ALB", 
    "ALGN (Align Technology)": "ALGN", "ALK (Alaska Air)": "ALK", "ALL (Allstate)": "ALL", "ALLE (Allegion)": "ALLE", 
    "AMAT (Applied Materials)": "AMAT", "AMCR (Amcor)": "AMCR", "AMD (AMD)": "AMD", "AME (AMETEK)": "AME", 
    "AMGN (Amgen)": "AMGN", "AMP (Ameriprise Financial)": "AMP", "AMT (American Tower)": "AMT", "AMZN (Amazon)": "AMZN", 
    "ANET (Arista Networks)": "ANET", "ANSS (ANSYS)": "ANSS", "AON (Aon)": "AON", "AOS (A O Smith)": "AOS", "APA (APA)": "APA",
    "APD (Air Products And Chemicals)": "APD", "APH (Amphenol)": "APH", "APTV (Aptiv)": "APTV", 
    "ARE (Alexandria Real Estate Equities)": "ARE", "ATO (Atmos Energy)": "ATO", "ATVI (Activision Blizzard)": "ATVI", 
    "AVB (AvalonBay Communities)": "AVB", "AVGO (Broadcom)": "AVGO", "AVY (Avery Dennison)": "AVY", 
    "AWK (American Water Works)": "AWK", "AXP (American Express)": "AXP", "AZO (AutoZone)": "AZO", "BA (Boeing)": "BA", 
    "BAC (Bank Of America)": "BAC", "BALL (Ball)": "BALL", "BAX (Baxter)": "BAX", "BBWI (Bath & Body Works)": "BBWI", 
    "BBY (Best Buy)": "BBY", "BDX (Becton Dickinson)": "BDX", "BEN (Franklin Resources)": "BEN", "BF.B (Brown-Forman)": "BF.B", 
    "BIIB (Biogen)": "BIIB", "BIO (Bio-Rad Laboratories)": "BIO", "BK (Bank Of New York Mellon)": "BK", 
    "BKNG (Booking Holdings)": "BKNG", "BKR (Baker Hughes)": "BKR", "BLK (BlackRock)": "BLK", "BMY (Bristol Myers Squibb)": "BMY", 
    "BR (Broadridge Financial Solutions)": "BR", "BRK.B (Berkshire Hathaway)": "BRK.B", "BRO (Brown & Brown)": "BRO", 
    "BSX (Boston Scientific)": "BSX", "BWA (BorgWarner)": "BWA", "BXP (Boston Properties)": "BXP", "C (Citigroup)": "C", 
    "CAG (Conagra Brands)": "CAG", "CAH (Cardinal Health)": "CAH", "CARR (Carrier Global)": "CARR", "CAT (Caterpillar)": "CAT",
    "CB (Chubb)": "CB", "CBOE (Cboe Global Markets)": "CBOE", "CBRE (CBRE)": "CBRE", "CCI (Crown Castle)": "CCI", 
    "CCL (Carnival)": "CCL", "CDAY (Ceridian HCM)": "CDAY", "CDNS (Cadence Design Systems)": "CDNS", "CDW (CDW)": "CDW", 
    "CE (Celanese)": "CE", "CEG (Constellation Energy)": "CEG", "CF (CF Industries Holdings)": "CF", 
    "CFG (Citizens Financial)": "CFG", "CHD (Church & Dwight)": "CHD", "CHRW (C.H Robinson Worldwide)": "CHRW",
    "CHTR (Charter Communications)": "CHTR", "CI (Cigna Group/The)": "CI", "CINF (Cincinnati Financial)": "CINF", 
    "CL (Colgate-Palmolive)": "CL", "CLX (Clorox)": "CLX", "CMA (Comerica)": "CMA", "CMCSA (Comcast)": "CMCSA", 
    "CME (CME Group)": "CME", "CMG (Chipotle Mexican Grill)": "CMG", "CMI (Cummins)": "CMI", "CMS (CMS Energy)": "CMS", 
    "CNC (Centene)": "CNC", "CNP (CenterPoint Energy)": "CNP", "COF (Capital One Financial)": "COF", "COO (Cooper)": "COO", 
    "COP (ConocoPhillips)": "COP", "COST (Costco)": "COST", "CPB (Campbell Soup)": "CPB", "CPRT (Copart)": "CPRT",
    "CPT (Camden Property Trust)": "CPT", "CRL (Charles River Laboratories)": "CRL", "CRM (Salesforce)": "CRM", 
    "CSCO (Cisco)": "CSCO", "CSGP (CoStar)": "CSGP", "CSX (CSX)": "CSX", "CTAS (Cintas)": "CTAS", "CTLT (Catalent)": "CTLT", 
    "CTRA (Coterra Energy)": "CTRA", "CTSH (Cognizant Technology Solutions)": "CTSH", "CTVA (Corteva)": "CTVA", 
    "CVS (CVS Health)": "CVS", "CVX (Chevron)": "CVX", "CZR (Caesars Entertainment)": "CZR", "D (Dominion Energy)": "D", 
    "DAL (Delta Air Lines)": "DAL", "DD (DuPont De Nemours)": "DD", "DE (Deere)": "DE", 
    "DFS (Discover Financial Services)": "DFS", "DG (Dollar General)": "DG", "DGX (Quest Diagnostics)": "DGX", 
    "DHI (D.R Horton)": "DHI", "DHR (Danaher)": "DHR", "DIS (Disney)": "DIS", "DISH (DISH Network)": "DISH", 
    "DLR (Digital Realty Trust)": "DLR", "DLTR (Dollar Tree)": "DLTR", "DOV (Dover)": "DOV", "DOW (Dow)": "DOW", 
    "DPZ (Domino's Pizza Inc)": "DPZ", "DRI (Darden Restaurants)": "DRI", "DTE (DTE Energy)": "DTE", 
    "DUK (Duke Energy)": "DUK", "DVA (DaVita)": "DVA", "DVN (Devon Energy)": "DVN", "DXC (DXC Technology)": "DXC",
    "DXCM (DexCom)": "DXCM", "EA (Electronic Arts)": "EA", "EBAY (EBay)": "EBAY", "ECL (Ecolab)": "ECL", 
    "ED (Consolidated Edison Inc)": "ED", "EFX (Equifax)": "EFX", "EIX (Edison)": "EIX", "EL (Estee Lauder)": "EL", 
    "ELV (Elevance Health)": "ELV", "EMN (Eastman Chemical)": "EMN", "EMR (Emerson Electric)": "EMR", 
    "ENPH (Enphase Energy)": "ENPH", "EOG (EOG Resources)": "EOG", "EPAM (EPAM Systems)": "EPAM", "EQIX (Equinix)": "EQIX", 
    "EQR (Equity Residential)": "EQR", "EQT (EQT)": "EQT", "ES (Eversource Energy)": "ES", "ESS (Essex Property Trust)": "ESS", 
    "ETN (Eaton)": "ETN", "ETR (Entergy)": "ETR", "ETSY (Etsy)": "ETSY", "EVRG (Evergy)": "EVRG", 
    "EW (Edwards Lifesciences)": "EW", "EXC (Exelon)": "EXC", "EXPD (Expeditors Of Washington)": "EXPD", 
    "EXPE (Expedia)": "EXPE", "EXR (Extra Space Storage Inc)": "EXR", "F (Ford Motor)": "F", "FANG (Diamondback Energy)": "FANG", 
    "FAST (Fastenal)": "FAST", "FCX (Freeport-McMoRan)": "FCX", "FDS (FactSet Research Systems)": "FDS", "FDX (FedEx)": "FDX", 
    "FE (FirstEnergy)": "FE", "FFIV (F5)": "FFIV", "FIS (Fidelity National Information Services)": "FIS", 
    "FISV (Fiserv)": "FISV", "FITB (Fifth Third Bancorp)": "FITB", "FLT (FleetCor Technologies)": "FLT", "FMC (FMC)": "FMC", 
    "FOX (Fox)": "FOX", "FOXA (Fox)": "FOXA", "FRC (First Republic Bank)": "FRC", 
    "FRT (Federal Realty Investment Trust)": "FRT", "FTNT (Fortinet)": "FTNT", "FTV (Fortive)": "FTV",
    "GD (General Dynamics)": "GD", "GE (General Electric)": "GE", "GEN (Gen Digital)": "GEN", 
    "GILD (Gilead Sciences)": "GILD", "GIS (General Mills)": "GIS", "GL (Globe Life)": "GL", "GLW (Corning)": "GLW",
    "GM (General Motors)": "GM", "GNRC (Generac Holdings)": "GNRC", "GOOG (Alphabet)": "GOOG", "GOOGL (Alphabet)": "GOOGL", 
    "GPC (Genuine Parts)": "GPC", "GPN (Global Payments)": "GPN", "GRMN (Garmin)": "GRMN", "GS (Goldman Sachs)": "GS",
    "GWW (W.W Grainger)": "GWW", "HAL (Halliburton)": "HAL", "HAS (Hasbro)": "HAS", "HBAN (Huntington Bancshares)": "HBAN", 
    "HCA (HCA Healthcare)": "HCA", "HD (Home Depot)": "HD", "HES (Hess)": "HES", "HIG (Hartford Financial Services)": "HIG",
    "HII (Huntington Ingalls Industries)": "HII", "HLT (Hilton Worldwide Holdings)": "HLT", "HOLX (Hologic)": "HOLX", 
    "HON (Honeywell)": "HON", "HPE (Hewlett Packard Enterprise)": "HPE", "HPQ (HP)": "HPQ", "HRL (Hormel Foods)": "HRL", 
    "HSIC (Henry Schein)": "HSIC", "HST (Host Hotels & Resorts)": "HST", "HSY (Hershey)": "HSY", "HUM (Humana)": "HUM", 
    "HWM (Howmet Aerospace)": "HWM", "IBM (IBM)": "IBM", "ICE (Intercontinental Exchange)": "ICE", 
    "IDXX (IDEXX Laboratories)": "IDXX", "IEX (IDEX)": "IEX", "IFF (International Flavors & Fragrances)": "IFF", 
    "ILMN (Illumina)": "ILMN", "INCY (Incyte)": "INCY", "INTC (Intel)": "INTC", "INTU (Intuit)": "INTU", 
    "INVH (Invitation Home)": "INVH", "IP (International Paper)": "IP", "IPG (Interpublic Group Of)": "IPG", 
    "IQV (IQVIA Holdings)": "IQV", "IR (Ingersoll Rand)": "IR", "IRM (Iron Mountain)": "IRM", 
    "ISRG (Intuitive Surgical)": "ISRG", "IT (Gartner)": "IT", "ITW (Illinois Tool Works)": "ITW", 
    "IVZ (Invesco)": "IVZ", "J (Jacobs Solutions)": "J", "JBHT (J.B Hunt Transport Services)": "JBHT", 
    "JCI (Johnson Controls)": "JCI", "JKHY (Jack Henry & Associates)": "JKHY", "JNJ (Johnson & Johnson)": "JNJ", 
    "JNPR (Juniper Networks)": "JNPR", "JPM (JPMorgan Chase)": "JPM", "K (Kellogg)": "K", "KDP (Keurig Dr Pepper)": "KDP", 
    "KEY (KeyCorp)": "KEY", "KEYS (Keysight Technologies)": "KEYS", "KHC (Kraft Heinz)": "KHC", "KIM (Kimco Realty)": "KIM",
    "KLAC (KLA)": "KLAC", "KMB (Kimberly-Clark)": "KMB", "KMI (Kinder Morgan)": "KMI", "KMX (CarMax)": "KMX",
    "KO (CocaCola)": "KO", "KR (Kroger)": "KR", "L (Loews)": "L", "LDOS (Leidos Holdings)": "LDOS", 
    "LEN (Lennar)": "LEN", "LH (Laboratory Of America Holdings)": "LH", "LHX (L3Harris Technologies Inc)": "LHX", 
    "LIN (Linde)": "LIN", "LKQ (LKQ)": "LKQ", "LLY (Eli Lilly)": "LLY", "LMT (Lockheed Martin)": "LMT", 
    "LNC (Lincoln National)": "LNC", "LNT (Alliant Energy)": "LNT", "LOW (Lowe's)": "LOW", 
    "LRCX (Lam Research)": "LRCX", "LUMN (Lumen Technologies)": "LUMN", "LUV (Southwest Airlines)": "LUV", 
    "LVS (Las Vegas Sands)": "LVS", "LW (Lamb Weston)": "LW", "LYB (LyondellBasell Industries)": "LYB", 
    "LYV (Live Nation Entertainment)": "LYV", "MA (Mastercard)": "MA", "MAA (Mid-America Apartment Communities)": "MAA", 
    "MAR (Marriott)": "MAR", "MAS (Masco)": "MAS", "MCD (McDonald's)": "MCD", "MCHP (Microchip Technology)": "MCHP", 
    "MCK (McKesson)": "MCK", "MCO (Moody's)": "MCO", "MDLZ (Mondelez)": "MDLZ", "MDT (Medtronic)": "MDT", 
    "MET (MetLife)": "MET", "META (Meta Platforms)": "META", "MGM (MGM Resorts)": "MGM", 
    "MHK (Mohawk Industries)": "MHK", "MKC (McCormick)": "MKC", "MKTX (MarketAxess Holdings)": "MKTX", 
    "MLM (Martin Marietta Materials)": "MLM", "MMC (Marsh & McLennan)": "MMC", "MMM (3M)": "MMM", 
    "MNST (Monster Beverage)": "MNST", "MO (Altria)": "MO", "MOH (Molina Healthcare)": "MOH", "MOS (Mosaic)": "MOS", 
    "MPC (Marathon Petroleum)": "MPC", "MPWR (Monolithic Power Systems)": "MPWR", "MRK (Merck)": "MRK", 
    "MRNA (Moderna)": "MRNA", "MRO (Marathon Oil)": "MRO", "MS (Morgan Stanley)": "MS", "MSCI (MSCI Inc)": "MSCI",
    "MSFT (Microsoft)": "MSFT", "MSI (Motorola Solutions)": "MSI", "MTB (M&T Bank)": "MTB", 
    "MTCH (Match Group)": "MTCH", "MTD (Mettler-Toledo)": "MTD", "MU (Micron Technology)": "MU", 
    "NCLH (Norwegian Cruise Line Holdings)": "NCLH", "NDAQ (Nasdaq)": "NDAQ", "NDSN (Nordson)": "NDSN", 
    "NEE (NextEra Energy)": "NEE", "NEM (Newmont)": "NEM", "NFLX (Netflix)": "NFLX", "NI (NiSource)": "NI", 
    "NKE (NIKE)": "NKE", "NOC (Northrop Grumman)": "NOC", "NOW (ServiceNow)": "NOW", "NRG (NRG Energy)": "NRG", 
    "NSC (Norfolk Southern)": "NSC", "NTAP (NetApp)": "NTAP", "NTRS (Northern Trust)": "NTRS", "NUE (Nucor)": "NUE", 
    "NVDA (NVIDIA)": "NVDA", "NVR (NVR)": "NVR", "NWL (Newell Brands)": "NWL", "NWS (News)": "NWS", 
    "NWSA (News)": "NWSA", "NXPI (NXP Semiconductors)": "NXPI", "O (Realty Income)": "O",
    "ODFL (Old Dominion Freight Line)": "ODFL", "OGN (Organon)": "OGN", "OKE (ONEOK)": "OKE",
    "OMC (Omnicom Group)": "OMC", "ON (ON Semiconductor)": "ON", "ORCL (Oracle)": "ORCL", 
    "ORLY (O'Reilly Automotive)": "ORLY", "OTIS (Otis Worldwide)": "OTIS", "OXY (Occidental Petroleum)": "OXY", 
    "PARA (Paramount Global)": "PARA", "PAYC (Paycom Software)": "PAYC", "PAYX (Paychex)": "PAYX", 
    "PCAR (PACCAR)": "PCAR", "PCG (Pacific Gas & Electric)": "PCG", "PEAK (Healthpeak Properties)": "PEAK", 
    "PEG (Public Service Enterprise Group)": "PEG", "PEP (PepsiCo)": "PEP", "PFE (Pfizer)": "PFE", 
    "PFG (Principal Financial)": "PFG", "PG (Procter & Gamble)": "PG", "PGR (Progressive)": "PGR", 
    "PH (Parker-Hannifin)": "PH", "PHM (PulteGroup)": "PHM", "PKG (Packaging Of America)": "PKG", 
    "PKI (PerkinElmer)": "PKI", "PLD (Prologis)": "PLD", "PM (Philip Morris)": "PM", 
    "PNC (PNC Financial Services)": "PNC", "PNR (Pentair)": "PNR", "PNW (Pinnacle West Capital)": "PNW", 
    "POOL (Pool)": "POOL", "PPG (PPG Industries)": "PPG", "PPL (PPL)": "PPL", 
    "PRU (Prudential Financial)": "PRU", "PSA (Public Storage)": "PSA", "PSX (Phillips 66)": "PSX", 
    "PTC (PTC)": "PTC", "PWR (Quanta Services)": "PWR", "PXD (Pioneer Natural Resources)": "PXD", 
    "PYPL (PayPal Holdings)": "PYPL", "QCOM (QUALCOMM)": "QCOM", "QRVO (Qorvo)": "QRVO", 
    "RCL (Royal Caribbean Cruises)": "RCL", "RE (Everest Re Group)": "RE", "REG (Regency Centers)": "REG", 
    "REGN (Regeneron Pharmaceuticals)": "REGN", "RF (Regions Financial)": "RF", "RHI (Robert Half)": "RHI", 
    "RJF (Raymond James Financial)": "RJF", "RL (Ralph Lauren)": "RL", "RMD (ResMed)": "RMD", 
    "ROK (Rockwell Automation)": "ROK", "ROL (Rollins)": "ROL", "ROP (Roper Technologies)": "ROP", 
    "ROST (Ross Stores)": "ROST", "RSG (Republic Services)": "RSG", "RTX (Raytheon Technologies)": "RTX",
    "SBAC (SBA Communications)": "SBAC", "SBNY (Signature Bank)": "SBNY", "SBUX (Starbucks)": "SBUX", 
    "SCHW (Charles Schwab)": "SCHW", "SEDG (SolarEdge Technologies)": "SEDG", "SEE (Sealed Air)": "SEE", 
    "SHW (Sherwin-Williams)": "SHW", "SIVB (SVB Financial Group)": "SIVB", "SJM (J M Smucker)": "SJM",
    "SLB (Schlumberger)": "SLB", "SNA (Snap-On)": "SNA", "SNPS (Synopsys)": "SNPS", "SO (Southern)": "SO",
    "SPG (Simon Property)": "SPG", "SPGI (S&P Global)": "SPGI", "SRE (Sempra Energy)": "SRE",
    "STE (STERIS)": "STE", "STT (State Street)": "STT", "STX (Seagate Technology Holdings)": "STX", 
    "STZ (Constellation Brands Inc)": "STZ", "SWK (Stanley Black & Decker)": "SWK", 
    "SWKS (Skyworks Solutions)": "SWKS", "SYF (Synchrony Financial)": "SYF", "SYK (Stryker)": "SYK", 
    "SYY (Sysco)": "SYY", "T (AT&T)": "T", "TAP (Molson Coors Beverage)": "TAP",
    "TDG (Transdigm Group)": "TDG", "TDY (Teledyne Technologies)": "TDY", "TECH (Bio-Techne Corp)": "TECH",
    "TEL (TE Connectivity)": "TEL", "TER (Teradyne)": "TER", "TFC (Truist Financial)": "TFC", 
    "TFX (Teleflex)": "TFX", "TGT (Target)": "TGT", "TJX (TJX)": "TJX", 
    "TMO (Thermo Fisher Scientific)": "TMO", "TMUS (T-Mobile US)": "TMUS", "TPR (Tapestry)": "TPR", 
    "TRGP (Targa Resources)": "TRGP", "TRMB (Trimble)": "TRMB", "TROW (T Rowe Price)": "TROW", 
    "TRV (Travelers)": "TRV", "TSCO (Tractor Supply)": "TSCO", "TSLA (Tesla)": "TSLA", "TSN (Tyson Foods)": "TSN", 
    "TT (Trane Technologies)": "TT", "TTWO (Take-Two Interactive Software)": "TTWO", "TXN (Texas Instruments)": "TXN", 
    "TXT (Textron)": "TXT", "TYL (Tyler Technologies)": "TYL", "UAL (United Airlines Holdings Inc)": "UAL", 
    "UDR (United Dominion Realty Trust)": "UDR", "UHS (Universal Health Services)": "UHS", "ULTA (Ulta Beauty)": "ULTA", 
    "UNH (UnitedHealth Group)": "UNH", "UNP (Union Pacific)": "UNP", "UPS (UPS)": "UPS", "URI (United Rentals)": "URI", 
    "USB (U.S Bancorp)": "USB", "V (Visa)": "V", "VFC (V.F)": "VFC", "VICI (VICI Properties)": "VICI", 
    "VLO (Valero Energy)": "VLO", "VMC (Vulcan Materials)": "VMC", "VNO (Vornado Realty Trust)": "VNO", 
    "VRSK (Verisk Analytics)": "VRSK", "VRSN (VeriSign)": "VRSN", "VRTX (Vertex Pharmaceuticals)": "VRTX", 
    "VTR (Ventas)": "VTR", "VTRS (Viatris)": "VTRS", "VZ (Verizon)": "VZ", "WAB (Westinghouse Air Brake Technologies)": "WAB", 
    "WAT (Waters)": "WAT", "WBA (Walgreens)": "WBA", "WBD (Warner Bros Discovery)": "WBD", "WDC (Western Digital)": "WDC", 
    "WEC (WEC Energy)": "WEC", "WELL (Welltower)": "WELL", "WFC (Wells Fargo)": "WFC", "WHR (Whirlpool)": "WHR",
    "WM (Waste Management)": "WM", "WMB (Williams)": "WMB", "WMT (Walmart)": "WMT", "WRB (W.R Berkley)": "WRB", 
    "WRK (WestRock)": "WRK", "WST (West Pharmaceutical Services)": "WST", "WTW (Willis Towers Watson Public)": "WTW",
    "WY (Weyerhaeuser)": "WY", "WYNN (Wynn Resorts)": "WYNN", "XEL (Xcel Energy)": "XEL", "XOM (Exxon)": "XOM", 
    "XRAY (DENTSPLY SIRONA)": "XRAY", "XYL (Xylem)": "XYL", "YUM (Yum! Brands)": "YUM", "ZBH (Zimmer Biomet Holdings)": 
    "ZBH", "ZBRA (Zebra Technologies)": "ZBRA", "ZION (Zions Bancorporation, N.A)": "ZION", "ZTS (Zoetis)": "ZTS",
}

indeces = {
    "S&P 500 (SPY)": "SPY",
    "NYSE US COMP (^XAX)": "^XAX",
    "DJ IND. AVG. (INDU)": "INDU",
    "NYSE COMP (^NYA)" : "^NYA",
    "NASDAQ COMP (^IXIC)": "^IXIC",
}

assets = {
    "Gold (GC=F)": "GC=F",
    "US bond (QLTA)": "QLTA",
    "Treas. 13w yield (^INX)": "^INX",
    "Treas. 5y yield (^FNX)": "^FNX",
    "Treas. 10y yield (^TNX)": "^TNX",
}

# merge all
available_symbols = {}
available_symbols.update(assets)
available_symbols.update(indeces)
available_symbols.update(stocks)

benchmarks = {}
benchmarks.update(assets)
benchmarks.update(indeces)


# define date range
start_date = "2000-01-22"
end_date  = datetime.today().strftime('%Y-%m-%d')

date_range = pd.date_range(start=start_date, end=end_date, freq="B")


def rs_ratio(prices_df, benchmark):
    
    """
    Function that returns dataframe with relative strength ratio for each symbol (days)
    """
    
    # create new dataframe
    index = prices_df.index
    ratio_df = pd.DataFrame(index=index)
    ratio_df.index = pd.to_datetime(ratio_df.index)
    
    benchmark = benchmark.rolling(12).mean()
    benchmark = benchmark.pct_change(5)
    
    #plt.plot(benchmark[-200:])

    for column in prices_df:
        prices_df[column] = prices_df[column].rolling(12).mean()
        prices_df[f'{column}_return'] = prices_df[column].pct_change(5)
        prices_df[f'{column}_ratio'] = prices_df[f'{column}_return'] - benchmark
        
    return prices_df.rolling(10).mean()

def rs_momentum(ratio_df):
    index = ratio_df.index

    momentum_df = pd.DataFrame(index=index)

    for column in ratio_df:
        name = column.split('_')[0]
        rs_momentum = ratio_df[column] - ratio_df[column].shift(5)
        momentum_df[f'{name}_momentum'] = rs_momentum.rolling(4).mean()
        
    return momentum_df


def visualize_asset_benchmark(df, asset_symbols, benchmark_symbol):
    """
    Function to visualize the RS ratio and Momentum on two separate graphs, given one symbol
    """
    # make a copy of the dataframe
    dff = df.copy()

    # if asset is a string then add column, otherwise add columns
    if type(asset_symbols) == str:
        asset = dff[("Adj Close", asset_symbols)]
    else:
        asset = dff[[("Adj Close", i) for i in asset_symbols]]

    # define benchmark column
    benchmark = dff[("Adj Close", benchmark_symbol)]

    # make graph
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

    # for every asset add a trace in the graph
    for column in asset:
        fig.add_trace(
            go.Scatter(x=asset.index, y=asset[column], name=f"Asset ({column[1]})"), row=1, col=1
        )
    
    # on the second graph plot only the benchmark
    fig.add_trace(
        go.Scatter(x=benchmark.index, y=benchmark, name=f"Benchmark ({benchmark_symbol})"), row=2, col=1
    )

    fig.update_layout(
        title=f"Benchmark ({benchmark_symbol}) vs asset ({asset_symbols})", 
        height=600, 
    )

    return fig

def visualize_rs(df, symbols):
    """
    Function to visualize the RS ratio and Momentum on two separate graphs, given one symbol
    """
    # make a copy of the dataframe
    dff = df.copy()

    # if symbols is string then add one column, else add multiple columns
    if type(symbols) == str:
        rs_ratio = dff[f"{symbols}_ratio"]
        rs_momentum = dff[f"{symbols}_momentum"]

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
        fig.add_trace(
            go.Scatter(x=rs_ratio.index, y=rs_ratio, name="RS Ratio"), row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=rs_momentum.index, y=rs_momentum, name="RS Momentum"), row=2, col=1
        )

        fig.update_layout(
            title=f"RS Ratio and Momentum for {symbols}", height=600, 
        )
    else:
        rs_ratio = dff[[f"{i}_ratio" for i in symbols]]
        rs_momentum = dff[[f"{i}_momentum" for i in symbols]]

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

        for ratio, momentum in zip(rs_ratio.columns, rs_momentum.columns):
            column =momentum.split("_")[0]
            fig.add_trace(
                go.Scatter(x=rs_ratio.index, y=rs_ratio[ratio], name=f"RS Ratio {column}"), row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=rs_momentum.index, y=rs_momentum[momentum], name=f"RS Momentum {column}"), row=2, col=1
            )

        fig.update_layout(
            title=f"RS Ratio and Momentum for {symbols}", height=600, 
        )
    return fig


def visualize_rrg(df, symbols, period):
    """
    Function to visualize the Relative Rotation Graph of the selected symbol
    """
    # make a copy of the dataframe
    dff = df.copy()

    # select last date
    dff = dff.iloc[-period:]

    # last datapoint
    past = dff.iloc[:-1]
    last = dff.iloc[-1]

    # plot figure
    fig = go.Figure()
    '''
    if type(symbols) ==str:
        fig.add_trace(
            go.Scatter(
                x=dff[f"{symbols}_ratio"],
                y=dff[f"{symbols}_momentum"],
                mode="lines",
                name=symbols,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[last[f"{symbols}_ratio"]],
                y=[last[f"{symbols}_momentum"]],
                mode="markers",
                marker=dict(size=7),
                showlegend=False,
                name = symbols,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=past[f"{symbols}_ratio"],
                y=past[f"{symbols}_momentum"],
                mode="markers",
                marker=dict(symbol="x"),
                showlegend=False,
            )
        )
    
    else:
    '''
    for i in symbols:
        fig.add_trace(
            go.Scatter(
                x=dff[f"{i}_ratio"],
                y=dff[f"{i}_momentum"],
                mode="lines",
                name=i,

            )
        )

        fig.add_trace(
            go.Scatter(
                x=[last[f"{i}_ratio"]],
                y=[last[f"{i}_momentum"]],
                mode="markers",
                marker=dict(size=7),
                showlegend=False,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=past[f"{i}_ratio"],
                y=past[f"{i}_momentum"],
                mode="markers",
                marker=dict(symbol="x"),
                showlegend=False,
            )
        )

    fig.update_layout(
        title=f"RRG graph",
        xaxis_title="RS ratio",
        yaxis_title="RS momentum",
        xaxis = dict(zerolinecolor='black'),
        yaxis = dict(zerolinecolor='black')
    )

    return fig
