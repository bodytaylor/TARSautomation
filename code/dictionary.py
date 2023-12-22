# Function for search value and return key in dictionary
def search_key(dict, search_value):
    found_key = None
    for key, value in dict.items():
        if value == search_value:
            found_key = key
            break
    return found_key

brands_dict = {
    "21C": '21c MUSEUM HOTELS',
    "ADG": 'APARTHOTELS ADAGIO',
    "ADP": 'ADAGIO PREMIUM',
    "AHE": 'ASSOCIATED HOTEL ECO',
    "AHM": 'ASSOCIATED HOTEL MIDSCALE',
    "AHU": 'ASSOCIATED HOTEL UPSCALE',
    "ALP": 'Not Use ALL SEASONS PREMIER',
    "ALS": 'Not use all seasons',
    "ART": 'ART SERIES',
    "ASE": 'ALL SEASONS',
    "ATR": 'ATRIA',
    "BAN": 'BANYAN TREE HOTELS RESORTS',
    "BKF": 'BREAKFREE',
    "BME": 'BY MERCURE',
    "CAR": 'CASSIA RESIDENCES',
    "CM": 'CLUB MED',
    "COR": 'CORALIA',
    "DEL": 'DELANO',
    "DEM": 'SOFITEL DEMEURE',
    "DOR": 'DORINT',
    "EMB": 'EMBLEMS',
    "ETP": 'ETAP HOTEL',
    "FAE": 'FAENA',
    "FAI": 'FAIRMONT',
    "FOR": 'FORMULE',
    "GLE": 'GLENEAGLES',
    "GRE": 'GREET',
    "HLB": 'HOTELS BARRIERE',
    "HOF": 'HOTELF1',
    "HOX": 'THE HOXTON',
    "HYD": 'HYDE',
    "HZU": 'HUAZHU',
    "IBB": 'IBIS BUDGET',
    "IBF": 'INDIAN FORMULE',
    "IBH": 'IBIS HOTELS',
    "IBI": 'IBIS (OLD BRAND)',
    "IBS": 'IBIS STYLES',
    "JDP": 'JARDINS DE PARIS',
    "JIN": 'JIN JIANG',
    "JOE": 'JO&JOE',
    "LIB": 'LIBERTEL',
    "MEI": 'GRAND MERCURE',
    "MER": 'MERCURE',
    "MGA": 'MGALLERY',
    "MGR": 'MGALLERY RESIDENCES',
    "MOD": 'MONDRIAN',
    "MOT": 'MOTEL',
    "MOV": 'MOVENPICK',
    "MSH": 'MAMA SHELTER',
    "MTA": 'MANTRA',
    "MTS": 'MANTIS',
    "NEQ": 'NEQTA',
    "NOL": 'NOVOTEL LIVING',
    "NOV": 'NOVOTEL',
    "OER": 'ORIENT EXPRESS RESIDENCES',
    "OES": 'ORIENT EXPRESS SERVICED RESIDENC',
    "OEX": 'ORIENT EXPRESS',
    "ORB": 'ORBIS',
    "PAN": 'PANNONIA',
    "PEP": 'PEPPERS',
    "PTH": 'PARTHENON',
    "PUL": 'PULLMAN',
    "PUR": 'THE PURIST',
    "RAF": 'RAFFLES',
    "RDR": 'RED ROOF INN',
    "REH": 'THE REDBURY',
    "RES": 'ACCOR',
    "RIX": 'RIXOS HOTELS',
    "SAM": 'OTHER BRANDS',
    "SEB": 'THE SEBEL',
    "SLS": 'SLS',
    "SO": 'SO/',
    "SOF": 'SOFITEL',
    "SOU": 'HANDWRITTEN',
    "STD": 'SUITE',
    "SUI": 'NOVOTEL SUITES',
    "SWI": 'SWISSOTEL',
    "THA": 'THALASSA SEA AND SPA',
    "TOR": 'MORGANS ORIGINALS',
    "TRI": 'TRIBE',
    "TST": 'HOTEL DE TEST',
    "TWF": '25HOURS',
    "VIL": 'VILLAGES HÔTEL'
}

