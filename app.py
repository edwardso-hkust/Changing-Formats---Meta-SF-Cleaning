import streamlit as st
import pandas as pd
import re
import io

# ==========================================
# MASTER COUNTRY DICTIONARY (Codes & Full Names)
# ==========================================
MASTER_COUNTRY_MAPPING = {
    # 2-Letter ISO Codes
    'AD': 'Andorra - AND', 'AE': 'U.A.E. - ARE', 'AF': 'Afghanistan - AFG', 'AG': 'Antigua and Barbuda - ATG',
    'AI': 'Anguilla - AIA', 'AL': 'Albania - ALB', 'AM': 'Armenia - ARM', 'AO': 'Angola - AGO',
    'AQ': 'Antarctica - ATA', 'AR': 'Argentina - ARG', 'AS': 'American Samoa - ASM', 'AT': 'Austria - AUT',
    'AU': 'Australia - AUS', 'AW': 'Aruba - ABW', 'AX': 'Åland Islands - ALA', 'AZ': 'Azerbaijan - AZE',
    'BA': 'Bosnia - BIH', 'BB': 'Barbados - BRB', 'BD': 'Bangladesh - BGD', 'BE': 'Belgium - BEL',
    'BF': 'Burkina Faso - BFA', 'BG': 'Bulgaria - BGR', 'BH': 'Bahrain - BHR', 'BI': 'Burundi - BDI',
    'BJ': 'Benin - BEN', 'BL': 'Saint Barthélemy - BLM', 'BM': 'Bermuda - BMU', 'BN': 'Brunei - BRN',
    'BO': 'Bolivia - BOL', 'BR': 'Brazil - BRA', 'BS': 'Bahamas - BHS', 'BT': 'Bhutan - BTN',
    'BV': 'Bouvet Island - BVT', 'BW': 'Botswana - BWA', 'BY': 'Belarus - BLR', 'BZ': 'Belize - BLZ',
    'CA': 'Canada - CAN', 'CC': 'Cocos Islands - CCK', 'CD': 'Congo, Dem. Rep. - COD', 'CF': 'Central African Republic - CAF',
    'CG': 'Congo - COG', 'CH': 'Switzerland - CHE', 'CI': 'Ivory Coast - CIV', 'CK': 'Cook Islands - COK',
    'CL': 'Chile - CHL', 'CM': 'Cameroon - CMR', 'CN': 'Chinese Mainland - CHN', 'CO': 'Colombia - COL',
    'CR': 'Costa Rica - CRI', 'CV': 'Cape Verde - CPV', 'CW': 'Curaçao - ANT', 'CX': 'Christmas Island - CXR',
    'CY': 'Cyprus - CYP', 'CZ': 'Czech Republic - CZE', 'DE': 'Germany - DEU', 'DJ': 'Djibouti - DJI',
    'DK': 'Denmark - DNK', 'DM': 'Dominica - DMA', 'DO': 'Dominican Republic - DOM', 'DZ': 'Algeria - DZA',
    'EC': 'Ecuador - ECU', 'EE': 'Estonia - EST', 'EG': 'Egypt - EGY', 'EH': 'Western Sahara - ESH',
    'ER': 'Eritrea - ERI', 'ES': 'Spain - ESP', 'ET': 'Ethiopia - ETH', 'FI': 'Finland - FIN',
    'FJ': 'Fiji - FJI', 'FK': 'Falkland Islands (Malvinas) - FLK', 'FM': 'Micronesia, Fed. - FSM', 'FO': 'Faroe Islands - FRO',
    'FR': 'France - FRA', 'GA': 'Gabon - GAB', 'GB': 'United Kingdom - GBR', 'GD': 'Grenada - GRD',
    'GE': 'Georgia - GEO', 'GF': 'French Guiana - GUF', 'GG': 'Guernsey - GGY', 'GH': 'Ghana - GHA',
    'GI': 'Gibraltar - GIB', 'GL': 'Greenland - GRL', 'GM': 'Gambia - GMB', 'GN': 'Guinea - GIN',
    'GP': 'Guadeloupe - GLP', 'GQ': 'Equatorial Guinea - GNQ', 'GR': 'Greece - GRC', 'GS': 'South Georgia and the South Sandwich Islands - SGS',
    'GT': 'Guatemala - GTM', 'GU': 'Guam - GUM', 'GW': 'Guinea-Bissau - GNB', 'GY': 'Guyana - GUY',
    'HK': 'Hong Kong, China - HKG', 'HM': 'Heard Island - HMD', 'HN': 'Honduras - HND', 'HR': 'Croatia - HRV',
    'HT': 'Haiti - HTI', 'HU': 'Hungary - HUN', 'ID': 'Indonesia - IDN', 'IE': 'Ireland - IRL',
    'IL': 'Israel - ISR', 'IM': 'Isle of Man - IMN', 'IN': 'India - IND', 'IO': 'British Indian Ocean Territory - IOT',
    'IQ': 'Iraq - IRQ', 'IS': 'Iceland - ISL', 'IT': 'Italy - ITA', 'JE': 'Jersey - JEY',
    'JM': 'Jamaica - JAM', 'JO': 'Jordan - JOR', 'JP': 'Japan - JPN', 'KE': 'Kenya - KEN',
    'KG': 'Kyrgyzstan - KGZ', 'KH': 'Cambodia - KHM', 'KI': 'Kiribati - KIR', 'KM': 'Comoros - COM',
    'KN': 'Saint Kitts and Nevis - KNA', 'KR': 'Korea, Republic of - KOR', 'KW': 'Kuwait - KWT', 'KY': 'Cayman Islands - CYM',
    'KZ': 'Kazakhstan - KAZ', 'LA': 'Laos - LAO', 'LB': 'Lebanon - LBN', 'LC': 'Saint Lucia - LCA',
    'LI': 'Liechtenstein - LIE', 'LK': 'Sri Lanka - LKA', 'LR': 'Liberia - LBR', 'LS': 'Lesotho - LSO',
    'LT': 'Lithuania - LTU', 'LU': 'Luxembourg - LUX', 'LV': 'Latvia - LVA', 'LY': 'Libya - LBY',
    'MA': 'Morocco - MAR', 'MC': 'Monaco - MCO', 'MD': 'Moldova - MDA', 'ME': 'Montenegro - MNE',
    'MF': 'Saint Martin (French) - MAF', 'MG': 'Madagascar - MDG', 'MH': 'Marshall Islands - MHL', 'MK': 'Macedonia - MKD',
    'ML': 'Mali - MLI', 'MM': 'Myanmar - MMR', 'MN': 'Mongolia - MNG', 'MO': 'Macao - MAC',
    'MP': 'Northern Marianas - MNP', 'MQ': 'Martinique - MTQ', 'MR': 'Mauritania - MRT', 'MS': 'Montserrat - MSR',
    'MT': 'Malta - MLT', 'MU': 'Mauritius - MUS', 'MV': 'Maldives - MDV', 'MW': 'Malawi - MWI',
    'MX': 'Mexico - MEX', 'MY': 'Malaysia - MYS', 'MZ': 'Mozambique - MOZ', 'NA': 'Namibia - NAM',
    'NC': 'New Caledonia - NCL', 'NE': 'Niger - NER', 'NF': 'Norfolk Island - NFK', 'NG': 'Nigeria - NGA',
    'NI': 'Nicaragua - NIC', 'NL': 'Netherlands - NLD', 'NO': 'Norway - NOR', 'NP': 'Nepal - NPL',
    'NR': 'Nauru - NRU', 'NU': 'Niue - NIU', 'NZ': 'New Zealand - NZL', 'OM': 'Oman - OMN',
    'PA': 'Panama - PAN', 'PE': 'Peru - PER', 'PF': 'French Polynesia - PYF', 'PG': 'Papua New Guinea - PNG',
    'PH': 'Philippines - PHL', 'PK': 'Pakistan - PAK', 'PL': 'Poland - POL', 'PM': 'Saint Pierre and Miquelon - SPM',
    'PN': 'Pitcairn - PCN', 'PR': 'Puerto Rico - PRI', 'PS': 'Palestinian Terr. - PSE', 'PT': 'Portugal - PRT',
    'PW': 'Palau - PLW', 'PY': 'Paraguay - PRY', 'QA': 'Qatar - QAT', 'RE': 'Réunion - REU',
    'RO': 'Romania - ROU', 'RS': 'Serbia - SRB', 'RU': 'Russia - RUS', 'RW': 'Rwanda - RWA',
    'SA': 'Saudi Arabia - SAU', 'SB': 'Solomon Islands - SLB', 'SC': 'Seychelles - SYC', 'SE': 'Sweden - SWE',
    'SG': 'Singapore - SGP', 'SH': 'Saint Helena - SHN', 'SI': 'Slovenia - SVN', 'SJ': 'Svalbard - SJM',
    'SK': 'Slovakia - SVK', 'SL': 'Sierra Leone - SLE', 'SM': 'San Marino - SMR', 'SN': 'Senegal - SEN',
    'SO': 'Somalia - SOM', 'SR': 'Suriname - SUR', 'SS': 'South Sudan - SDN', 'ST': 'Sao Tome & Principe - STP',
    'SV': 'El Salvador - SLV', 'SX': 'Sint Maarten (Dutch) - ANT', 'SZ': 'Swaziland - SWZ', 'TC': 'Turks and Caicos - TCA',
    'TD': 'Chad - TCD', 'TF': 'French Southern Territories - ATF', 'TG': 'Togo - TGO', 'TH': 'Thailand - THA',
    'TJ': 'Tajikistan - TJK', 'TK': 'Tokelau - TKL', 'TL': 'Timor-Leste - TLS', 'TM': 'Turkmenistan - TKM',
    'TN': 'Tunisia - TUN', 'TO': 'Tonga - TON', 'TR': 'Turkey - TUR', 'TT': 'Trinidad and Tobago - TTO',
    'TV': 'Tuvalu - TUV', 'TW': 'Taiwan - TWN', 'TZ': 'Tanzania - TZA', 'UA': 'Ukraine - UKR',
    'UG': 'Uganda - UGA', 'UM': 'United States Minor Outlying Islands - UMI', 'US': 'United States - USA',
    'UY': 'Uruguay - URY', 'UZ': 'Uzbekistan - UZB', 'VA': 'Vatican City - VAT', 'VC': 'Saint Vincent - VCT',
    'VE': 'Venezuela - VEN', 'VG': 'Virgin Islands, British - VGB', 'VI': 'Virgin Islands, U.S. - VIR',
    'VN': 'Vietnam - VNM', 'VU': 'Vanuatu - VUT', 'WF': 'Wallis and Futuna - WLF', 'WS': 'Samoa - WSM',
    'YE': 'Yemen - YEM', 'YT': 'Mayotte - MYT', 'ZA': 'South Africa - ZAF', 'ZM': 'Zambia - ZMB',
    'ZW': 'Zimbabwe - ZWE',
    
    # Full Names / Extended Variations (Uppercase)
    'AALAND ISLANDS': 'Åland Islands - ALA', 'AFGHANISTAN': 'Afghanistan - AFG', 'ALBANIA': 'Albania - ALB',
    'ALGERIA': 'Algeria - DZA', 'AMERICAN SAMOA': 'American Samoa - ASM', 'ANDORRA': 'Andorra - AND',
    'ANGOLA': 'Angola - AGO', 'ANGUILLA': 'Anguilla - AIA', 'ANTARCTICA': 'Antarctica - ATA',
    'ANTIGUA AND BARBUDA': 'Antigua and Barbuda - ATG', 'ARGENTINA': 'Argentina - ARG', 'ARMENIA': 'Armenia - ARM',
    'ARUBA': 'Aruba - ABW', 'AUSTRALIA': 'Australia - AUS', 'AUSTRIA': 'Austria - AUT', 'AZERBAIJAN': 'Azerbaijan - AZE',
    'BAHAMAS': 'Bahamas - BHS', 'BAHRAIN': 'Bahrain - BHR', 'BANGLADESH': 'Bangladesh - BGD', 'BARBADOS': 'Barbados - BRB',
    'BELARUS': 'Belarus - BLR', 'BELGIUM': 'Belgium - BEL', 'BELIZE': 'Belize - BLZ', 'BENIN': 'Benin - BEN',
    'BERMUDA': 'Bermuda - BMU', 'BHUTAN': 'Bhutan - BTN', 'BOLIVIA': 'Bolivia - BOL', 'BOSNIA': 'Bosnia - BIH',
    'BOTSWANA': 'Botswana - BWA', 'BOUVET ISLAND': 'Bouvet Island - BVT', 'BRAZIL': 'Brazil - BRA',
    'BRITISH INDIAN OCEAN TERRITORY': 'British Indian Ocean Territory - IOT', 'BRUNEI': 'Brunei - BRN',
    'BULGARIA': 'Bulgaria - BGR', 'BURKINA FASO': 'Burkina Faso - BFA', 'BURUNDI': 'Burundi - BDI',
    'CAMBODIA': 'Cambodia - KHM', 'CAMEROON': 'Cameroon - CMR', 'CANADA': 'Canada - CAN', 'CAPE VERDE': 'Cape Verde - CPV',
    'CAYMAN ISLANDS': 'Cayman Islands - CYM', 'CENTRAL AFRICAN REPUBLIC': 'Central African Republic - CAF',
    'CHAD': 'Chad - TCD', 'CHILE': 'Chile - CHL', 'CHINA': 'Chinese Mainland - CHN',
    'CHRISTMAS ISLAND': 'Christmas Island - CXR', 'COCOS (KEELING) ISLANDS': 'Cocos Islands - CCK',
    'COLOMBIA': 'Colombia - COL', 'COMOROS': 'Comoros - COM', 'CONGO, DEM. REP.': 'Congo, Dem. Rep. - COD',
    'CONGO': 'Congo - COG', 'COOK ISLANDS': 'Cook Islands - COK', 'COSTA RICA': 'Costa Rica - CRI',
    'CROATIA': 'Croatia - HRV', 'CUBA': 'Cuba - CUB', 'CURAÇAO': 'Curaçao - ANT', 'CYPRUS': 'Cyprus - CYP',
    'CZECH REPUBLIC': 'Czech Republic - CZE', 'DENMARK': 'Denmark - DNK', 'DJIBOUTI': 'Djibouti - DJI',
    'DOMINICA': 'Dominica - DMA', 'DOMINICAN REPUBLIC': 'Dominican Republic - DOM', 'ECUADOR': 'Ecuador - ECU',
    'EGYPT': 'Egypt - EGY', 'EL SALVADOR': 'El Salvador - SLV', 'EQUATORIAL GUINEA': 'Equatorial Guinea - GNQ',
    'ERITREA': 'Eritrea - ERI', 'ESTONIA': 'Estonia - EST', 'ETHIOPIA': 'Ethiopia - ETH',
    'FALKLAND ISLANDS (MALVINAS)': 'Falkland Islands (Malvinas) - FLK', 'FAROE ISLANDS': 'Faroe Islands - FRO',
    'FIJI': 'Fiji - FJI', 'FINLAND': 'Finland - FIN', 'FRANCE': 'France - FRA', 'FRENCH GUIANA': 'French Guiana - GUF',
    'FRENCH POLYNESIA': 'French Polynesia - PYF', 'FRENCH SOUTHERN TERRITORIES': 'French Southern Territories - ATF',
    'GABON': 'Gabon - GAB', 'GAMBIA': 'Gambia - GMB', 'GEORGIA': 'Georgia - GEO', 'GERMANY': 'Germany - DEU',
    'GHANA': 'Ghana - GHA', 'GIBRALTAR': 'Gibraltar - GIB', 'GREECE': 'Greece - GRC', 'GREENLAND': 'Greenland - GRL',
    'GRENADA': 'Grenada - GRD', 'GUADELOUPE': 'Guadeloupe - GLP', 'GUAM': 'Guam - GUM', 'GUATEMALA': 'Guatemala - GTM',
    'GUERNSEY': 'Guernsey - GGY', 'GUINEA-BISSAU': 'Guinea-Bissau - GNB', 'GUINEA': 'Guinea - GIN', 'GUYANA': 'Guyana - GUY',
    'HAITI': 'Haiti - HTI', 'HEARD ISLAND': 'Heard Island - HMD', 'HONDURAS': 'Honduras - HND',
    'HONG KONG': 'Hong Kong, China - HKG', 'HONG KONG SAR': 'Hong Kong, China - HKG', 'HUNGARY': 'Hungary - HUN',
    'ICELAND': 'Iceland - ISL', 'INDIA': 'India - IND', 'INDONESIA': 'Indonesia - IDN', 'IRAN': 'Iran - IRN',
    'IRAQ': 'Iraq - IRQ', 'IRELAND': 'Ireland - IRL', 'ISLE OF MAN': 'Isle of Man - IMN', 'ISRAEL': 'Israel - ISR',
    'ITALY': 'Italy - ITA', 'IVORY COAST': 'Ivory Coast - CIV', 'JAMAICA': 'Jamaica - JAM', 'JAPAN': 'Japan - JPN',
    'JERSEY (CHANNEL ISLANDS)': 'Jersey - JEY', 'JORDAN': 'Jordan - JOR', 'KAZAKHSTAN': 'Kazakhstan - KAZ',
    'KENYA': 'Kenya - KEN', 'KIRIBATI': 'Kiribati - KIR', "KOREA, DEMO PEOPLE'S REP OF": "Korea, Demo People's Rep of - PRK",
    'KOREA, REPUBLIC OF': 'Korea, Republic of - KOR', 'SOUTH KOREA': 'Korea, Republic of - KOR', 'KUWAIT': 'Kuwait - KWT',
    'KYRGYZSTAN': 'Kyrgyzstan - KGZ', 'LAOS': 'Laos - LAO', 'LATVIA': 'Latvia - LVA', 'LEBANON': 'Lebanon - LBN',
    'LESOTHO': 'Lesotho - LSO', 'LIBERIA': 'Liberia - LBR', 'LIBYA': 'Libya - LBY', 'LIECHTENSTEIN': 'Liechtenstein - LIE',
    'LITHUANIA': 'Lithuania - LTU', 'LUXEMBOURG': 'Luxembourg - LUX', 'MACAO': 'Macao - MAC', 'MACAU': 'Macao - MAC',
    'MACEDONIA': 'Macedonia - MKD', 'MADAGASCAR': 'Madagascar - MDG', 'MALAWI': 'Malawi - MWI', 'MALAYSIA': 'Malaysia - MYS',
    'MALDIVES': 'Maldives - MDV', 'MALI': 'Mali - MLI', 'MALTA': 'Malta - MLT', 'MARSHALL ISLANDS': 'Marshall Islands - MHL',
    'MARTINIQUE': 'Martinique - MTQ', 'MAURITANIA': 'Mauritania - MRT', 'MAURITIUS': 'Mauritius - MUS',
    'MAYOTTE': 'Mayotte - MYT', 'MEXICO': 'Mexico - MEX', 'MICRONESIA, FED.': 'Micronesia, Fed. - FSM',
    'MOLDOVA': 'Moldova - MDA', 'MONACO': 'Monaco - MCO', 'MONGOLIA': 'Mongolia - MNG', 'MONTENEGRO': 'Montenegro - MNE',
    'MONTSERRAT': 'Montserrat - MSR', 'MOROCCO': 'Morocco - MAR', 'MOZAMBIQUE': 'Mozambique - MOZ',
    'MYANMAR': 'Myanmar - MMR', 'NAMIBIA': 'Namibia - NAM', 'NAURU': 'Nauru - NRU', 'NEPAL': 'Nepal - NPL',
    'NETHERLANDS': 'Netherlands - NLD', 'NEW CALEDONIA': 'New Caledonia - NCL', 'NEW ZEALAND': 'New Zealand - NZL',
    'NICARAGUA': 'Nicaragua - NIC', 'NIGERIA': 'Nigeria - NGA', 'NIGER': 'Niger - NER', 'NIUE': 'Niue - NIU',
    'NORFOLK ISLAND': 'Norfolk Island - NFK', 'NORTHERN MARIANAS': 'Northern Marianas - MNP', 'NORWAY': 'Norway - NOR',
    'OMAN': 'Oman - OMN', 'PAKISTAN': 'Pakistan - PAK', 'PALAU': 'Palau - PLW', 'PALESTINIAN TERR.': 'Palestinian Terr. - PSE',
    'PANAMA': 'Panama - PAN', 'PAPUA NEW GUINEA': 'Papua New Guinea - PNG', 'PARAGUAY': 'Paraguay - PRY',
    'PERU': 'Peru - PER', 'PHILIPPINES': 'Philippines - PHL', 'PITCAIRN': 'Pitcairn - PCN', 'POLAND': 'Poland - POL',
    'PORTUGAL': 'Portugal - PRT', 'PUERTO RICO': 'Puerto Rico - PRI', 'QATAR': 'Qatar - QAT', 'RÉUNION': 'Réunion - REU',
    'REUNION': 'Réunion - REU', 'ROMANIA': 'Romania - ROU', 'RUSSIA': 'Russia - RUS', 'RWANDA': 'Rwanda - RWA',
    'SAINT BARTHÉLEMY': 'Saint Barthélemy - BLM', 'SAINT HELENA': 'Saint Helena - SHN',
    'SAINT KITTS AND NEVIS': 'Saint Kitts and Nevis - KNA', 'SAINT LUCIA': 'Saint Lucia - LCA',
    'SAINT MARTIN (FRENCH)': 'Saint Martin (French) - MAF', 'SAINT PIERRE AND MIQUELON': 'Saint Pierre and Miquelon - SPM',
    'SAINT VINCENT': 'Saint Vincent - VCT', 'SAMOA': 'Samoa - WSM', 'SAN MARINO': 'San Marino - SMR',
    'SAO TOME & PRINCIPE': 'Sao Tome & Principe - STP', 'SAUDI ARABIA': 'Saudi Arabia - SAU', 'SENEGAL': 'Senegal - SEN',
    'SERBIA': 'Serbia - SRB', 'SEYCHELLES': 'Seychelles - SYC', 'SIERRA LEONE': 'Sierra Leone - SLE',
    'SINGAPORE': 'Singapore - SGP', 'SINT MAARTEN (DUTCH)': 'Sint Maarten (Dutch) - ANT', 'SLOVAKIA': 'Slovakia - SVK',
    'SLOVENIA': 'Slovenia - SVN', 'SOLOMON ISLANDS': 'Solomon Islands - SLB', 'SOMALIA': 'Somalia - SOM',
    'SOUTH AFRICA': 'South Africa - ZAF', 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS': 'South Georgia and the South Sandwich Islands - SGS',
    'SOUTH SUDAN': 'South Sudan - SDN', 'SPAIN': 'Spain - ESP', 'SRI LANKA': 'Sri Lanka - LKA', 'SUDAN': 'Sudan - SDN',
    'SURINAME': 'Suriname - SUR', 'SVALBARD': 'Svalbard - SJM', 'SWAZILAND': 'Swaziland - SWZ', 'SWEDEN': 'Sweden - SWE',
    'SWITZERLAND': 'Switzerland - CHE', 'SYRIA': 'Syria - SYR', 'TAIWAN': 'Taiwan - TWN', 'TAJIKISTAN': 'Tajikistan - TJK',
    'TANZANIA': 'Tanzania - TZA', 'THAILAND': 'Thailand - THA', 'TIMOR-LESTE': 'Timor-Leste - TLS', 'TOGO': 'Togo - TGO',
    'TOKELAU': 'Tokelau - TKL', 'TONGA': 'Tonga - TON', 'TRINIDAD AND TOBAGO': 'Trinidad and Tobago - TTO',
    'TUNISIA': 'Tunisia - TUN', 'TURKEY': 'Turkey - TUR', 'TURKMENISTAN': 'Turkmenistan - TKM',
    'TURKS AND CAICOS': 'Turks and Caicos - TCA', 'TUVALU': 'Tuvalu - TUV', 'U.A.E.': 'U.A.E. - ARE',
    'UNITED ARAB EMIRATES': 'U.A.E. - ARE', 'UGANDA': 'Uganda - UGA', 'UKRAINE': 'Ukraine - UKR',
    'UNITED KINGDOM': 'United Kingdom - GBR', 'UNITED STATES MINOR OUTLYING ISLANDS': 'United States Minor Outlying Islands - UMI',
    'UNITED STATES': 'United States - USA', 'URUGUAY': 'Uruguay - URY', 'UZBEKISTAN': 'Uzbekistan - UZB',
    'VANUATU': 'Vanuatu - VUT', 'VATICAN CITY': 'Vatican City - VAT', 'VENEZUELA': 'Venezuela - VEN',
    'VIET NAM': 'Vietnam - VNM', 'VIETNAM': 'Vietnam - VNM', 'VIRGIN ISLANDS, BRITISH': 'Virgin Islands, British - VGB',
    'VIRGIN ISLANDS, U.S.': 'Virgin Islands, U.S. - VIR', 'WALLIS AND FUTUNA': 'Wallis and Futuna - WLF',
    'WESTERN SAHARA': 'Western Sahara - ESH', 'YEMEN': 'Yemen - YEM', 'ZAMBIA': 'Zambia - ZMB', 'ZIMBABWE': 'Zimbabwe - ZWE'
}

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def normalize_header(header_string):
    """Removes spaces, underscores, punctuation, makes lowercase for flexible matching."""
    return re.sub(r'[^a-zA-Z0-9]', '', str(header_string)).lower()

