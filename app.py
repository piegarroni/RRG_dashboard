import dash
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output, ctx, dcc, html # pip install dash (version 2.0.0 or higher)
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots

# external css static
external_stylesheets = [dbc.themes.SLATE]

# dash app with external stylesheet
app = Dash(__name__,
           external_stylesheets=external_stylesheets)

# all symbols to be retrieved in dashboard
stocks = {'A (Agilent Technologies)': 'A', 'AAL (American Airlines Group)': 'AAL', 'AAP (Advance Auto Parts)': 'AAP', 'AAPL (Apple)': 'AAPL', 'ABBV (AbbVie)': 'ABBV', 'ABC (AmerisourceBergen)': 'ABC', 'ABT (Abbott Laboratories)': 'ABT', 'ACGL (Arch Capital Group)': 'ACGL', 'ACN (Accenture)': 'ACN', 'ADBE (Adobe)': 'ADBE', 'ADI (Analog Devices)': 'ADI', 'ADM (Archer Daniels Midland)': 'ADM', 'ADP (ADP)': 'ADP', 'ADSK (Autodesk)': 'ADSK', 'AEE (Ameren)': 'AEE', 'AEP (American Electric Power)': 'AEP', 'AES (AES)': 'AES', 
          'AFL (Aflac)': 'AFL', 'AIG (American)': 'AIG', 'AIZ (Assurant)': 'AIZ', 'AJG (Arthur J Gallagher)': 'AJG', 'AKAM (Akamai Technologies)': 'AKAM', 'ALB (Albemarle)': 'ALB', 'ALGN (Align Technology)': 'ALGN', 'ALK (Alaska Air)': 'ALK', 'ALL (Allstate)': 'ALL', 'ALLE (Allegion)': 'ALLE', 'AMAT (Applied Materials)': 'AMAT', 'AMCR (Amcor)': 'AMCR', 'AMD (AMD)': 'AMD', 'AME (AMETEK)': 'AME', 'AMGN (Amgen)': 'AMGN', 'AMP (Ameriprise Financial)': 'AMP', 'AMT (American Tower)': 'AMT', 'AMZN (Amazon)': 'AMZN', 
          'ANET (Arista Networks)': 'ANET', 'ANSS (ANSYS)': 'ANSS', 'AON (Aon)': 'AON', 'AOS (A O Smith)': 'AOS', 'APA (APA)': 'APA', 'APD (Air Products And Chemicals)': 'APD', 'APH (Amphenol)': 'APH', 'APTV (Aptiv)': 'APTV', 'ARE (Alexandria Real Estate Equities)': 'ARE', 'ATO (Atmos Energy)': 'ATO', 'ATVI (Activision Blizzard)': 'ATVI', 'AVB (AvalonBay Communities)': 'AVB', 'AVGO (Broadcom)': 'AVGO', 'AVY (Avery Dennison)': 'AVY', 'AWK (American Water Works)': 'AWK', 'AXP (American Express)': 'AXP', 'AZO (AutoZone)': 'AZO', 'BA (Boeing)': 'BA', 'BAC (Bank Of America)': 'BAC', 'BALL (Ball)': 'BALL', 'BAX (Baxter)': 'BAX', 'BBWI (Bath & Body Works)': 'BBWI', 'BBY (Best Buy)': 'BBY', 'BDX (Becton Dickinson)': 'BDX', 'BEN (Franklin Resources)': 'BEN', 'BF.B (Brown-Forman)': 'BF.B', 'BIIB (Biogen)': 'BIIB', 'BIO (Bio-Rad Laboratories)': 'BIO', 'BK (Bank Of New York Mellon)': 'BK', 'BKNG (Booking Holdings)': 'BKNG', 'BKR (Baker Hughes)': 'BKR', 'BLK (BlackRock)': 'BLK', 'BMY (Bristol Myers Squibb)': 'BMY', 'BR (Broadridge Financial Solutions)': 'BR', 'BRK.B (Berkshire Hathaway)': 'BRK.B', 'BRO (Brown & Brown)': 'BRO', 'BSX (Boston Scientific)': 'BSX', 'BWA (BorgWarner)': 'BWA', 'BXP (Boston Properties)': 'BXP', 'C (Citigroup)': 'C', 'CAG (Conagra Brands)': 'CAG', 'CAH (Cardinal Health)': 'CAH', 'CARR (Carrier Global)': 'CARR', 'CAT (Caterpillar)': 'CAT', 'CB (Chubb)': 'CB', 'CBOE (Cboe Global Markets)': 'CBOE', 'CBRE (CBRE)': 'CBRE', 'CCI (Crown Castle)': 'CCI', 'CCL (Carnival)': 'CCL', 'CDAY (Ceridian HCM)': 'CDAY', 'CDNS (Cadence Design Systems)': 'CDNS', 'CDW (CDW)': 'CDW', 'CE (Celanese)': 'CE', 'CEG (Constellation Energy)': 'CEG', 'CF (CF Industries Holdings)': 'CF', 'CFG (Citizens Financial)': 'CFG', 'CHD (Church & Dwight)': 'CHD', 'CHRW (C.H Robinson Worldwide)': 'CHRW', 'CHTR (Charter Communications)': 'CHTR', 'CI (Cigna Group/The)': 'CI', 'CINF (Cincinnati Financial)': 'CINF', 'CL (Colgate-Palmolive)': 'CL', 'CLX (Clorox)': 'CLX', 'CMA (Comerica)': 'CMA', 'CMCSA (Comcast)': 'CMCSA', 'CME (CME Group)': 'CME', 'CMG (Chipotle Mexican Grill)': 'CMG', 'CMI (Cummins)': 'CMI', 'CMS (CMS Energy)': 'CMS', 'CNC (Centene)': 'CNC', 'CNP (CenterPoint Energy)': 'CNP', 'COF (Capital One Financial)': 'COF', 'COO (Cooper)': 'COO', 'COP (ConocoPhillips)': 'COP', 'COST (Costco)': 'COST', 'CPB (Campbell Soup)': 'CPB', 'CPRT (Copart)': 'CPRT', 'CPT (Camden Property Trust)': 'CPT', 'CRL (Charles River Laboratories)': 'CRL', 'CRM (Salesforce)': 'CRM', 'CSCO (Cisco)': 'CSCO', 'CSGP (CoStar)': 'CSGP', 'CSX (CSX)': 'CSX', 'CTAS (Cintas)': 'CTAS', 'CTLT (Catalent)': 'CTLT', 'CTRA (Coterra Energy)': 'CTRA', 'CTSH (Cognizant Technology Solutions)': 'CTSH', 'CTVA (Corteva)': 'CTVA', 'CVS (CVS Health)': 'CVS', 'CVX (Chevron)': 'CVX', 'CZR (Caesars Entertainment)': 'CZR', 'D (Dominion Energy)': 'D', 'DAL (Delta Air Lines)': 'DAL', 'DD (DuPont De Nemours)': 'DD', 'DE (Deere)': 'DE', 'DFS (Discover Financial Services)': 'DFS', 'DG (Dollar General)': 'DG', 'DGX (Quest Diagnostics)': 'DGX', 'DHI (D.R Horton)': 'DHI', 'DHR (Danaher)': 'DHR', 'DIS (Disney)': 'DIS', 'DISH (DISH Network)': 'DISH', 'DLR (Digital Realty Trust)': 'DLR', 'DLTR (Dollar Tree)': 'DLTR', 'DOV (Dover)': 'DOV', 'DOW (Dow)': 'DOW', "DPZ (Domino's Pizza Inc)": 'DPZ', 'DRI (Darden Restaurants)': 'DRI', 'DTE (DTE Energy)': 'DTE', 'DUK (Duke Energy)': 'DUK', 'DVA (DaVita)': 'DVA', 'DVN (Devon Energy)': 'DVN', 'DXC (DXC Technology)': 'DXC', 'DXCM (DexCom)': 'DXCM', 'EA (Electronic Arts)': 'EA', 'EBAY (EBay)': 'EBAY', 'ECL (Ecolab)': 'ECL', 'ED (Consolidated Edison Inc)': 'ED', 'EFX (Equifax)': 'EFX', 'EIX (Edison)': 'EIX', 'EL (Estee Lauder)': 'EL', 'ELV (Elevance Health)': 'ELV', 'EMN (Eastman Chemical)': 'EMN', 
          'EMR (Emerson Electric)': 'EMR', 'ENPH (Enphase Energy)': 'ENPH', 'EOG (EOG Resources)': 'EOG', 'EPAM (EPAM Systems)': 'EPAM', 'EQIX (Equinix)': 'EQIX', 'EQR (Equity Residential)': 'EQR', 'EQT (EQT)': 'EQT', 'ES (Eversource Energy)': 'ES', 'ESS (Essex Property Trust)': 'ESS', 'ETN (Eaton)': 'ETN', 'ETR (Entergy)': 'ETR', 'ETSY (Etsy)': 'ETSY', 'EVRG (Evergy)': 'EVRG', 'EW (Edwards Lifesciences)': 'EW', 'EXC (Exelon)': 'EXC', 'EXPD (Expeditors Of Washington)': 'EXPD', 'EXPE (Expedia)': 'EXPE', 'EXR (Extra Space Storage Inc)': 'EXR', 'F (Ford Motor)': 'F', 'FANG (Diamondback Energy)': 'FANG', 'FAST (Fastenal)': 'FAST', 'FCX (Freeport-McMoRan)': 'FCX', 'FDS (FactSet Research Systems)': 'FDS', 'FDX (FedEx)': 'FDX', 'FE (FirstEnergy)': 'FE', 'FFIV (F5)': 'FFIV', 'FIS (Fidelity National Information Services)': 'FIS', 'FISV (Fiserv)': 'FISV', 'FITB (Fifth Third Bancorp)': 'FITB', 'FLT (FleetCor Technologies)': 'FLT', 'FMC (FMC)': 'FMC', 'FOX (Fox)': 'FOX', 'FOXA (Fox)': 'FOXA', 'FRC (First Republic Bank)': 'FRC', 'FRT (Federal Realty Investment Trust)': 'FRT', 'FTNT (Fortinet)': 'FTNT', 'FTV (Fortive)': 'FTV', 'GD (General Dynamics)': 'GD', 'GE (General Electric)': 'GE', 'GEN (Gen Digital)': 'GEN', 'GILD (Gilead Sciences)': 'GILD', 'GIS (General Mills)': 'GIS', 'GL (Globe Life)': 'GL', 'GLW (Corning)': 'GLW', 'GM (General Motors)': 'GM', 'GNRC (Generac Holdings)': 'GNRC', 'GOOG (Alphabet)': 'GOOG', 'GOOGL (Alphabet)': 'GOOGL', 'GPC (Genuine Parts)': 'GPC', 'GPN (Global Payments)': 'GPN', 'GRMN (Garmin)': 'GRMN', 'GS (Goldman Sachs)': 'GS', 'GWW (W.W Grainger)': 'GWW', 'HAL (Halliburton)': 'HAL', 'HAS (Hasbro)': 'HAS', 'HBAN (Huntington Bancshares)': 'HBAN', 'HCA (HCA Healthcare)': 'HCA', 'HD (Home Depot)': 'HD', 'HES (Hess)': 'HES', 'HIG (Hartford Financial Services)': 'HIG', 'HII (Huntington Ingalls Industries)': 'HII', 'HLT (Hilton Worldwide Holdings)': 'HLT', 'HOLX (Hologic)': 'HOLX', 'HON (Honeywell)': 'HON', 'HPE (Hewlett Packard Enterprise)': 'HPE', 'HPQ (HP)': 'HPQ', 'HRL (Hormel Foods)': 'HRL', 'HSIC (Henry Schein)': 'HSIC', 'HST (Host Hotels & Resorts)': 'HST', 'HSY (Hershey)': 'HSY', 'HUM (Humana)': 'HUM', 'HWM (Howmet Aerospace)': 'HWM', 'IBM (IBM)': 'IBM', 'ICE (Intercontinental Exchange)': 'ICE', 'IDXX (IDEXX Laboratories)': 'IDXX', 'IEX (IDEX)': 'IEX', 'IFF (International Flavors & Fragrances)': 'IFF', 'ILMN (Illumina)': 'ILMN', 'INCY (Incyte)': 'INCY', 'INTC (Intel)': 'INTC', 'INTU (Intuit)': 'INTU', 'INVH (Invitation Home)': 'INVH', 'IP (International Paper)': 'IP', 'IPG (Interpublic Group Of)': 'IPG', 'IQV (IQVIA Holdings)': 'IQV', 'IR (Ingersoll Rand)': 'IR', 'IRM (Iron Mountain)': 'IRM', 'ISRG (Intuitive Surgical)': 'ISRG', 'IT (Gartner)': 'IT', 'ITW (Illinois Tool Works)': 'ITW', 'IVZ (Invesco)': 'IVZ', 'J (Jacobs Solutions)': 'J', 'JBHT (J.B Hunt Transport Services)': 'JBHT', 'JCI (Johnson Controls)': 'JCI', 'JKHY (Jack Henry & Associates)': 'JKHY', 'JNJ (Johnson & Johnson)': 'JNJ', 'JNPR (Juniper Networks)': 'JNPR', 'JPM (JPMorgan Chase)': 'JPM', 'K (Kellogg)': 'K', 'KDP (Keurig Dr Pepper)': 'KDP', 'KEY (KeyCorp)': 'KEY', 'KEYS (Keysight Technologies)': 'KEYS', 'KHC (Kraft Heinz)': 'KHC', 'KIM (Kimco Realty)': 'KIM', 'KLAC (KLA)': 'KLAC', 'KMB (Kimberly-Clark)': 'KMB', 'KMI (Kinder Morgan)': 'KMI', 'KMX (CarMax)': 'KMX', 'KO (CocaCola)': 'KO', 'KR (Kroger)': 'KR', 'L (Loews)': 'L', 'LDOS (Leidos Holdings)': 'LDOS', 'LEN (Lennar)': 'LEN', 'LH (Laboratory Of America Holdings)': 'LH', 'LHX (L3Harris Technologies Inc)': 'LHX', 'LIN (Linde)': 'LIN', 'LKQ (LKQ)': 'LKQ', 'LLY (Eli Lilly)': 'LLY', 'LMT (Lockheed Martin)': 'LMT', 'LNC (Lincoln National)': 'LNC', 'LNT (Alliant Energy)': 'LNT', "LOW (Lowe's)": 'LOW', 'LRCX (Lam Research)': 'LRCX', 'LUMN (Lumen Technologies)': 'LUMN', 'LUV (Southwest Airlines)': 'LUV', 'LVS (Las Vegas Sands)': 'LVS', 'LW (Lamb Weston)': 'LW', 'LYB (LyondellBasell Industries)': 'LYB', 'LYV (Live Nation Entertainment)': 'LYV', 'MA (Mastercard)': 'MA', 'MAA (Mid-America Apartment Communities)': 'MAA', 'MAR (Marriott)': 'MAR', 'MAS (Masco)': 'MAS', "MCD (McDonald's)": 'MCD', 'MCHP (Microchip Technology)': 'MCHP', 'MCK (McKesson)': 'MCK', "MCO (Moody's)": 'MCO', 'MDLZ (Mondelez)': 'MDLZ', 'MDT (Medtronic)': 'MDT', 'MET (MetLife)': 'MET', 'META (Meta Platforms)': 'META', 'MGM (MGM Resorts)': 'MGM', 'MHK (Mohawk Industries)': 'MHK', 'MKC (McCormick)': 'MKC', 'MKTX (MarketAxess Holdings)': 'MKTX', 'MLM (Martin Marietta Materials)': 'MLM', 'MMC (Marsh & McLennan)': 'MMC', 'MMM (3M)': 'MMM', 'MNST (Monster Beverage)': 'MNST', 'MO (Altria)': 'MO', 'MOH (Molina Healthcare)': 'MOH', 'MOS (Mosaic)': 'MOS', 'MPC (Marathon Petroleum)': 'MPC', 'MPWR (Monolithic Power Systems)': 'MPWR', 'MRK (Merck)': 'MRK', 'MRNA (Moderna)': 'MRNA', 'MRO (Marathon Oil)': 'MRO', 'MS (Morgan Stanley)': 'MS', 'MSCI (MSCI Inc)': 'MSCI', 'MSFT (Microsoft)': 'MSFT', 'MSI (Motorola Solutions)': 'MSI', 'MTB (M&T Bank)': 'MTB', 'MTCH (Match Group)': 'MTCH', 'MTD (Mettler-Toledo)': 'MTD', 'MU (Micron Technology)': 'MU', 'NCLH (Norwegian Cruise Line Holdings)': 'NCLH', 
          'NDAQ (Nasdaq)': 'NDAQ', 'NDSN (Nordson)': 'NDSN', 'NEE (NextEra Energy)': 'NEE', 'NEM (Newmont)': 'NEM', 'NFLX (Netflix)': 'NFLX', 'NI (NiSource)': 'NI', 'NKE (NIKE)': 'NKE', 'NOC (Northrop Grumman)': 'NOC', 'NOW (ServiceNow)': 'NOW', 'NRG (NRG Energy)': 'NRG', 'NSC (Norfolk Southern)': 'NSC', 'NTAP (NetApp)': 'NTAP', 'NTRS (Northern Trust)': 'NTRS', 'NUE (Nucor)': 'NUE', 'NVDA (NVIDIA)': 'NVDA', 'NVR (NVR)': 'NVR', 'NWL (Newell Brands)': 'NWL', 'NWS (News)': 'NWS', 'NWSA (News)': 'NWSA', 'NXPI (NXP Semiconductors)': 'NXPI', 'O (Realty Income)': 'O', 'ODFL (Old Dominion Freight Line)': 'ODFL', 'OGN (Organon)': 'OGN', 'OKE (ONEOK)': 'OKE', 'OMC (Omnicom Group)': 'OMC', 'ON (ON Semiconductor)': 'ON', 'ORCL (Oracle)': 'ORCL', "ORLY (O'Reilly Automotive)": 'ORLY', 'OTIS (Otis Worldwide)': 'OTIS', 'OXY (Occidental Petroleum)': 'OXY', 'PARA (Paramount Global)': 'PARA', 'PAYC (Paycom Software)': 'PAYC', 'PAYX (Paychex)': 'PAYX', 'PCAR (PACCAR)': 'PCAR', 'PCG (Pacific Gas & Electric)': 'PCG', 'PEAK (Healthpeak Properties)': 'PEAK', 'PEG (Public Service Enterprise Group)': 'PEG', 'PEP (PepsiCo)': 'PEP', 'PFE (Pfizer)': 'PFE', 'PFG (Principal Financial)': 'PFG', 'PG (Procter & Gamble)': 'PG', 'PGR (Progressive)': 'PGR', 'PH (Parker-Hannifin)': 'PH', 'PHM (PulteGroup)': 'PHM', 'PKG (Packaging Of America)': 'PKG', 'PKI (PerkinElmer)': 'PKI', 'PLD (Prologis)': 'PLD', 'PM (Philip Morris)': 'PM', 'PNC (PNC Financial Services)': 'PNC', 'PNR (Pentair)': 'PNR', 'PNW (Pinnacle West Capital)': 'PNW', 'POOL (Pool)': 'POOL', 'PPG (PPG Industries)': 'PPG', 'PPL (PPL)': 'PPL', 'PRU (Prudential Financial)': 'PRU', 'PSA (Public Storage)': 'PSA', 'PSX (Phillips 66)': 'PSX', 'PTC (PTC)': 'PTC', 'PWR (Quanta Services)': 'PWR', 'PXD (Pioneer Natural Resources)': 'PXD', 'PYPL (PayPal Holdings)': 'PYPL', 'QCOM (QUALCOMM)': 'QCOM', 'QRVO (Qorvo)': 'QRVO', 'RCL (Royal Caribbean Cruises)': 'RCL', 'RE (Everest Re Group)': 'RE', 'REG (Regency Centers)': 'REG', 'REGN (Regeneron Pharmaceuticals)': 'REGN', 'RF (Regions Financial)': 'RF', 'RHI (Robert Half)': 'RHI', 'RJF (Raymond James Financial)': 'RJF', 'RL (Ralph Lauren)': 'RL', 'RMD (ResMed)': 'RMD', 'ROK (Rockwell Automation)': 'ROK', 'ROL (Rollins)': 'ROL', 'ROP (Roper Technologies)': 'ROP', 'ROST (Ross Stores)': 'ROST', 'RSG (Republic Services)': 'RSG', 'RTX (Raytheon Technologies)': 'RTX', 'SBAC (SBA Communications)': 'SBAC', 'SBNY (Signature Bank)': 'SBNY', 'SBUX (Starbucks)': 'SBUX', 'SCHW (Charles Schwab)': 'SCHW', 'SEDG (SolarEdge Technologies)': 'SEDG', 'SEE (Sealed Air)': 'SEE', 'SHW (Sherwin-Williams)': 'SHW', 'SIVB (SVB Financial Group)': 'SIVB', 'SJM (J M Smucker)': 'SJM', 'SLB (Schlumberger)': 'SLB', 'SNA (Snap-On)': 'SNA', 'SNPS (Synopsys)': 'SNPS', 'SO (Southern)': 'SO', 'SPG (Simon Property)': 'SPG', 'SPGI (S&P Global)': 'SPGI', 'SRE (Sempra Energy)': 'SRE', 'STE (STERIS)': 'STE', 'STT (State Street)': 'STT', 'STX (Seagate Technology Holdings)': 'STX', 'STZ (Constellation Brands Inc)': 'STZ', 'SWK (Stanley Black & Decker)': 'SWK', 'SWKS (Skyworks Solutions)': 'SWKS', 'SYF (Synchrony Financial)': 'SYF', 'SYK (Stryker)': 'SYK', 'SYY (Sysco)': 'SYY', 'T (AT&T)': 'T', 'TAP (Molson Coors Beverage)': 'TAP', 'TDG (Transdigm Group)': 'TDG', 'TDY (Teledyne Technologies)': 'TDY', 'TECH (Bio-Techne Corp)': 'TECH', 'TEL (TE Connectivity)': 'TEL', 'TER (Teradyne)': 'TER', 'TFC (Truist Financial)': 'TFC', 'TFX (Teleflex)': 'TFX', 'TGT (Target)': 'TGT', 'TJX (TJX)': 'TJX', 'TMO (Thermo Fisher Scientific)': 'TMO', 'TMUS (T-Mobile US)': 'TMUS', 'TPR (Tapestry)': 'TPR', 'TRGP (Targa Resources)': 'TRGP', 'TRMB (Trimble)': 'TRMB', 'TROW (T Rowe Price)': 'TROW', 'TRV (Travelers)': 'TRV', 'TSCO (Tractor Supply)': 'TSCO', 'TSLA (Tesla)': 'TSLA', 'TSN (Tyson Foods)': 'TSN', 'TT (Trane Technologies)': 'TT', 'TTWO (Take-Two Interactive Software)': 'TTWO', 'TXN (Texas Instruments)': 'TXN', 'TXT (Textron)': 'TXT', 'TYL (Tyler Technologies)': 'TYL', 'UAL (United Airlines Holdings Inc)': 'UAL', 'UDR (United Dominion Realty Trust)': 'UDR', 'UHS (Universal Health Services)': 'UHS', 'ULTA (Ulta Beauty)': 'ULTA', 'UNH (UnitedHealth Group)': 'UNH', 'UNP (Union Pacific)': 'UNP', 'UPS (UPS)': 'UPS', 'URI (United Rentals)': 'URI', 'USB (U.S Bancorp)': 'USB', 'V (Visa)': 'V', 'VFC (V.F)': 'VFC', 'VICI (VICI Properties)': 'VICI', 'VLO (Valero Energy)': 'VLO', 'VMC (Vulcan Materials)': 'VMC', 'VNO (Vornado Realty Trust)': 'VNO', 'VRSK (Verisk Analytics)': 'VRSK', 'VRSN (VeriSign)': 'VRSN', 'VRTX (Vertex Pharmaceuticals)': 'VRTX', 'VTR (Ventas)': 'VTR', 'VTRS (Viatris)': 'VTRS', 'VZ (Verizon)': 'VZ', 'WAB (Westinghouse Air Brake Technologies)': 'WAB', 'WAT (Waters)': 'WAT', 'WBA (Walgreens)': 'WBA', 'WBD (Warner Bros Discovery)': 'WBD', 'WDC (Western Digital)': 'WDC', 'WEC (WEC Energy)': 'WEC', 'WELL (Welltower)': 'WELL', 'WFC (Wells Fargo)': 'WFC', 'WHR (Whirlpool)': 'WHR', 'WM (Waste Management)': 'WM', 'WMB (Williams)': 'WMB', 'WMT (Walmart)': 'WMT', 'WRB (W.R Berkley)': 'WRB', 'WRK (WestRock)': 'WRK', 
          'WST (West Pharmaceutical Services)': 'WST', 'WTW (Willis Towers Watson Public)': 'WTW', 'WY (Weyerhaeuser)': 'WY', 'WYNN (Wynn Resorts)': 'WYNN', 'XEL (Xcel Energy)': 'XEL', 'XOM (Exxon)': 'XOM', 'XRAY (DENTSPLY SIRONA)': 'XRAY', 'XYL (Xylem)': 'XYL', 'YUM (Yum! Brands)': 'YUM', 'ZBH (Zimmer Biomet Holdings)': 'ZBH', 'ZBRA (Zebra Technologies)': 'ZBRA', 'ZION (Zions Bancorporation, N.A)': 'ZION', 'ZTS (Zoetis)': 'ZTS'}

