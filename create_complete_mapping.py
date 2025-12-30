import json

# Manual mapping based on pattern analysis between data and Excel
manual_mappings = {
    # Broad Market
    "tri - Nifty 50": ("N50", "NIFTY 50", "Broad Market"),
    "tri - Nifty NEXT 50": ("NN50", "NIFTY NEXT 50", "Broad Market"),
    "tri - Nifty 100": ("N100", "NIFTY 100", "Broad Market"),
    "tri - Nifty 200": ("N200", "NIFTY 200", "Broad Market"),
    "tri - NIFTY TOTAL MKT": ("NTM", "Nifty Total Market", "Broad Market"),
    "tri - Nifty 500": ("N500", "NIFTY 500", "Broad Market"),
    "tri - NIFTY500 MULTICAP": ("N500_MC_50_25_25", "NIFTY500 MULTICAP 50:25:25", "Broad Market"),
    "tri - Nifty500 EW": ("N500_EQ", "NIFTY500 EQUAL WEIGHT", "Broad Market"),
    "tri - NIFTY MIDCAP 150": ("NMC150", "NIFTY MIDCAP 150", "Broad Market"),
    "tri - Nifty Midcap 50": ("NMC50", "NIFTY MIDCAP 50", "Broad Market"),
    "tri - NIFTY MID SELECT": ("NMCS", "Nifty Midcap Select", "Broad Market"),
    "tri - NIFTY MIDCAP 100": ("NMC100", "NIFTY MIDCAP 100", "Broad Market"),
    "tri - NIFTY SMLCAP 250": ("NSC250", "NIFTY SMALLCAP 250", "Broad Market"),
    "tri - NIFTY SMLCAP 50": ("NSC50", "NIFTY SMALLCAP 50", "Broad Market"),
    "tri - NIFTY SMLCAP 100": ("NSC100", "NIFTY SMALLCAP 100", "Broad Market"),
    "tri - NIFTY MICROCAP250": ("NMICRO250", "NIFTY MICROCAP 250", "Broad Market"),
    "tri - NIFTY LARGEMID250": ("NLMC250", "NIFTY LargeMidcap 250", "Broad Market"),
    "tri - NIFTY MIDSML 400": ("NMSC400", "NIFTY MIDSMALLCAP 400", "Broad Market"),
    "tri - Nifty Mid Liq 15": ("NMC_LIQ15", "NIFTY MIDCAP LIQUID 15", "Broad Market"),
    "tri - Nifty100 Liq 15": ("N100_LIQ15", "NIFTY100 LIQUID 15", "Broad Market"),
    "tri - NIFTY IPO": ("NIPO", "NIFTY IPO", "Broad Market"),
    "tri - Nifty SME EMERGE": ("NSME", "NIFTY SME EMERGE", "Broad Market"),
    
    # Sectoral
    "tri - Nifty Auto": ("NAUTO", "NIFTY AUTO", "Sectoral"),
    "tri - Nifty Bank": ("NBANK", "NIFTY BANK", "Sectoral"),
    "tri - Nifty CHEMICALS": ("NCHEM", "NIFTY CHEMICALS", "Sectoral"),
    "tri - Nifty Fin Service": ("NFIN", "NIFTY FINANCIAL SERVICES", "Sectoral"),
    "tri - NIFTY FINSRV25 50": ("NFIN_25_50", "NIFTY FINANCIAL SERVICES 25/50", "Sectoral"),
    "tri - Nifty FinSerExBnk": ("NFIN_EXB", "Nifty Financial Services Ex Bank", "Sectoral"),
    "tri - Nifty FMCG": ("NFMCG", "NIFTY FMCG", "Sectoral"),
    "tri - NIFTY HEALTHCARE": ("NHEALTH", "Nifty HEALTHCARE", "Sectoral"),
    "tri - Nifty IT": ("NIT", "NIFTY IT", "Sectoral"),
    "tri - NIFTY MEDIA": ("NMEDIA", "NIFTY MEDIA", "Sectoral"),
    "tri - Nifty Metal": ("NMETAL", "NIFTY METAL", "Sectoral"),
    "tri - Nifty Pharma": ("NPHARMA", "NIFTY PHARMA", "Sectoral"),
    "tri - Nifty Pvt Bank": ("NPRVB", "NIFTY PRIVATE BANK", "Sectoral"),
    "tri - Nifty PSU Bank": ("NPSUB", "NIFTY PSU BANK", "Sectoral"),
    "tri - Nifty Realty": ("NREALTY", "NIFTY REALTY", "Sectoral"),
    "tri - NIFTY CONSR DURBL": ("NCD", "NIFTY CONSUMER DURABLES", "Sectoral"),
    "tri - NIFTY OIL AND GAS": ("NOILGAS", "NIFTY OIL AND GAS INDEX", "Sectoral"),
    "tri - Nifty Capital Market": ("NCAPMKT", "Nifty Capital Markets", "Sectoral"),
    "tri - Nifty Commodities": ("NCOM", "NIFTY COMMODITIES", "Sectoral"),
    "tri - Nifty Energy": ("NENERGY", "NIFTY ENERGY", "Sectoral"),
    "tri - Nifty Infra": ("NINFRA", "NIFTY INFRASTRUCTURE", "Sectoral"),
    "tri - Nifty Serv Sector": ("NSERVICE", "NIFTY SERVICES SECTOR", "Sectoral"),
    "tri - Nifty Trans Logis": ("NTRANS", "Nifty Transportation & Logistics", "Sectoral"),
    "tri - Nifty MS Fin Serv": ("NMS_FIN", "Nifty MidSmall Financial Services", "Sectoral"),
    "tri - NIFTY MIDSML HLTH": ("NMS_HEALTH", "Nifty MidSmall Healthcare", "Sectoral"),
    "tri - Nifty MS IT Telcm": ("NMS_IT", "Nifty MidSmall IT & Telecom", "Sectoral"),
    
    # Strategy
    "tri - NIFTY100 EQL WGT": ("N100_EQ", "NIFTY 100 EQUAL WEIGHT", "Strategy"),
    "tri - NIFTY100 LOWVOL30": ("N100_LV30", "NIFTY 100 LOW VOLATILITY 30", "Strategy"),
    "tri - Nifty200Momentm30": ("N200_MOM30", "NIFTY200 MOMENTUM 30", "Strategy"),
    "tri - Nifty200 Alpha 30": ("N200_A30", "NIFTY200 ALPHA 30", "Strategy"),
    "tri - Nifty100 Alpha 30": ("N100_A30", "NIFTY100 ALPHA 30", "Strategy"),
    "tri - NIFTY ALPHA 50": ("NA50", "NIFTY ALPHA 50", "Strategy"),
    "tri - NIFTY ALPHALOWVOL": ("NALV30", "NIFTY ALPHA LOW VOLATILITY 30", "Strategy"),
    "tri - Nifty Qlty LV 30": ("NAQLV30", "NIFTY ALPHA QUALITY LOW VOLATILITY 30", "Strategy"),
    "tri - Nifty AQLV 30": ("NAQVL30", "NIFTY ALPHA QUALITY VALUE LOW-VOLATILITY 30", "Strategy"),
    "tri - Nifty Div Opps 50": ("NDIV50", "NIFTY DIVIDEND OPPORTUNITIES 50", "Strategy"),
    "tri - Nifty GrowSect 15": ("NGROW15", "NIFTY GROWTH SECTORS 15", "Strategy"),
    "tri - Nifty HighBeta 50": ("NHB50", "NIFTY HIGH BETA 50", "Strategy"),
    "tri - Nifty Low Vol 50": ("NLV50", "NIFTY LOW VOLATILITY 50", "Strategy"),
    "tri - Nifty Top 10 EW": ("NT10_EQ", "NIFTY TOP 10 EQUAL WEIGHT", "Strategy"),
    "tri - Nifty Top 15 EW": ("NT15_EQ", "NIFTY TOP 15 EQUAL WEIGHT", "Strategy"),
    "tri - Nifty Top 20 EW": ("NT20_EQ", "NIFTY TOP 20 EQUAL WEIGHT", "Strategy"),
    "tri - NIFTY100 QUALTY30": ("N100_Q30", "NIFTY100 QUALITY 30", "Strategy"),
    "tri - NIFTYM150MOMNTM50": ("NMC150_MOM50", "NIFTY Midcap150 Momentum 50", "Strategy"),
    "tri - NIFTY500 FLEXICAP": ("N500_FQ30", "Nifty500 Flexicap Quality 30", "Strategy"),
    "tri - Nifty500 LowVol50": ("N500_LV50", "NIFTY500 LOW VOLATILITY 50", "Strategy"),
    "tri - Nifty500Momentm50": ("N500_MOM50", "NIFTY500 MOMENTUM 50", "Strategy"),
    "tri - Nifty500 Qlty50": ("N500_Q50", "NIFTY500 QUALITY 50", "Strategy"),
    "tri - Nifty500 MQVLv50": ("N500_MF50", "NIFTY500 MULTIFACTOR MQVLv 50", "Strategy"),
    "tri - NIFTY M150 QLTY50": ("NMC150_Q50", "NIFTY Midcap150 Quality 50", "Strategy"),
    "tri - Nifty Sml250 Q50": ("NSC250_Q50", "Nifty Smallcap250 Quality 50", "Strategy"),
    "tri - NIFTY TMMQ 50": ("N500_MCMQ50", "NIFTY500 MULTICAP MOMENTUM QUALITY 50", "Strategy"),
    "tri - NiftyMS400 MQ 100": ("NMSC400_MQ100", "Nifty MidSmallcap400 Momentum Quality 100", "Strategy"),
    "tri - NiftySml250MQ 100": ("NSC250_MQ100", "Nifty Smallcap250 Momentum Quality 100", "Strategy"),
    "tri - Nifty Multi MQ 50": ("NQLV30", "NIFTY QUALITY LOW VOLATILITY 30", "Strategy"),
    "tri - NIFTY50 EQL WGT": ("N50_EQ", "NIFTY50 EQUAL WEIGHT", "Strategy"),
    "tri - Nifty50 Value 20": ("N50_V20", "NIFTY50 VALUE 20", "Strategy"),
    "tri - Nifty200 Value 30": ("N200_V30", "Nifty200 Value 30", "Strategy"),
    "tri - Nifty500 Value 50": ("N500_V50", "NIFTY500 VALUE 50", "Strategy"),
    "tri - Nifty200 Quality 30": ("N200_Q30", "NIFTY200 Quality 30", "Strategy"),
    
    # Thematic
    "tri - DSP QUANT": ("DSP_Q", "DSP QUANT", "Thematic"),
    "tri - DSP ELSS": ("DSP_ELSS", "DSP ELSS", "Thematic"),
    "tri - ICICI PRU SILVER": ("SILVER", "ICICI PRU SILVER", "Thematic"),
    "tri - Nifty GS 10Yr Cln": ("GSEC_10Y", "NIFTY 10 YR BENCHMARK G-SEC", "Thematic"),
    "tri - KOTAK CONTRA": ("KOTAK_CONTRA", "KOTAK CONTRA", "Thematic"),
    "tri - KOTAK GOLD": ("GOLD", "KOTAK GOLD", "Thematic"),
    "tri - UTI FLEX": ("UTI_FLEX", "UTI FLEX", "Thematic"),
    "tri - AXIS INNOVATION": ("AXIS_INNOV", "AXIS INNOVATION", "Thematic"),
    "tri - Nifty Aditya Birla": ("N_ADITYA", "NIFTY INDIA CORPORATE GROUP INDEX - ADITYA BIRLA GROUP", "Thematic"),
    "tri - Nifty CoreHousing": ("N_CORE_HOUS", "Nifty Core Housing", "Thematic"),
    "tri - Nifty CPSE": ("NCPSE", "NIFTY CPSE", "Thematic"),
    "tri - Nifty EV New Age": ("NEV", "Nifty EV & New Age Automotive", "Thematic"),
    "tri - Nifty Housing": ("NHOUSING", "Nifty Housing", "Thematic"),
    "tri - NIFTY100 ESG": ("N100_ESG", "NIFTY100 ESG", "Thematic"),
    "tri - Nifty100 Enh ESG": ("N100_EESG", "NIFTY100 Enhanced ESG", "Thematic"),
    "tri - Nifty100ESGSecLdr": ("N100_ESG_SL", "Nifty100 ESG Sector Leaders", "Thematic"),
    "tri - Nifty Consumption": ("N_CONSUME", "NIFTY INDIA CONSUMPTION", "Thematic"),
    "tri - Nifty India Defence": ("N_DEFENCE", "Nifty India Defence", "Thematic"),
    "tri - NIFTY IND DIGITAL": ("N_DIGITAL", "Nifty India Digital", "Thematic"),
    "tri - NIFTY INFRALOG": ("N_INFRA_LOG", "NIFTY INDIA INFRASTRUCTURE & LOGISTICS", "Thematic"),
    "tri - Nifty India Internet": ("N_INTERNET", "Nifty India Internet", "Thematic"),
    "tri - NIFTY INDIA MFG": ("N_MANUF", "Nifty India Manufacturing", "Thematic"),
    "tri - Nifty Ind Tourism": ("N_TOURISM", "NIFTY INDIA TOURISM", "Thematic"),
    "tri - Nifty Mahindra": ("N_MAHINDRA", "NIFTY INDIA CORPORATE GROUP INDEX - MAHINDRA GROUP", "Thematic"),
    "tri - NIFTY MNC": ("NMNC", "NIFTY MNC", "Thematic"),
    "tri - Nifty Mobility": ("N_MOBILITY", "Nifty Mobility", "Thematic"),
    "tri - Nifty PSE": ("NPSE", "NIFTY PSE", "Thematic"),
    "tri - Nifty REITs InvITs": ("N_REIT", "Nifty REITs & InvITs", "Thematic"),
    "tri - Nifty Rural": ("N_RURAL", "Nifty Rural", "Thematic"),
    "tri - Nifty50 Shariah": ("N_SHARIAH25", "NIFTY SHARIAH 25", "Thematic"),
    "tri - Nifty Tata Group": ("N_TATA", "NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP", "Thematic"),
    "tri - NIFTY TATA 25 CAP": ("N_TATA_25", "NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP 25% CAP", "Thematic"),
    "tri - Nifty India Railways": ("N_RAIL", "Nifty India Railways PSU", "Thematic"),
    "tri - Nifty Corp MAATR": ("N_MAATR", "NIFTY INDIA SELECT 5 CORPORATE GROUPS (MAATR)", "Thematic"),
    "tri - Nifty New Consump": ("N_NEWCONS", "NIFTY INDIA NEW AGE CONSUMPTION", "Thematic"),
    "tri - Nifty Waves": ("N_WAVES", "Nifty Waves", "Thematic"),
    "tri - NIFTY 50 FUTURES TR INDEX": ("N50_FUT", "NIFTY 50 FUTURES TR INDEX", "Thematic"),
    "tri - Nifty500 Shariah": ("N500_SHARIAH", "Nifty500 Shariah", "Thematic"),
    "tri - NIFTY500 HEALTH": ("N500_HEALTH", "NIFTY500 HEALTH", "Thematic"),
    "tri - Nifty500 LMS Eql": ("N500_LMS_EQ", "Nifty500 LMS Eql", "Thematic"),
    "tri - NIFTY MULTI MFG": ("N_MULTI_MFG", "NIFTY MULTI MFG", "Thematic"),
    "tri - NIFTY MULTI INFRA": ("N_MULTI_INFRA", "NIFTY MULTI INFRA", "Thematic"),
    "tri - Nifty NonCyc Cons": ("N_NONCYC", "Nifty NonCyc Cons", "Thematic"),
    "tri - Nifty Conglomerate 50": ("N_CONGLOM", "Nifty Conglomerate 50", "Thematic"),
    "tri - Nifty AQL 30": ("NAQL30", "Nifty AQL 30", "Thematic"),
    "tri - Nifty MS Ind Cons": ("NMS_ICONS", "Nifty MS Ind Cons", "Thematic"),
}