def map_country(val):
    """Maps Facebook fields to target format, with aggressive fallback logic."""
    if pd.isna(val) or str(val).strip() == '':
        return val
        
    # 1. Clean the string: uppercase, fix underscores and weird dashes
    val_clean = str(val).upper().replace('_', ' ').replace('–', '-').strip()
    
    # 2. Check for an exact 2-letter code or Full Name match
    if val_clean in MASTER_COUNTRY_MAPPING:
        return MASTER_COUNTRY_MAPPING[val_clean]
        
    # 3. SNAP-BACK FORMATTING: If it already looks like "MALAYSIA - MYS" but has bad capitalization
    valid_outputs = {v.upper(): v for v in MASTER_COUNTRY_MAPPING.values()}
    if val_clean in valid_outputs:
        return valid_outputs[val_clean]
        
    # 4. SMART OVERRIDES: Catch messy Facebook formats by checking for keywords
    if 'HONG KONG' in val_clean:
        return 'Hong Kong, China - HKG'
    if 'MACAO' in val_clean or 'MACAU' in val_clean:
        return 'Macao - MAC'
    if 'TAIWAN' in val_clean:
        return 'Taiwan - TWN'
    if 'KOREA' in val_clean and 'SOUTH' in val_clean:
        return 'Korea, Republic of - KOR'
        
    # 5. Fallback 1: Extract 2-letter OR 3-letter code after a dash
    if '-' in val_clean:
        parts = val_clean.split('-')
        potential_code = parts[-1].strip()
        
        # Check if it's a 2-letter code
        if len(potential_code) == 2 and potential_code in MASTER_COUNTRY_MAPPING:
            return MASTER_COUNTRY_MAPPING[potential_code]
            
        # Check if it's a 3-letter code (like MYS or GBR)
        if len(potential_code) == 3:
            for clean_out, proper_out in valid_outputs.items():
                if clean_out.endswith(f"- {potential_code}"):
                    return proper_out
                    
    # 6. Fallback 2: If no map is found at all, return the string with spaces
    return str(val).replace('_', ' ').strip()
    