indeces = {'NYSE US COMP': '^XAX', 'DJ IND. AVG.': 'INDU', 'NYSE COMP':'^NYA', 'NASDAQ COMP': '^IXIC'}

assets = {'Gold': 'GC=F', 'US bond': 'QLTA','Treas. 13w yield': '^INX','Treas. 5y yield': '^FNX','Treas. 10y yield': '^TNX'}
available_symbols = {}
available_symbols.update(assets)
available_symbols.update(indeces)
available_symbols.update(stocks)

# define range
start_date = '2000-01-22'
end_date = '2023-02-22'
date_range = pd.date_range(start=start_date, end=end_date, freq='B')
print(date_range)

def rs_ratio(prices_df, benchmark, window=14):
    """
    Method to return dataframe with relative strength ratio for each symbol
    """
    
    ratio_df = pd.DataFrame()
    
    for column in prices_df:
        rs = (prices_df[column] / benchmark) * 100
        rs_ratio = rs.rolling(window).mean()
        rel_ratio = 100 + ((rs_ratio - rs_ratio.mean()) / rs_ratio.std() + 1)
    
        ratio_df[f'{column}_ratio'] = rel_ratio
        
    ratio_df.dropna(axis=0, how='all', inplace=True)
    
    return ratio_df

def rs_momentum(prices_df, benchmark, window=14):
    """
    Method to return dataframe with relative strength momentum for each symbol
    """
    momentum_df = pd.DataFrame()
    for column in prices_df:
        rs = (prices_df[column] / benchmark) * 100
        rs_ratio = rs.rolling(window).mean()      
        rs_momentum = rs_ratio - rs_ratio.shift(window)
        rel_momentum = 100 + ((rs_momentum - rs_momentum.mean()) / rs_momentum.std() + 1)
        momentum_df[f'{column}_momentum'] = rel_momentum   
    momentum_df.dropna(axis=0, how='all', inplace=True)
    return momentum_df
        