# Load existing summary data
with open('data/summary_data.json', 'r') as f:
    summary_data = json.load(f)

# Create new mapped data
new_summary_data = {}
unmatched = []

for key, value in summary_data.items():
    if key in manual_mappings:
        short_name, full_name, category = manual_mappings[key]
        new_summary_data[short_name] = {
            'percentile': value,
            'full_name': full_name,
            'category': category
        }
    else:
        unmatched.append(key)

print(f"Total indices: {len(summary_data)}")
print(f"Matched indices: {len(new_summary_data)}")
print(f"Unmatched indices: {len(unmatched)}")

if unmatched:
    print("\nUnmatched:")
    for item in unmatched:
        print(f"  {item}")

# Save
with open('data/short_name_summary.json', 'w') as f:
    json.dump(new_summary_data, f, indent=2)

print("\n✓ Created data/short_name_summary.json")

# Print samples by category
print("\n=== SAMPLES BY CATEGORY ===")
for cat in ["Broad Market", "Sectoral", "Strategy", "Thematic"]:
    items = [(k, v) for k, v in new_summary_data.items() if v['category'] == cat]
    print(f"\n{cat}: {len(items)} indices")
    for short, data in sorted(items[:5]):
        print(f"  {short}: {data['percentile']:.4f} - {data['full_name']}")
