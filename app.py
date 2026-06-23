import streamlit as st
import pandas as pd
import re
import io

# ==========================================
# MASTER COUNTRY DICTIONARY
# ==========================================
COUNTRY_MAPPING = {
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
    'ZW': 'Zimbabwe - ZWE'
}

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def normalize_header(header_string):
    """Removes spaces, underscores, punctuation, makes lowercase for flexible matching."""
    return re.sub(r'[^a-zA-Z0-9]', '', str(header_string)).lower()

def map_country(val):
    """Maps Facebook ISO codes to target custom format."""
    if pd.isna(val) or str(val).strip() == '':
        return val
    val = str(val).strip().upper()
    return COUNTRY_MAPPING.get(val, val)

def clean_phone(val):
    """Strips all non-numeric characters."""
    if pd.isna(val):
        return val
    cleaned = re.sub(r'\D', '', str(val))
    return cleaned if cleaned else pd.NA

def load_data(uploaded_file):
    """Robustly load CSV data by reading bytes directly, avoiding file-seek errors."""
    import io
    
    # 1. Catch if the file drops out of memory
    if uploaded_file is None:
        raise ValueError("File lost from memory. Please re-attach the CSV.")
        
    # 2. Extract the raw byte data directly
    raw_bytes = uploaded_file.getvalue()
    
    try:
        # 3. First try reading as standard UTF-8
        text = raw_bytes.decode('utf-8')
        return pd.read_csv(io.StringIO(text), sep=None, engine='python', on_bad_lines='skip')
    except UnicodeDecodeError:
        # 4. If it's a Meta/Facebook format, it's often UTF-16. Fallback safely!
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
        elif norm == 'country': # Standard FB country field fallback
            renamed[col] = 'which region are you from?'
            
    df = df.rename(columns=renamed)
    
    # Ensure all columns exist
    for col in target_cols:
        if col not in df.columns:
            df[col] = pd.NA
            
    df = df[target_cols]
    
    # Text Processing
    skip_underscore = ['email', 'linkedin_profile_link']
    for col in df.columns:
        if col not in skip_underscore and df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: x.replace('_', ' ') if isinstance(x, str) else x)
            
    df['phone_number'] = df['phone_number'].apply(clean_phone)
    if 'created_time' in df.columns:
        df['created_time'] = df['created_time'].apply(lambda d: str(d).split('T')[0] if pd.notna(d) else d)
        df = df.sort_values(by='created_time', ascending=True)
        
    df['which region are you from?'] = df['which region are you from?'].apply(map_country)
    
    # Drop completely blank columns
    df = df.dropna(axis=1, how='all')
    return df

# ==========================================
# TASK 2: SF FORMAT
# ==========================================
def process_sf_format(df, event_name, platform_link):
    # Mapping FB headers -> SF Target Columns
    sf_mapping = {
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Attendee Email',
        'companyname': 'Company',
        'phonenumber': 'Phone',
        'workexperience': 'Work Experience',
        'yearsofworkexperience': 'Work Experience', # fallback FB string
        'whichmbaprogramareyouinterestedin': 'Interested Program',
        'whichregionareyoufrom': 'Country',
        'country': 'Country', # fallback FB string
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
    
    # Ensure all required columns exist before processing
    for col in final_order:
        if col not in df.columns:
            df[col] = pd.NA
            
    # Derive new columns
    df['Event'] = event_name
    df['Platform Link'] = platform_link
    df['Name on Badge'] = df['First Name'].fillna('') + ' ' + df['Last Name'].fillna('')
    df['Name on Badge'] = df['Name on Badge'].str.strip()
    
    # Underscore & Specific Text Logic
    skip_underscore = ['Attendee Email', 'Platform Link']
    for col in df.columns:
        if col not in skip_underscore and df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: str(x).replace('_', ' ') if pd.notna(x) else x)
            # Apply exact string match for part time MBA
            df[col] = df[col].apply(lambda x: str(x).replace('part time mba (bi-weekly mode)', 'part time mba ( bi-weekly mode)') if pd.notna(x) else x)

    # Phone Clean and Country Map
    df['Phone'] = df['Phone'].apply(clean_phone)
    df['Country'] = df['Country'].apply(map_country)
    
    # Enforce strict column order
    df = df[final_order]
    return df

# ==========================================
# STREAMLIT USER INTERFACE
# ==========================================
st.set_page_config(page_title="Meta Lead Converter", layout="centered")

st.title("📊 Meta Lead Data Processor")
st.write("Upload your raw Meta/Facebook CSV file, choose your processing task, and download the standardized output.")

# 1. Select the task
task = st.radio("Select Processing Mode:", ("Cleaning FB Lead Form", "Changing FB Lead Form to SF Format"))

# 2. Upload file
uploaded_file = st.file_uploader("Upload Raw Data CSV", type=['csv'])

# 3. Extra Inputs for Task 2
event_name = ""
platform_link = ""
if task == "Changing FB Lead Form to SF Format":
    st.markdown("### SF Format Required Fields")
    event_name = st.text_input("Event Name", placeholder="e.g., Summer MBA Fair 2026")
    platform_link = st.text_input("Platform Link", placeholder="https://zoom.us/j/12345...")

# 4. Processing Button
if st.button("Process Data"):
    if uploaded_file is None:
        st.warning("⚠️ Please upload a CSV file first.")
    elif task == "Changing FB Lead Form to SF Format" and (not event_name or not platform_link):
        st.warning("⚠️ Please fill in both the Event Name and Platform Link.")
    else:
        try:
            with st.spinner("Processing data..."):
                raw_df = load_data(uploaded_file)
                
                if task == "Cleaning FB Lead Form":
                    processed_df = process_cleaning_fb(raw_df)
                    file_name = "Cleaned_FB_Leads.csv"
                else:
                    processed_df = process_sf_format(raw_df, event_name, platform_link)
                    file_name = "SF_Formatted_Leads.csv"
                
                st.success("✅ Data processed successfully!")
                st.dataframe(processed_df.head(10)) # Show preview
                
                # Convert DF to CSV with UTF-8 BOM encoding for correct Excel rendering
                csv_data = processed_df.to_csv(index=False).encode('utf-8-sig')
                
                st.download_button(
                    label="📥 Download Output CSV",
                    data=csv_data,
                    file_name=file_name,
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"❌ An error occurred during processing: {e}")