def visualize_rs(df, symbol:str):
    """
    Method to visualize the RS ratio and Momentum on two separate graphs, given one symbol
    """
    rs_ratio = df[f'{symbol}_ratio']
    rs_momentum = df[f'{symbol}_momentum']
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
    fig.add_trace(go.Scatter(x=rs_ratio.index, y=rs_ratio, name="RS Ratio"), row=1, col=1)
    fig.add_trace(go.Scatter(x=rs_momentum.index, y=rs_momentum, name="RS Momentum"), row=2, col=1)
    fig.update_layout(title=f"RS Ratio and Momentum for {symbol}", height=800)
    return fig


def visualize_rrg(df, symbol, period, last_date):
    df = df.copy()

    df = df.loc[df.index<=last_date]
    df = df.iloc[-period:]

    last = df.iloc[-1]  
    past = df.iloc[:-1]    

    # plot figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df[f'{symbol}_ratio'], y=df[f'{symbol}_momentum'], mode='lines', name='Data'))
    fig.add_trace(go.Scatter(x=[last[f'{symbol}_ratio']], y=[last[f'{symbol}_momentum']], mode='markers', marker=dict(size = 7), name='Last'))
    fig.add_trace(go.Scatter(x=past[f'{symbol}_ratio'], y=past[f'{symbol}_momentum'], mode='markers', marker=dict(symbol='x'), name='Past'))

    # add vertical and horizontal quadrants line
    fig.add_trace(go.Scatter(x=[0, 200], y=[100, 100], mode='lines', line=dict(color='darkgrey', width=1), name='Horizontal line'))
    fig.add_trace(go.Scatter(y=[0, 200], x=[100, 100], mode='lines', line=dict(color='darkgrey', width=1), name='Horizontal line'))

    fig.update_layout(title=f"RRG graph for {symbol}", xaxis_title="RS ratio", yaxis_title="RS momentum", 
                  xaxis_range=[95, 105], yaxis_range=[95, 105])
    return fig