chain_dict = {
    "ETAP HOTEL": "ETP",
    "FAENA": "FAE",
    "FAIRMONT": "FAI",
    "FAIRMONT SERVICED RESIDENCES": "FAR",
    "FOLIO": "FOL",
    "FORMULE": "FOR",
    "GARRYA": "GAR",
    "GLENEAGLES": "GLE",
    "GREET": "GRE",
    "HOUSE OF EMBLEMS": "HEM",
    "HI INN": "HII",
    "HOTELS BARRIERE": "HLB",
    "HOTELF1": "HOF",
    "HOMM": "HOM",
    "THE HOXTON": "HOX",
    "HANTING HOTEL": "HTG",
    "HYDE": "HYD",
    "HYDE LIVING": "HYL",
    "IBIS BUDGET": "IBB",
    "INDIAN FORMULE": "IBF",
    "IBIS HOTELS": "IBH",
    "IBIS (OLD CHAIN)": "IBI",
    "IBIS STYLES": "IBS",
    "JI HOTEL": "JIH",
    "JIN JIANG": "JIN",
    "JO&JOE": "JOE",
    "JOYA HOTEL": "JOY",
    "MONDRIAN LIVING": "MDL",
    "GRAND MERCURE": "MEI",
    "MERCURE LIVING": "MEL",
    "MERCURE": "MER",
    "MGALLERY": "MGA",
    "MGALLERY LIVING": "MGL",
    "MGALLERY RESIDENCES": "MGR",
    "MANXIN HOTELS RESORTS": "MHR",
    "MONDRIAN": "MOD",
    "MOVENPICK LIVING": "MOL",
    "MOTEL": "MOT",
    "MOVENPICK": "MOV",
    "MAMA SHELTER": "MSH",
    "MANTRA": "MTA",
    "MANTIS": "MTS",
    "NEQTA": "NEQ",
    "NOVOTEL LIVING": "NOL",
    "NOVOTEL": "NOV",
    "ORIENT EXPRESS RESIDENCES": "OER",
    "ORIENT EXPRESS SERVICED RESIDENC": "OES",
    "ORIENT EXPRESS": "OEX",
    "ORBIS": "ORB",
    "PEPPERS": "PEP",
    "PULLMAN LIVING": "PLL",
    "PULLMAN": "PUL",
    "RAFFLES": "RAF",
    "RED ROOF INN": "RDR",
    "REDBURY HOTELS": "REH",
    "RIXOS HOTELS": "RIX",
    "OTHER BRAND": "SAM",
    "THE SEBEL": "SEB",
    "SLS": "SLS",
    "SO/": "SO",
    "SOFITEL": "SOF",
    "SOFITEL LEGEND": "SOL",
    "SOFITEL SERVICED RESIDENCES": "SOR",
    "SO SOFITEL": "SOS",
    "HANDWRITTEN": "SOU",
    "SO/ SERVICED RESIDENCES": "SSR",
    "STARWAY HOTEL": "STA",
    "STUDIO": "STD",
    "NOVOTEL SUITES": "SUI",
    "SWISSOTEL": "SWI",
    "SWISSOTEL LIVING": "SWL",
    "MORGANS ORIGINALS": "TOR",
    "TRIBE": "TRI",
    "HOTEL DE TEST": "TST",
    "25HOURS": "TWF",
    "VILLAGES HÔTEL": "VIL",
}

loggin_type_dict = {
    "FR": 'Franchised',
    "MG": 'Managed',
    "AC": 'Subsidiary'
}

lodging_type_dict = {
    "Hotel": "HTL",
    "Non Hotel": "NHP",
    "Resort hotel": "RST",
    "Serviced Apartment (Adagio)": "APT",
}

standard_dict = {
    "21c MUSEUM HOTELS": "LX",
    "25HOURS": "UP",
    "ADAGIO ACCESS": "FI",
    "ADAGIO ORIGINAL": "TO",
    "ADAGIO PREMIUM": "UP",
    "ALL SEASONS": "TO",
    "ANGSANA": "UP",
    "ART SERIES": "UP",
    "BANYAN TREE": "LX",
    "BREAKFREE": "TO",
    "BY MERCURE": "FI",
    "CASSIA": "FI",
    "DELANO": "FI",
    "DHAWA": "LX",
    "ETAP HOTEL": "BU",
    "FAENA": "LX",
    "FAIRMONT": "LX",
    "FOLIO": "FI",
    "GARRYA": "FI",
    "GRAND MERCURE": "UP",
    "GREET": "TO",
    "HANDWRITTEN": "FI",
    "HOMM": "FI",
    "HOTELF1": "BU",
    "HYDE": "LX",
    "IBIS BU": "BU",
    "IBIS HOTELS": "TO",
    "IBIS STYLES": "TO",
    "JO&JOE": "BU",
    "MAMA SHELTER": "FI",
    "MANTRA": "FI",
    "MANTIS": "UP",
    "MERCURE": "FI",
    "MERCURE LIVING": "FI",
    "MGALLERY BY SOFITEL": "LX",
    "MONDRIAN": "LX",
    "MORGANS ORIGINALS": "LX",
    "Mövenpick": "UP",
    "MOVENPICK": "UP",
    "MOVENPICK LIVING": "UP",
    "NOVOTEL": "FI",
    "NOVOTEL LIVING": "FI",
    "NOVOTEL SUITES": "FI",
    "PEPPERS": "UP",
    "PULLMAN": "UP",
    "RAFFLES": "LX",
    "RIXOS HOTELS": "LX",
    "SLS": "LX",
    "SO SOFITEL": "LX",
    "SOFITEL": "LX",
    "SOFITEL LEGEND": "LX",
    "SWISSOTEL": "UP",
    "SWISSOTEL LIVING": "UP",
    "THE SEBEL": "UP",
    "TRIBE": "FI",
}

