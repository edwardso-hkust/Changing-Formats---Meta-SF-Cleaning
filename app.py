import streamlit as st
import pandas as pd
import re
import io

# ==========================================
# MASTER COUNTRY DICTIONARY (Codes & Full Names)
# ==========================================
MASTER_COUNTRY_MAPPING = {
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
    'VN': 'Vietnam - VNM', 'VIETNAM': 'Vietnam - VNM', 'VIRGIN ISLANDS, BRITISH': 'Virgin Islands, British - VGB',
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
        
    val_clean = str(val).upper().replace('_', ' ').replace('–', '-').strip()
    
    if val_clean in MASTER_COUNTRY_MAPPING:
        return MASTER_COUNTRY_MAPPING[val_clean]
        
    valid_outputs = {v.upper(): v for v in MASTER_COUNTRY_MAPPING.values()}
    if val_clean in valid_outputs:
        return valid_outputs[val_clean]
        
    if 'HONG KONG' in val_clean:
        return 'Hong Kong, China - HKG'
    if 'MACAO' in val_clean or 'MACAU' in val_clean:
        return 'Macao - MAC'
    if 'TAIWAN' in val_clean:
        return 'Taiwan - TWN'
    if 'KOREA' in val_clean and 'SOUTH' in val_clean:
        return 'Korea, Republic of - KOR'
        
    if '-' in val_clean:
        parts = val_clean.split('-')
        potential_code = parts[-1].strip()
        
        if len(potential_code) == 2 and potential_code in MASTER_COUNTRY_MAPPING:
            return MASTER_COUNTRY_MAPPING[potential_code]
            
        if len(potential_code) == 3:
            for clean_out, proper_out in valid_outputs.items():
                if clean_out.endswith(f"- {potential_code}"):
                    return proper_out
                    
    return 'Others'
    
def clean_phone(val):
    """Strips all non-numeric characters and returns a pure string of digits."""
    if pd.isna(val) or str(val).strip() == '':
        return pd.NA
    cleaned = re.sub(r'\D', '', str(val))
    return cleaned if cleaned else pd.NA

def clean_job_title(val):
    """Extracts a plausible job title by removing conversational words/company names and safely caps at 80 chars."""
    if pd.isna(val):
        return 'N/A'
    title = str(val).strip()
    
    if title.lower() in ['', 'na', 'n/a', 'nan', 'none', '-', '.']:
        return 'N/A'
        
    filler_patterns = [
        r'(?i)^i am (a|an)\s+',
        r'(?i)^currently (working as )?(a|an)?\s*',
        r'(?i)^working as (a|an)?\s*',
        r'(?i)^my (role|title) is\s+',
        r'(?i)^(role|title):\s*'
    ]
    for pattern in filler_patterns:
        title = re.sub(pattern, '', title).strip()
        
    split_delimiters = [r'(?i)\s+at\s+', r'\s*@\s*', r'\s*\|\s*', r'\s*\(']
    for delim in split_delimiters:
        parts = re.split(delim, title)
        if len(parts) > 1 and len(parts[0].strip()) > 0:
            title = parts[0].strip()
            break
            
    if len(title) > 80:
        truncated = title[:80]
        if ' ' in truncated:
            title = truncated.rsplit(' ', 1)[0]
        else:
            title = truncated
            
    return title.strip() if title.strip() else 'N/A'

def load_data(uploaded_file):
    """Robustly load CSV data, forcing all columns to be read as plain text."""
    if uploaded_file is None:
        raise ValueError("File lost from memory. Please re-attach the CSV.")
        
    raw_bytes = uploaded_file.getvalue()
    
    try:
        text = raw_bytes.decode('utf-8')
        return pd.read_csv(io.StringIO(text), sep=None, engine='python', on_bad_lines='skip', dtype=str)
    except UnicodeDecodeError:
        text = raw_bytes.decode('utf-16')
        return pd.read_csv(io.StringIO(text), sep=None, engine='python', on_bad_lines='skip', dtype=str)

# ==========================================
# TASK 1: CLEANING FB LEAD FORM
# ==========================================
def process_cleaning_fb(df):
    target_cols = [
        'created_time', 'form_name', 'first_name', 'last_name', 'email',
        'phone_number', 'work experience', 'job_title', 'company_name',
        'which region are you from?', 'linkedin_profile_link'
    ]
    
    mapping = {normalize_header(c): c for c in target_cols}
    
    renamed = {}
    for col in df.columns:
        norm = normalize_header(col)
        if norm in mapping:
            renamed[col] = mapping[norm]
        elif norm == 'country': 
            renamed[col] = 'which region are you from?'
        elif norm == 'yearsofworkexperience':
            renamed[col] = 'work experience'
            
    df = df.rename(columns=renamed)
    df = df.loc[:, ~df.columns.duplicated(keep='first')].copy()
    
    for col in target_cols:
        if col not in df.columns:
            df[col] = pd.NA
            
    df = df[target_cols]
    
    skip_underscore = ['email', 'linkedin_profile_link']
    for col in df.columns:
        if col not in skip_underscore:
            df[col] = df[col].apply(lambda x: str(x).replace('_', ' ') if pd.notna(x) else x)
            
    df['phone_number'] = df['phone_number'].apply(clean_phone)
    if 'created_time' in df.columns:
        df['created_time'] = df['created_time'].apply(lambda d: str(d).split('T')[0] if pd.notna(d) else d)
        
    df['which region are you from?'] = df['which region are you from?'].apply(map_country)
    return df

# ==========================================
# TASK 2: SF FORMAT
# ==========================================
def process_sf_format(df, event_name, platform_link):
    sf_mapping = {
        'firstname': 'First Name', 'lastname': 'Last Name', 'email': 'Attendee Email',
        'companyname': 'Company', 'phonenumber': 'Phone', 'workexperience': 'Work Experience',
        'yearsofworkexperience': 'Work Experience', 'whichregionareyoufrom': 'Country',
        'country': 'Country', 'jobtitle': 'Title on Badge'
    }
    
    renamed = {}
    for col in df.columns:
        norm = normalize_header(col)
        if norm in sf_mapping:
            renamed[col] = sf_mapping[norm]
            
    df = df.rename(columns=renamed)
    df = df.loc[:, ~df.columns.duplicated(keep='first')].copy()
    
    final_order = [
        'First Name', 'Last Name', 'Attendee Email', 'Company', 'Phone',
        'Work Experience', 'Platform Link', 'Country', 'Title on Badge', 'Event', 'Name on Badge'
    ]
    
    for col in final_order:
        if col not in df.columns:
            df[col] = pd.NA
            
    df['Event'] = event_name
    df['Platform Link'] = platform_link
    df['Name on Badge'] = df['First Name'].fillna('') + ' ' + df['Last Name'].fillna('')
    df['Name on Badge'] = df['Name on Badge'].str.strip()
    
    skip_underscore = ['Attendee Email', 'Platform Link']
    for col in df.columns:
        if col not in skip_underscore:
            df[col] = df[col].apply(lambda x: str(x).replace('_', ' ') if pd.notna(x) else x)
            df[col] = df[col].apply(lambda x: str(x).replace('part time mba (bi-weekly mode)', 'part time mba ( bi-weekly mode)') if pd.notna(x) else x)

    df['Title on Badge'] = df['Title on Badge'].apply(clean_job_title)
    df['Company'] = df['Company'].apply(
        lambda x: 'N/A' if pd.isna(x) or str(x).strip().lower() in ['', 'na', 'n/a', 'nan', 'none', '-', '.'] 
        else str(x).strip()
    )
    df['Phone'] = df['Phone'].apply(clean_phone)
    df['Country'] = df['Country'].apply(map_country)
    
    df = df[final_order]
    return df

# ==========================================
# TASK 3: SLEEKFLOW FORMAT (New Feature)
# ==========================================
def process_sleekflow_format(uploaded_file, label_value):
    """
    Extracts, formats, and exports attendee information from Excel or CSV files 
    by automatically detecting headers.
    """
    mapping_rules = {
        "FirstName": ["first_name", "first name", "given name", "fname"],
        "LastName": ["last_name", "last name", "surname", "lname"],
        "Email": ["email", "attendee email", "e-mail", "mail", "email address"],
        "PhoneNumber": ["phone_number", "phone", "mobile", "tel", "contact number", "mobile number"],
        "CompanyName": ["company_name", "company", "attendee company", "organization", "employer"],
        "JobTitle": ["job_title", "job title", "title on badge", "designation", "position"],
        "Work Experience": ["work experience", "years of experience", "exp", "total experience"],
        "Interested Program": ["which mba program are you interested in?", "interested program", "program", "intended program"],
        "Country": ["which region are you from?", "country", "region", "location", "nationality"]
    }
    final_columns = ["FirstName", "LastName", "Label", "Email", "PhoneNumber", "CompanyName", "JobTitle", "Work Experience", "Interested Program", "Country"]
    processed_dfs = []

    file_name = uploaded_file.name.lower()
    raw_bytes = uploaded_file.getvalue()

    # Smart Read based on file extension
    if file_name.endswith('.csv'):
        try:
            text = raw_bytes.decode('utf-8')
            dict_df = {"Sheet1": pd.read_csv(io.StringIO(text), header=None, engine='python', on_bad_lines='skip', dtype=str)}
        except UnicodeDecodeError:
            text = raw_bytes.decode('utf-16')
            dict_df = {"Sheet1": pd.read_csv(io.StringIO(text), header=None, engine='python', on_bad_lines='skip', dtype=str)}
    elif file_name.endswith(('.xls', '.xlsx')):
        dict_df = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=None, header=None, dtype=str)
    else:
        raise ValueError("Unsupported file format.")

    # Process each sheet
    for sheet_name, df_raw in dict_df.items():
        header_row_index = -1
        # Search for headers
        for i, row in df_raw.iterrows():
            row_vals = [str(v).strip().lower() for v in row.values]
            if any(x in row_vals for x in ['email', 'first_name', 'first name', 'phone', 'mail', 'fname']):
                header_row_index = i
                break

        if header_row_index == -1: 
            continue

        df_tab = df_raw.iloc[header_row_index + 1:].copy()
        df_tab.columns = [str(c).strip().lower() for c in df_raw.iloc[header_row_index]]

        tab_standardized = pd.DataFrame(index=df_tab.index)
        tab_standardized['Label'] = label_value

        for target, synonyms in mapping_rules.items():
            found_col = next((c for c in df_tab.columns if any(s.lower() in c for s in synonyms)), None)
            if found_col:
                tab_standardized[target] = df_tab[found_col]
            else:
                tab_standardized[target] = ""

        processed_dfs.append(tab_standardized)

    if not processed_dfs:
        raise ValueError(f"No valid data or headers found in the file: {uploaded_file.name}")

    df_final = pd.concat(processed_dfs, ignore_index=True)
    df_final = df_final.fillna("")

    # Filter out empty records
    data_cols = [c for c in final_columns if c != 'Label']
    is_row_blank = df_final[data_cols].apply(lambda x: x.astype(str).str.strip().replace(['nan', 'None', 'NULL', ''], pd.NA)).isna().all(axis=1)
    df_final = df_final[~is_row_blank].copy()
    
    # Enforce strict column order and completeness
    for col in final_columns:
        if col not in df_final.columns:
            df_final[col] = ""
            
    df_final = df_final[final_columns]
    
    return df_final