def clean_phone(val):
    """Strips all non-numeric characters."""
    if pd.isna(val):
        return val
    cleaned = re.sub(r'\D', '', str(val))
    return cleaned if cleaned else pd.NA

def load_data(uploaded_file):
    """Robustly load CSV data by reading bytes directly, avoiding file-seek errors."""
    if uploaded_file is None:
        raise ValueError("File lost from memory. Please re-attach the CSV.")
        
    raw_bytes = uploaded_file.getvalue()
    
    try:
        text = raw_bytes.decode('utf-8')
        return pd.read_csv(io.StringIO(text), sep=None, engine='python', on_bad_lines='skip')
    except UnicodeDecodeError:
        text = raw_bytes.decode('utf-16')
        return pd.read_csv(io.StringIO(text), sep=None, engine='python', on_bad_lines='skip')

# ==========================================
# TASK 1: CLEANING FB LEAD FORM
# ==========================================
def process_cleaning_fb(df):
    target_cols = [
        'created_time', 'form_name', 'first_name', 'last_name', 'email',
        'phone_number', 'work experience', 'job_title', 'company_name',
        'i would like to talk to a mba advisor', 'which region are you from?',
        'which mba program are you interested in?', 'linkedin_profile_link'
    ]
    mapping = {normalize_header(c): c for c in target_cols}
    
    renamed = {}
    for col in df.columns:
        norm = normalize_header(col)
        if norm in mapping:
            renamed[col] = mapping[norm]
        elif norm == 'country': 
            renamed[col] = 'which region are you from?'
            
    df = df.rename(columns=renamed)
    
    for col in target_cols:
        if col not in df.columns:
            df[col] = pd.NA
            
    df = df[target_cols]
    
    # Text Processing - Force underscore replace on all except protected columns
    skip_underscore = ['email', 'linkedin_profile_link']
    for col in df.columns:
        if col not in skip_underscore:
            df[col] = df[col].apply(lambda x: str(x).replace('_', ' ') if pd.notna(x) else x)
            
    # Phone numbers: Pure digits
    df['phone_number'] = df['phone_number'].apply(clean_phone)
    
    # Date: Strip time (keep only part before 'T')
    if 'created_time' in df.columns:
        df['created_time'] = df['created_time'].apply(lambda d: str(d).split('T')[0] if pd.notna(d) else d)
        
    df['which region are you from?'] = df['which region are you from?'].apply(map_country)
    df = df.dropna(axis=1, how='all')
    return df