enviro_dict = {
    "At the airport": "AIR",
    "At the seaside": "SEA",
    "Beside a golf course": "GOL",
    "Beside a lake": "LAC", 
    "Beside a park": "PAR",
    "Beside a river": "RIV",
    "In the centre of town": "TOW",
    "In the country": "COU",
    "In the mountains": "MOU",
    "In town": "CIT",
    "Near the beach": "NTB",
    "On the Beach": "BEA",
    "Suburb": "SUB", 
    "Woodland/forest area": "WOO",
    "In the center of town": "TOW",
    "On the beach": "BEA",
}

location_dict = {
    "Business district": "BUSD",
    "Downtown": "CITY",
    "Eastern suburb": "ESUB",
    "Entertainment district": "ENTD",
    "Financial district": "FINA",
    "Northern suburb": "NSUB",
    "On the highway": "HIGH",
    "Resort": "RESO",
    "Shopping district": "SHOP",
    "Southern suburb": "SSUB",
    "Theatre district": "THEA",
    "University area": "UNI",
    "Western suburb": "WSUB",
    "Within 5 min of train station": "TRAN",
    "Within 5 min of airport": "AIRP",
}

bar_dic = {
    "BAR1": "AMERICAN BAR",
    "BAR": "BAR",
    "IBI99": "bar",
    "IBI01": "bar-rendez-vous",
    "BAR7": "DISCOTHEQUE BAR",
    "BAR6": "LOBBY BAR",
    "LOUNGE": "LOUNGE",
    "BAR4": "PIANO BAR",
    "BAR2": "POOL BAR",
    "BAR3": "POOL SIDE SNACK BAR",
    "PRIVBA": "PRIVATE BAR",
    "PUB": "PUB",
    "SNACBA": "SNACK-BAR",
    "WINBAR": "WINE BAR",
}