app.layout = html.Div([
        html.H1("Visualizing RS Ratio and Momentum"),
        html.Label("Select a symbol:"),

        dcc.Dropdown(
            id="symbol-dropdown",
            options=[{"label": symbol, "value": available_symbols[symbol]} for symbol in available_symbols],
            value=available_symbols['NYSE US COMP']
        ),
        html.Br(),


        dcc.Graph(id="rs-plot"),
        html.Br(),
        html.Br(),

        html.Label("Select tail length (days):"),
        dcc.Slider(
            id='tail-length',
            min=5,
            max=50,
            value=20,
            marks={i: str(i) for i in range(5, 51)}
        ),  
        html.Br(),

        html.Label("Select period (last point):"),
 

        dcc.Slider(id='time-range',
            marks={i: {"label": str(date_range[i]).split('00:00')[0], "style": {"transform": "rotate(45deg)", 'color':'white'}}
                        for i in range(0, len(date_range), 15)},
            min=0,
            max=len(date_range) - 1,
            value= len(date_range)-1,
        ),
        html.Br(),
        html.Div(id='output_container', children=[]),
        html.Br(),

        dcc.Graph(id='rrg-plot', figure={}, style={'width': '100%', 'height': '67vh', 'backgroundColor': 'black'}),
        html.Br(),
    ],
    style={"margin": "35px 5% 75px 5%"}
)