# ==========================================
# TASK 2: SF FORMAT
# ==========================================
def process_sf_format(df, event_name, platform_link):
    sf_mapping = {
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Attendee Email',
        'companyname': 'Company',
        'phonenumber': 'Phone',
        'workexperience': 'Work Experience',
        'yearsofworkexperience': 'Work Experience',
        'whichmbaprogramareyouinterestedin': 'Interested Program',
        'whichregionareyoufrom': 'Country',
        'country': 'Country', 
        'jobtitle': 'Title on Badge',
        'iwouldliketotalktoambaadvisor': 'Interested in Consultation'
    }
    
    renamed = {}
    for col in df.columns:
        norm = normalize_header(col)
        if norm in sf_mapping:
            renamed[col] = sf_mapping[norm]
            
    df = df.rename(columns=renamed)
    
    final_order = [
        'First Name', 'Last Name', 'Attendee Email', 'Company', 'Phone',
        'Work Experience', 'Platform Link', 'Interested Program', 'Country',
        'Title on Badge', 'Interested in Consultation', 'Event', 'Name on Badge'
    ]
    
    for col in final_order:
        if col not in df.columns:
            df[col] = pd.NA
            
    df['Event'] = event_name
    df['Platform Link'] = platform_link
    df['Name on Badge'] = df['First Name'].fillna('') + ' ' + df['Last Name'].fillna('')
    df['Name on Badge'] = df['Name on Badge'].str.strip()
    
    # Text Processing - Force underscore replace on all except protected columns
    skip_underscore = ['Attendee Email', 'Platform Link']
    for col in df.columns:
        if col not in skip_underscore:
            df[col] = df[col].apply(lambda x: str(x).replace('_', ' ') if pd.notna(x) else x)
            # Re-apply the part-time MBA rule
            df[col] = df[col].apply(lambda x: str(x).replace('part time mba (bi-weekly mode)', 'part time mba ( bi-weekly mode)') if pd.notna(x) else x)

    # Phone numbers: Pure digits
    df['Phone'] = df['Phone'].apply(clean_phone)
    
    # Apply Country mapping
    df['Country'] = df['Country'].apply(map_country)
    
    df = df[final_order]
    return df