country_dict = {
    "AFGHANISTAN": "AF",
    "ALAND ISLANDS": "AX",
    "ALBANIA": "AL",
    "ALGERIA": "DZ",
    "AMERICAN SAMOA": "AS",
    "ANDORRA": "AD",
    "ANGOLA": "AO",
    "ANGUILLA": "AI",
    "ANTARTICA": "AQ",
    "ANTIGUA AND BARBUDA": "AG",
    "ARGENTINA": "AR",
    "ARMENIA": "AM",
    "ARUBA": "AW",
    "AUSTRALIA": "AU",
    "AUSTRIA": "AT",
    "AZERBAIJAN": "AZ",
    "BAHAMAS": "BS",
    "BAHRAIN": "BH",
    "BANGLADESH": "BD",
    "BARBADOS": "BB",
    "BELARUS": "BY",
    "BELGIUM": "BE",
    "BELIZE": "BZ",
    "BENIN": "BJ",
    "BERMUDA": "BM",
    "BHUTAN": "BT",
    "BOLIVIA": "BO",
    "BONAIRE, SINT EUSTATIUS AND SABA": "BQ",
    "BOSNIA AND HERZEGOVINA": "BA",
    "BOTSWANA": "BW",
    "BOUVET ISLAND": "BV",
    "BRAZIL": "BR",
    "BRITISH INDIAN OCEAN TERRITORY": "IO",
    "BRUNEI DARUSSALAM": "BN",
    "BULGARIA": "BG",
    "BURKINA FASO": "BF",
    "BURUNDI": "BI",
    "CAMBODIA": "KH",
    "CAMEROON": "CM",
    "CANADA": "CA",
    "CAPE VERDE": "CV",
    "CAYMAN ISLANDS": "KY",
    "CENTRAL AFRICAN REPUBLIC": "CF",
    "CHAD": "TD",
    "CHILE": "CL",
    "CHINA": "CN",
    "CHRISTMAS ISLAND": "CX",
    "COCOS (KEELING) ISLANDS": "CC",
    "COLOMBIA": "CO",
    "COMOROS": "KM",
    "CONGO": "CG",
    "COOK ISLANDS": "CK",
    "COSTA RICA": "CR",
    "CROATIA": "HR",
    "CUBA": "CU",
    "CURACAO": "CW",
    "CYPRUS": "CY",
    "CZECH REPUBLIC": "CZ",
    "DEMOCRATIC REPUBLIC KOREA": "KP",
    "DEMOCRATIC REPUBLIC LAO": "LA",
    "DEMOCRATIC REPUBLIC OF CONGO": "CD",
    "DENMARK": "DK",
    "DJIBOUTI": "DJ",
    "DOMINICA": "DM",
    "DOMINICAN REPUBLIC": "DO",
    "ECUADOR": "EC",
    "EGYPT": "EG",
    "EL SALVADOR": "SV",
    "EQUATORIAL GUINEA": "GQ",
    "ERITREA": "ER",
    "ESTONIA": "EE",
    "ETHIOPIA": "ET",
    "FALKLAND ISLAND/MALVINAS": "FK",
    "FAROE ISLANDS": "FO",
    "FIJI": "FJ",
    "FINLAND": "FI",
    "FRANCE": "FR",
    "FRENCH GUIANA": "GF",
    "FRENCH POLYNESIA": "PF",
    "FRENCH SOUTHERN TERRITORIES": "TF",
    "GABOON": "GA",
    "GAMBIA": "GM",
    "GEORGIA": "GE",
    "GERMANY": "DE",
    "GHANA": "GH",
    "GIBRALTAR": "GI",
    "GREECE": "GR",
    "GREENLAND": "GL",
    "GRENADA": "GD",
    "GUADELOUPE": "GP",
    "GUAM": "GU",
    "GUATEMALA": "GT",
    "GUERNSEY": "GG",
    "GUINEA": "GN",
    "GUINEA BISSAU": "GW",
    "GUYANA": "GY",
    "HAITI": "HT",
    "HEARD ISLAND MCDONALD ISLANDS": "HM",
    "HOLY SEE (VATICAN CITY STATE)": "VA",
    "HONDURAS": "HN",
    "HONG KONG SAR, CHINA": "HK",
    "HUNGARY": "HU",
    "ICELAND": "IS",
    "INDIA": "IN",
    "INDONESIA": "ID",
    "IRAN": "IR",
    "IRAQ": "IQ",
    "IRELAND": "IE",
    "ISLE OF MAN": "IM",
    "ISRAEL": "IL",
    "ITALY": "IT",
    "IVORY COAST": "CI",
    "JAMAICA": "JM",
    "JAPAN": "JP",
    "JERSEY": "JE",
    "JORDAN": "JO",
    "KAZAKHSTAN": "KZ",
    "KENYA": "KE",
    "KIRIBATI": "KI",
    "KOREA, REPUBLIC OF": "KR",
    "KOSOVO": "XK",
    "KUWAIT": "KW",
    "KYRGYSTAN": "KG",
    "LATVIA": "LV",
    "LEBANON": "LB",
    "LESOTHO": "LS",
    "LIBERIA": "LR",
    "LIBYA": "LY",
    "LIECHTENSTEIN": "LI",
    "LITHUANIA": "LT",
    "LUXEMBOURG": "LU",
    "MACAU SAR, CHINA": "MO",
    "MADAGASCAR": "MG",
    "MALAWI": "MW",
    "MALAYSIA": "MY",
    "MALDIVES": "MV",
    "MALI": "ML",
    "MALTA": "MT",
    "MARSHALL ISLANDS": "MH",
    "MARTINIQUE": "MQ",
    "MAURITANIA": "MR",
    "MAURITIUS": "MU",
    "MAYOTTE": "YT",
    "MEXICO": "MX",
    "MICRONESIA, FEDERATED STATES OF": "FM",
    "MOLDOVA": "MD",
    "MONACO": "MC",
    "MONGOLIA": "MN",
    "MONTENEGRO": "ME",
    "MONTSERRAT": "MS",
    "MOROCCO": "MA",
    "MOZAMBIQUE": "MZ",
    "MYANMAR": "MM",
    "NAMIBIA": "NA",
    "NAURU": "NR",
    "NE PAS UTILISER XXXXXXXXX": "XX",
    "NEPAL": "NP",
    "NETHERLANDS": "NL",
    "NETHERLANDS ANTILLES": "AN",
    "NEW CALEDONIA": "NC",
    "NEW ZEALAND": "NZ",
    "NICARAGUA": "NI",
    "NIGER": "NE",
    "NIGERIA": "NG",
    "NIUE": "NU",
    "NORFOLK ISLAND": "NF",
    "NORTHERN MARIANA ISLANDS": "MP",
    "NORWAY": "NO",
    "OMAN": "OM",
    "PAKISTAN": "PK",
    "PALAU": "PW",
    "PALESTINIAN TERRITORY": "PS",
    "PANAMA": "PA",
    "PAPUA NEW GUINEA": "PG",
    "PARAGUAY": "PY",
    "PERU": "PE",
    "PHILIPPINES": "PH",
    "PITCAIRN": "PN",
    "POLAND": "PL",
    "PORTUGAL": "PT",
    "PUERTO RICO": "PR",
    "QATAR": "QA",
    "REPUBLIC OF MACEDONIA": "MK",
    "REUNION": "RE",
    "ROMANIA": "RO",
    "RUSSIAN FEDERATION": "RU",
    "RWANDA": "RW",
    "SAINT BARTHELEMY": "BL",
    "SAINT KITTS AND NEVIS": "KN",
    "SAINT LUCIA": "LC",
    "SAINT MARTIN (FRENCH PART)": "MF",
    "SAINT PIERRE AND MIQUELON": "PM",
    "SAINT VINCENT AND THE GRENADINES": "VC",
    "SAMOA": "WS",
    "SAN MARINO": "SM",
    "SAO TOME AND PRINCIPE": "ST",
    "SAUDI ARABIA": "SA",
    "SENEGAL": "SN",
    "SERBIA": "RS",
    "SEYCHELLES": "SC",
    "SIERRA LEONE": "SL",
    "SINGAPORE": "SG",
    "SINT MAARTEN (DUTCH PART)": "SX",
    "SLOVAKIA": "SK",
    "SLOVENIA": "SI",
    "SOLOMON ISLANDS": "SB",
    "SOMALIA": "SO",
    "SOUTH AFRICA": "ZA",
    "SOUTH GEORGIA SOUTH SANDWICH ISL": "GS",
    "SOUTH SUDAN": "SS",
    "SPAIN": "ES",
    "SRI LANKA": "LK",
    "ST HELENA,ASCENSION AND TRISTAN": "SH",
    "SUDAN": "SD",
    "SURINAME": "SR",
    "SVALBARD AND JAN MAYEN": "SJ",
    "SWAZILAND": "SZ",
    "SWEDEN": "SE",
    "SWITZERLAND": "CH",
    "SYRIAN ARAB REPUBLIC": "SY",
    "TAIWAN": "TW",
    "TAJIKISTAN": "TJ",
    "TANZANIA": "TZ",
    "THAILAND": "TH",
    "TIMOR-LESTE": "TL",
    "TOGO": "TG",
    "TOKELAU": "TK",
    "TONGA": "TO",
    "TRINIDAD AND TOBAGO": "TT",
    "TUNISIA": "TN",
    "TURKEY": "TR",
    "TURKMENISTAN": "TM",
    "TURKS AND CAICOS ISLAND": "TC",
    "TUVALU": "TV",
    "UGANDA": "UG",
    "UKRAINE": "UA",
    "UNITED ARAB EMIRATES": "AE",
    "UNITED KINGDOM": "GB",
    "UNITED STATES": "US",
    "UNITED STATES MINOR ISLANDS": "UM",
    "URUGUAY": "UY",
    "UZBEKISTAN": "UZ",
    "VANUATU": "VU",
    "VENEZUELA": "VE",
    "VIET NAM": "VN",
    "VIRGIN ISLANDS BRITISH": "VG",
    "VIRGIN ISLANDS U.S.": "VI",
    "WALLIS AND FUTUNA": "WF",
    "YEMEN": "YE",
    "ZAMBIA": "ZM",
    "ZIMBABWE": "ZW",
    }

