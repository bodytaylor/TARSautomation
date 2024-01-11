from deep_translator import GoogleTranslator
from fuzzywuzzy import process
from dictionary import *
from dotenv import load_dotenv
import os
import re
from datetime import datetime
import TarsAutomation as ta
import csv
import pandas as pd

# Todo Test the code
# Extraction will rewrite to full automate extraction directly from Welcome Now
def job_extraction():
    # path = input('Input report path: ').replace('"', '')
    path = r"D:\NSANGKARN\Downloads\sc_req_item.csv"
    df = pd.read_csv(path, dtype=str, encoding='ISO-8859-1')
    return df

# Google api setting
class AskGoogle():
    def __init__(self) -> None:
        import google.generativeai as genai
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)

        # Set up the model
        self.generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
            }

        self.safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
        ]

        self.model = genai.GenerativeModel(model_name="gemini-pro",
                                    generation_config=self.generation_config,
                                    safety_settings=self.safety_settings)
    
    def send_prompt(self, prompt_parts: list):
        response = self.model.generate_content(prompt_parts)
        return response.text
    
    def get_iata_code(self, city, country):
        # Ask Google and return IATA code from given city, country
        prompt_parts = [
            f"Given city and country, find nearest airport and return 3 character of IATA code: city = {city}, country = {country}"
        ]
        iata_code = self.send_prompt(prompt_parts)
        return iata_code

    def get_currency_code(self, currency_data):
        # Ask Google and return currency code 3 digits
        prompt_parts = [
            f"Find currency code for given information, return currency code 3 digits: data = {currency_data}",
            ]
        
        currency_code = self.send_prompt(prompt_parts)
        return currency_code
    
    def create_response(self, rid, name):
        prompt_parts = [
            "Rewrite this sentence: We are pleased to confirm you that the below request has been completed.",
            ]
        
        response = self.send_prompt(prompt_parts)
        ticket_response = f'{response} RID for the hotel is {rid}-{name} and the hotels status is DELETED'
        return ticket_response
    
# Function for RID Creation task
def extract_zipcode(text):
    # Use regex to find all numbers in the text
    numbers = re.findall(r'\d+', text)
    
    # Convert the matched strings to integers
    numbers = [int(num) for num in numbers]
    if len(numbers) >= 1:
        zip_code = str(numbers[-1])
    else:
        zip_code = '00000'
    
    return zip_code

def text_to_dict(text):
    data_dict = {}
    current_key = None
    
    for line in text.split('\n'):
        if ":" in line:
            current_key, value = map(str.strip, line.split(":", 1))
            data_dict[current_key] = value
        elif current_key is not None:
            data_dict[current_key] += "\n" + line.strip()
    
    for key, value in data_dict.items():
        formatted_value = str(value).replace('\n', '')
        data_dict[key] = formatted_value

    new_dict = {key.split('/')[-1]: value if '/' in key else value for key, value in data_dict.items()}  
    return new_dict

def split_text(address, max_characters=32):
    if len(address) <= max_characters:
        return [address]
    words = address.split()
    current_line = words[0]
    lines = []

    for word in words[1:]:
        if len(current_line) + len(word) + 1 <= max_characters:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    return lines

def find_best_match(query, choices):
    # Use process.extractOne to find the best match
    best_match = process.extractOne(query, choices)
    return best_match

# Function to create a CSV file and append data
def create_csv(file_path, data):
    # Check if the file exists
    file_exists = False
    try:
        with open(file_path, 'r') as file:
            file_exists = True
    except FileNotFoundError:
        pass

    # Open the CSV file in append mode
    with open(file_path, 'a', newline='') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)

        # If the file is newly created, write the header
        if not file_exists:
            csv_writer.writerow(['Number', 'RID', 'Hotel_name', 'Response_Text'])

        csv_writer.writerow(data)
        