# ==========================================
# STREAMLIT USER INTERFACE
# ==========================================
st.set_page_config(page_title="Meta Lead Converter", layout="centered")

st.title("📊 Meta Lead Data Processor")
st.write("Upload your raw Meta/Facebook CSV or Excel file(s), choose your processing task, and download the standardized output.")

task = st.radio(
    "Select Processing Mode:", 
    ("Cleaning FB Lead Form", "Changing FB Lead Form to SF Format", "Changing SF -> Sleekflow format")
)

# File uploader updated to accept CSV, XLSX, and XLS
uploaded_files = st.file_uploader("Upload Raw Data CSV/Excel(s)", type=['csv', 'xlsx', 'xls'], accept_multiple_files=True)

# Dynamic Fields based on user selection
event_name = ""
platform_link = ""
label_value = ""

if task == "Changing FB Lead Form to SF Format":
    st.markdown("### SF Format Required Fields")
    event_name = st.text_input("Event Name", placeholder="e.g., Summer MBA Fair 2026")
    platform_link = st.text_input("Platform Link", placeholder="https://zoom.us/j/12345...")
elif task == "Changing SF -> Sleekflow format":
    st.markdown("### Sleekflow Format Required Fields")
    label_value = st.text_input("Label", placeholder="e.g., ;HKUST Part-Time (Weekly) Info Session | Jul 2")

