from accor_repo import AccorRepo
from dotenv import load_dotenv
import pandas as pd
import time
import pyautogui
import functions as f
import datetime

# Further update will be text processing. worldspan has limit per line input!!

# find opposite direction
def find_opposite_dir(direction):
    opposite_direction = {
    'N': 'S',
    'S': 'N',
    'W': 'E',
    'E': 'W'
    }
    
    opp_orientation = ''
    try:
        for i in direction:
            opp_orientation += opposite_direction.get(i)
        return opp_orientation
    except:
        return 'N'

# for save Worldspand data
def save():
    pyautogui.press('left')
    pyautogui.press('left')
    pyautogui.press('left')
    pyautogui.press('left')
    pyautogui.press('left')
    pyautogui.press('up')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('HUE')
    pyautogui.press('enter')
    time.sleep(1)
    
def type_with_delay(text, delay=0.5):
    text = str(text)
    pyautogui.typewrite(text)
    time.sleep(delay)
    
def find_gds_windows():
    time.sleep(1)
    image = pyautogui.locateOnScreen(r"img\worldspan_main.PNG", confidence=0.85)
    print('Please Open GDS - Term Worldspan Prod')
    while image == None:
        image = pyautogui.locateOnScreen(r"img\worldspan_main.PNG", confidence=0.85)
        time.sleep(5)
    
# Get info from Day1
hotel_rid = input('Please Enter Hotel RID: ')
hotel_rid = str(hotel_rid).upper()
file_path = f"gds\worldspan\{hotel_rid} Worldspan.csv"
df = pd.read_csv(file_path, dtype=str)

worldspan_code = df['worldspan code'].iloc[0]

# Get data
hotel_content = AccorRepo(hotel_rid)

# Update Geo Location
# HHGM + Chain code + worldspand code

# Latitude
latitude = hotel_content.get_latitude()
latitude = float(latitude)
if abs(latitude) < 10:
    latitude_6decimals = "0" + "{:.6f}".format(abs(latitude)) 
else:
    latitude_6decimals = "{:.6f}".format(abs(latitude)) 
    
if latitude > 0:
    latitude_formatted = ' ' + str(latitude_6decimals)
else:
    latitude_formatted = '-' + str(latitude_6decimals)


# Longtitude
longtitude = hotel_content.get_longitude()
longtitude = float(longtitude)
if abs(longtitude) < 100:
    longtitude_6decimals = "0" + "{:.6f}".format(abs(longtitude)) 
else:
    longtitude_6decimals = "{:.6f}".format(abs(longtitude)) 
    
if longtitude > 0:
    longtitude_formatted = ' ' + str(longtitude_6decimals)
else:
    longtitude_formatted = '-' + str(longtitude_6decimals)

# iata code from AER1
hotel_content.get_iata()
iata_code = hotel_content.iata_code

# Distance in Mile (Round Number) 
if hotel_content.airport_unit == 'Km':
    distance_km = hotel_content.airport_distance
    distance_m = str((int((float(distance_km) * 0.621371))))
else:
    distance_m = hotel_content.airport_distance
    
# Unit always M
unit = 'M'  

# Oppsite direction of AER1 in TARS

opp_orientation = hotel_content.airport_direction


# Enter Worldspan Geo code
find_gds_windows()
pyautogui.typewrite('HHGM' + worldspan_code)
pyautogui.press('enter')
time.sleep(2)

f.tabing(6)
type_with_delay(latitude_formatted)
f.tabing(1)
type_with_delay(longtitude_formatted)
f.tabing(1)
type_with_delay(iata_code)
f.tabing(2)
type_with_delay(distance_m)
f.tabing(1)
type_with_delay(unit)
f.tabing(1)
type_with_delay(opp_orientation)
f.tabing(4)
time.sleep(2)
save()
time.sleep(1.5)