# ==========================================
# STREAMLIT USER INTERFACE
# ==========================================
st.set_page_config(page_title="Meta Lead Converter", layout="centered")

st.title("📊 Meta Lead Data Processor")
st.write("Upload your raw Meta/Facebook CSV file(s), choose your processing task, and download the standardized output.")

task = st.radio("Select Processing Mode:", ("Cleaning FB Lead Form", "Changing FB Lead Form to SF Format"))

# UPDATED: accept_multiple_files=True added here
uploaded_files = st.file_uploader("Upload Raw Data CSV(s)", type=['csv'], accept_multiple_files=True)

event_name = ""
platform_link = ""
if task == "Changing FB Lead Form to SF Format":
    st.markdown("### SF Format Required Fields")
    event_name = st.text_input("Event Name", placeholder="e.g., Summer MBA Fair 2026")
    platform_link = st.text_input("Platform Link", placeholder="https://zoom.us/j/12345...")

if st.button("Process Data"):
    # UPDATED: Checking if the list is empty
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one CSV file first.")
    elif task == "Changing FB Lead Form to SF Format" and (not event_name or not platform_link):
        st.warning("⚠️ Please fill in both the Event Name and Platform Link.")
    else:
        try:
            with st.spinner(f"Processing {len(uploaded_files)} file(s)..."):
                
                # UPDATED: Loop through all files and store the processed dataframes in a list
                processed_dfs = []
                for file in uploaded_files:
                    raw_df = load_data(file)
                    
                    if task == "Cleaning FB Lead Form":
                        processed_df = process_cleaning_fb(raw_df)
                    else:
                        processed_df = process_sf_format(raw_df, event_name, platform_link)
                        
                    processed_dfs.append(processed_df)
                
                # UPDATED: Combine all processed files into one master dataframe
                master_df = pd.concat(processed_dfs, ignore_index=True)
                
                # Optional sorting for task 1 (since we combined multiple files)
                if task == "Cleaning FB Lead Form" and 'created_time' in master_df.columns:
                     master_df = master_df.sort_values(by='created_time', ascending=True)

                file_name = "Cleaned_FB_Leads_Combined.csv" if task == "Cleaning FB Lead Form" else "SF_Formatted_Leads_Combined.csv"
                
                st.success("✅ Data combined and processed successfully!")
                st.dataframe(master_df.head(10)) 
                
                csv_data = master_df.to_csv(index=False).encode('utf-8-sig')
                
                st.download_button(
                    label=f"📥 Download Combined Output CSV ({len(uploaded_files)} files)",
                    data=csv_data,
                    file_name=file_name,
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"❌ An error occurred during processing: {e}")