# attractions dict
surrouding_dict = {
    'ADML':	'Administrative Location',
    'AIRP':	'Airport',
    'SKI': 'At a ski lift',
    'BAR': 'Bar',
    'BAY': 'Bay',
    'BUS': 'Bus stop',
    'AFFA':	'Business & financial district',
    'CANL':	'Canal',
    'CITY':	'City center',
    'DOWN':	'City downtown',
    'NCIT':	'Closest major urban centre',
    'CENT':	'Distance from city centre',
    'NPT1':	'Domestic airport 1 - full name',
    'NAP1':	'Domestic airport 1 - IATA code',
    'NPT2':	'Domestic airport 2 - full name',
    'NAP2':	'Domestic airport 2 - IATA code',
    'NPT3':	'Domestic airport 3 - full name',
    'NAP3':	'Domestic airport 3 - IATA code',
    'THEA':	'Entertainment/theatre district',
    'FERR':	'Ferries',
    'HELI':	'Helipad/aerodrome',
    'HEXI':	'Highway exit',
    'APT1':	'Int. airport 1 - full name',
    'AER1':	'Int. airport 1 - IATA code',
    'APT2':	'Int. airport 2 - full name',
    'AER2':	'Int. airport 2 - IATA code',
    'APT3':	'Int. airport 3 - full name',
    'AER3':	'Int. airport 3 - IATA code',
    'APT4':	'Int. airport 4 - full name',
    'AER4':	'Int. airport 4 - IATA code',
    'APT5':	'Int. airport 5 - full name',
    'AER5':	'Int. airport 5 - IATA code',
    'MARI':	'Marina',
    'HARD':	'Marine terminal',
    'METR':	'Metro/underground/subway',
    'MONT':	'Mountain',
    'NAPA':	'National park',
    'PLGN':	'Nearby',
    'NCC': 'Nearest major city - code',
    'NCN': 'Nearest major city - name',
    'PLAG':	'On the beach',
    'VIEW':	'Panoramic view',
    'PARK':	'Park',
    'PCC': 'Primary city code',
    'PCN': 'Primary city name',
    'STAT':	'Railway and underground station',
    'GARE':	'Railway station',
    'RSTO':	'Restaurant',
    'RIVE':	'River',
    'SHOP':	'Shopping district',
    'THTR':	'Theatre',
    'SNCF':	'TRAIN + HOTEL GARE SNCF',
    'TRAM':	'Tramway',
    'VALL':	'Valley',
    'SVIE':	'With sea view',
    'WOOD':	'Wood/forest',
    'ADMI':	'Administrative building',
    'ENT': 'Amusement park',
    'APAR':	'Amusement park',
    'AQU': 'Aquarium',
    'ARTC':	'Art and Culture',
    'PLGA':	'Beach area',
    'BOT': 'Botanical gardens',
    'EVNT':	'Business centre',
    'CAS': 'Casino',
    'CINE':	'Cinema district',
    'CLIN':	'Clinic/hospital',
    'COLL':	'College/university',
    'COMP':	'Company',
    'CONC':	'Concert hall',
    'CONG':	'Convention centre',
    'CULT':	'Cultural centre',
    'EMBA':	'Embassy',
    'ENTE':	'Entertainment and theatre',
    'ENTC':	'Entertainment centre',
    'EVNS':	'Events centre',
    'EXHI':	'Exhibition and convention centre',
    'EXPO':	'Exhibition centre',
    'GOLF':	'Golf course',
    'HIST':	'Historic monument',
    'HOPI':	'Hospital',
    'INDU':	'Industrial area',
    'LAKE':	'Lake',
    'MALL':	'Mall and Shopping Centre',
    'MILI':	'Military base',
    'MOVI':	'Movie theatre',
    'MUSM':	'Museums',
    'TSP': 'Nearest transport',
    'OPE': 'Opera/symphony/concert hall',
    'OATT':	'Other attractions',
    'OTBU':	'Other point of business interest',
    'RELI':	'Place of worship',
    'CTR1':	'Primary point of interest',
    'RAC': 'Racetrack',
    'REST':	'Restaurant and cafe district',
    'SCHO':	'School/university',
    'SHOM':	'Shopping centre/mall',
    'PIST':	'Ski area',
    'DIVE':	'Special tourist area',
    'TOUR':	'Special tourist area',
    'CSPO':	'Sports centre',
    'SPOR':	'Sports centre',
    'STAD':	'Stadium',
    'ATOU':	'Tourist attraction',
    'INFO':	'Tourist information',
    'WORL':	'World Trade Center',
    'ZOO':	'Zoo',
    'PZOO':	'Zoological park',
    }