@app.callback(
    dash.dependencies.Output("rs-plot", "figure"), dash.dependencies.Output("rrg-plot", "figure"), dash.dependencies.Output("output_container", "children"),
    [dash.dependencies.Input("symbol-dropdown", "value"), 
     dash.dependencies.Input("tail-length", "value"), 
     dash.dependencies.Input("time-range", "value")]
)
def update_plots(symbol, tail_len, last_date):
    triggered = dash.callback_context.triggered[0]['prop_id']
    symbol_changed = "symbol-dropdown" in triggered
    print(symbol_changed)

    # Download data from Yahoo Finance only if the symbol has changed
    if symbol_changed:

        data = yf.download([symbol, 'SPY'], start_date, end_date)
        print('data downloaded')


    #---------------------------------
    last_date = date_range[last_date]

    # download data from yahoo
    data = yf.download([symbol, 'SPY'], start_date, end_date)

    #retrieve rs ratio and mometnum
    ratio_df = rs_ratio(data['Adj Close'], data[('Adj Close', 'SPY')])
    momentum_df = rs_momentum(data['Adj Close'], data[('Adj Close', 'SPY')])

    # merge rs ratio and momentum data
    df = pd.merge(ratio_df, momentum_df, left_on=ratio_df.index, right_on=momentum_df.index).set_index('key_0')

    container = f'Displaying RRG graph for {symbol} from {str(last_date)}, with tail length {tail_len}'

    return visualize_rs(df, symbol), visualize_rrg(df, symbol, int(tail_len), last_date), container

if __name__ == "__main__":
    app.run_server(debug=True)