# Transform data - Translate
def create_hotel_rid(google: AskGoogle, input: str):
    translated = GoogleTranslator(source='fr', target='en').translate(input)
    data = text_to_dict(translated)

    # Prep data
    country = data['Country']
    city = data['City']
    iata_code = google.get_iata_code(city, country)
    data['iata_code'] = iata_code

    # Hotel name and general information
    sign = data['Sign']
    hotel_name = data['Establishment name']
    chain_code = find_best_match(data['Sign'], chain_dict)[0]
    brand_code = find_best_match(data['Sign'], brands_dict)[2]
    # brand = find_best_match(data['Sign'], brands_dict)[0]
    if sign not in hotel_name:
        hotel_name = f'{sign} {hotel_name}'

    address = data['Address']
    zipcode = extract_zipcode(data["Address"])
    address = address.replace(zipcode, '')

    address = split_text(address)
    address1, address2, address3 = None, None, None
    if len(address) >= 1: 
        address1 = address[0]
    if len(address) >= 2:
        address2 = address[1]
    if len(address) >= 3:
        address3 = address[2]

    # Hotel Commercial name
    open_date = data['Opening date']
    try:
        date_format = "%d/%m/%Y"
        date_object = datetime.strptime(open_date, date_format)
    except ValueError:
        date_format = '%m/%d/%Y'
        date_object = datetime.strptime(open_date, date_format)  

    open_date = date_object.strftime("%d/%m/%Y")
    open_date_text = date_object.strftime("%B %Y")
    hotel_com_name = f'{hotel_name} (Opening {open_date_text})'

    country = data['Country'].upper()
    country_code = country_dict.get(country)

    loggin_type = find_best_match(data['Operation mode'], loggin_type_dict)[2]

    # Standard
    hotel_std = find_best_match(data['Sign'], standard_dict)[0]

    # Currency Code
    currency_code = google.get_currency_code(data['Currency'])

    # Tar Automate part

    ta.login()

    ta.new_hotel()
    ta.wait_for_element('hotelAddressLink')

    # Create RID
    ta.hotel_alpha_code(hotel_name, iata_code)
    ta.input_text('hotel.name', text=hotel_name)
    ta.select_dropdown('hotel.chain.code', chain_code)
    ta.select_dropdown('hotel.brand.code', brand_code)
    ta.input_text('hotel.commercialName', hotel_com_name)
    ta.input_text('hotel.address.addresses[0]', address1)
    ta.input_text('hotel.address.addresses[1]', address2)
    ta.input_text('hotel.address.addresses[2]', address3)
    ta.input_text('hotel.address.city', city)
    ta.input_text('hotel.address.zipCode', zipcode)
    ta.select_dropdown('hotel.address.country.code', country_code)
    ta.select_dropdown('hotel.hotelManagementType.code', loggin_type)

    # Submit Data
    ta.click_button('hotelTax.submitButton')
    ta.accept_alert()
    rid, name = ta.get_hotel_name()

    # General page
    ta.general_page()

    # Open date
    ta.input_text('gi_openingDate', open_date)

    # message to AH
    ta.tick_box('gi.mesToHotelOnAH')

    # Standard of the hotel
    ta.select_dropdown('gi.stHotCode', value=hotel_std)

    # Number of rooms
    ta.input_text('gi.nbOfRooms', text=data['Exploited rooms'])

    # Tars currency
    ta.select_dropdown('gi.currency', value=currency_code)

    # Click update
    ta.click_button('hotelTax.submitButton')
    ta.get_response(hotel_rid=rid, code='RID CREATION')
    
    # Log out
    ta.log_out()
    
    return rid, name

if __name__ == '__main__':
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%d%m%Y')
    file_path = f'log\{formatted_datetime}_RID_Creation.csv'
    google = AskGoogle()

    # Change file path to extraction file
    df = job_extraction()
    for index, row in df.iterrows():
        description = row['description']
        req_number = row['number']
        rid, name = create_hotel_rid(google, input=description)
        
        # Job report reqiure hotel RID and Ticket Number for next task.
        job_report = [req_number, rid, name, google.create_response(rid, name)]
        create_csv(file_path, data=job_report)
    
    # Close Browser
    ta.quit()
        
        
    