# ADD Surrounding
attraction_df = hotel_content.get_attractions()
c_country = df['CNTRY'].iloc[0]
ctr1 = attraction_df.iloc[0]
ctr1_name = ctr1['AttractionName']
ctr1_dis = str(int(ctr1['DistanceMiles']))
ctr1_dir = ctr1['Direction']
ctri_opp_dir = find_opposite_dir(direction=ctr1_dir)


pcn = attraction_df.iloc[1]
pcn_name = pcn['AttractionName']
pcn_dis = str(int(pcn['DistanceMiles']))
pcn_dir = pcn['Direction']
pcn_opp_dir = find_opposite_dir(direction=pcn_dir)

apt1 = attraction_df.iloc[2]
apt1_name = apt1['AttractionName']
apt1_dis = str(int(apt1['DistanceMiles']))
apt1_dir = apt1['Direction']
apt1_opp_dir = find_opposite_dir(direction=apt1_dir)

pyautogui.typewrite('HHTA' + worldspan_code)
pyautogui.press('enter')
time.sleep(2)
f.tabing(7)

type_with_delay(text=ctr1_name)
f.tabing(2)
type_with_delay(text=c_country)
f.tabing(1)
type_with_delay(text=ctr1_dis)
f.tabing(1)
type_with_delay(text=ctri_opp_dir)
f.tabing(1)

type_with_delay(text=pcn_name)
f.tabing(2)
type_with_delay(text=c_country)
f.tabing(1)
type_with_delay(text=pcn_dis)
f.tabing(1)
type_with_delay(text=pcn_opp_dir)
f.tabing(1)

type_with_delay(text=apt1_name)
f.tabing(2)
type_with_delay(text=c_country)
f.tabing(1)
type_with_delay(text=apt1_dis)
f.tabing(1)
type_with_delay(text=apt1_opp_dir)
f.tabing(1)
f.tabing(31)
save()
time.sleep(1.5)

# guarantee 
pyautogui.typewrite('HHQA' + worldspan_code)
pyautogui.press('enter')
time.sleep(1.5)
f.tabing(13)

# Get current time data
current_datetime = datetime.datetime.now()
# Format to DDMMYY
formatted_date = current_datetime.strftime("%d%b%y").upper()

pyautogui.typewrite(formatted_date + '-' + 'XXXXXXX')
f.tabing(1)
pyautogui.typewrite('1234567')
f.tabing(1)
pyautogui.typewrite('1800')
f.tabing(1)
pyautogui.typewrite('X')
f.tabing(43)
pyautogui.press('right', presses=5, interval=0.15)
pyautogui.press('enter')
time.sleep(1)
pyautogui.typewrite('HUE')
pyautogui.press('enter')
time.sleep(1.5)

# canpol
pyautogui.typewrite('HHNA' + worldspan_code)
pyautogui.press('enter')
time.sleep(1.5)
f.tabing(15)
time.sleep(0.5)

pyautogui.typewrite(formatted_date + '-' + 'XXXXXXX')
f.tabing(1)
pyautogui.typewrite('1234567')
f.tabing(1)
pyautogui.typewrite('1800')
f.tabing(28)
pyautogui.press('right', presses=10, interval=0.15)
pyautogui.press('enter')
time.sleep(1)
pyautogui.typewrite('HUE')
pyautogui.press('enter')
time.sleep(1.5)

# Amemities add only one the rest will flow
pyautogui.typewrite('HHMA' + worldspan_code)
pyautogui.press('enter')
time.sleep(1.5)
f.tabing(20)
time.sleep(0.5)
pyautogui.typewrite('X')
f.tabing(1)
pyautogui.press('enter')
time.sleep(1.5)
pyautogui.typewrite('HUE')
pyautogui.press('enter')
time.sleep(1.5)

# Activate Hotel
pyautogui.typewrite('HHWU' + worldspan_code)
pyautogui.press('enter')
time.sleep(1.5)

# Check unlock status
pyautogui.typewrite('HHWR' + worldspan_code)
pyautogui.press('enter')
time.sleep(1.5)
         


