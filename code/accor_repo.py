import requests
from bs4 import BeautifulSoup
from typing import Optional
import time

class AccorRepo():
    def __init__(self, hotel_rid: str):
        self.url = f'https://repos.accor.com/ota/{hotel_rid}.xml'
        response = requests.get(self.url)
        xml_content = response.text
        self.soup = BeautifulSoup(xml_content, 'xml')
        self.hotel_repo = self.soup.find('HotelDescriptiveContent', {'LanguageCode': 'en'})

    def convert_latin_to_utf8(self):
        try:
            # Convert Latin-1 to UTF-8
            utf8_string = self.encode('latin-1').decode('utf-8')
            return utf8_string
        except UnicodeDecodeError:
            print("Error: Unable to decode the input string.")
            return None
        
    def _get_field(self, segment: str, field: str, attribute: str) -> Optional[str]:
        segment_data = self.hotel_repo.find(segment)
        if segment_data is None:
            return None

        fields_data = segment_data.find(field)

        if fields_data is None:
            return None

        attribute_value = fields_data.get(attribute)
        if attribute_value is None:
            return None

        return attribute_value
    
    def get_latitude(self):
        self.latitude = self._get_field('HotelInfo', 'Position', 'Latitude')
        return self.latitude
    
    def get_longitude(self):
        self.longitude = self._get_field('HotelInfo', 'Position', 'Longitude')
        return self.longitude
    
    def get_ref_point(self):
        segment_data = self.hotel_repo.find('AreaInfo')
        fields_data = segment_data.find('RefPoints')

        for item in fields_data.find_all('RefPoint'):
            point_code = item['IndexPointCode']

            if point_code == '6': # Airport
                self.airport_name = item['Name']
                if len(self.airport_name) == 3:
                    self.iata_code = self.airport_name

                self.airport_direction = item['Direction']
                self.airport_distance = item['Distance']
                self.airport_unit = item['DistanceUnitName']

            elif point_code == '5': # City
                self.primary_city_name = item['Name']
                self.primary_city_direction = item['Direction']
                self.primary_city_distance = item['Distance']
                self.primary_city_unit = item['DistanceUnitName']   
    
    def get_hotel_info(self):
        self.brand_code = self.hotel_repo['BrandCode']
        self.brand_name = self.hotel_repo['BrandName']
        self.timezone = self.hotel_repo['TimeZone']
        self.currency = self.hotel_repo['CurrencyCode']
        self.hotel_name = self.hotel_repo['HotelName']
        self.hotel_short_name = self._get_field('HotelInfo', 'HotelName', 'HotelShortName')
        
    def hotel_address(self):
        xml_address = self.hotel_repo.find('ContactInfos') 
        adress_lines = xml_address.find_all('AddressLine')
        
        # Address
        address_list = [None, None, None]
        for index, line in enumerate(adress_lines):
            address_list[index] = line.text
            
        self.address1, self.address2, self.address3 = address_list
        
        # Phone
        phone_detail = xml_address.find('Phones')
        phone = phone_detail.find('Phone', {'PhoneLocationType': '6',
                                   'PhoneTechType': '1'})
        self.phone_code, self.phone = self.seperate_text(phone['PhoneNumber'])
        
        fax = phone_detail.find('Phone', {'PhoneLocationType': '6',
                                   'PhoneTechType': '3'})
        
        self.fax_code, self.fax = self.seperate_text(fax['PhoneNumber'])
        
        # Country
        tag_country = xml_address.find('CountryName')
        self.country_code = tag_country['Code']
        self.country = tag_country.text
        
        # City
        city_tag = xml_address.find('CityName')
        self.city = city_tag.text
        
        # Postal Code
        postal_tag = xml_address.find('PostalCode')
        self.post_code = postal_tag.text
        
    def seperate_text(self, text: str):
        parts = text.split('/')
        first_part = parts[0]
        second_part = parts[1]
        return first_part, second_part
    
    def get_roooms(self):
        rooms_segment = self.hotel_repo.find('FacilityInfo')
        rooms_list = rooms_segment.find_all('GuestRoom')

        # List to store structured data
        structured_data = []
        
        # Process each GuestRoom element
        for room in rooms_list:
            room_data = {'Code': room.get('Code')}
            
            # Extract TypeRoom information
            type_room = room.find('TypeRoom')
            if type_room:
                room_data['TypeRoom'] = {'Name': type_room.get('Name')}
            
            # Extract Description information
            description = room.find('Description')
            if description:
                room_data['Description'] = description.find('Text').text.strip()

            # Extract MaxOccupancy information
            room_data['MaxOccupancy'] = room.get('MaxOccupancy')
            
            # Append room_data to structured_data
            structured_data.append(room_data)
            
        # Extract Amenities information
        # Code ALL is for room amenity
            
        # Print the structured data
        for data in structured_data:
            if data['Code'] == 'ALL':
                structured_data.remove(data)
            print(data)       
    
# Testing      
end_time = time.perf_counter()

hotel_list = ['0563']
for hotel in hotel_list:
    repo = AccorRepo(hotel)
    repo.get_roooms()

# time the code
start_time = time.perf_counter()
elapsed_time = start_time - end_time

print(f"Elapsed time: {elapsed_time} seconds")