if st.button("Process Data"):
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one file first.")
    elif task == "Changing FB Lead Form to SF Format" and (not event_name or not platform_link):
        st.warning("⚠️ Please fill in both the Event Name and Platform Link.")
    elif task == "Changing SF -> Sleekflow format" and not label_value:
        st.warning("⚠️ Please fill in the Label value.")
    else:
        try:
            with st.spinner(f"Processing {len(uploaded_files)} file(s)..."):
                
                processed_dfs = []
                for file in uploaded_files:
                    
                    # Direct new tool logic
                    if task == "Changing SF -> Sleekflow format":
                        processed_df = process_sleekflow_format(file, label_value)
                        processed_dfs.append(processed_df)
                        
                    # Original FB Lead Form tools logic
                    else:
                        if not file.name.lower().endswith('.csv'):
                            st.error(f"⚠️ {file.name} skipped: Task 1 and Task 2 currently only support CSV files.")
                            continue
                            
                        raw_df = load_data(file)
                        
                        if task == "Cleaning FB Lead Form":
                            processed_df = process_cleaning_fb(raw_df)
                        elif task == "Changing FB Lead Form to SF Format":
                            processed_df = process_sf_format(raw_df, event_name, platform_link)
                            
                        processed_dfs.append(processed_df)
                
                if processed_dfs:
                    # Combine all processed files into one master dataframe
                    master_df = pd.concat(processed_dfs, ignore_index=True)
                    
                    # Optional sorting for task 1
                    if task == "Cleaning FB Lead Form" and 'created_time' in master_df.columns:
                         master_df = master_df.sort_values(by='created_time', ascending=True)

                    if task == "Cleaning FB Lead Form":
                        file_name = "Cleaned_FB_Leads_Combined.csv"
                    elif task == "Changing FB Lead Form to SF Format":
                        file_name = "SF_Formatted_Leads_Combined.csv"
                    else:
                        file_name = "Sleekflow_Formatted_Leads_Combined.csv"
                    
                    st.success("✅ Data combined and processed successfully!")
                    st.dataframe(master_df.head(10)) 
                    
                    csv_data = master_df.to_csv(index=False).encode('utf-8-sig')
                    
                    st.download_button(
                        label=f"📥 Download Combined Output CSV ({len(uploaded_files)} files)",
                        data=csv_data,
                        file_name=file_name,
                        mime="text/csv"
                    )
                else:
                    st.error("❌ No valid files were processed.")
                    
        except Exception as e:
            st.error(f"❌ An error occurred during processing: {e}")
