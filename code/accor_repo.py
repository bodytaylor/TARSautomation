import requests
from bs4 import BeautifulSoup
from typing import Optional
import time
import pandas as pd

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
    
    def get_iata(self):
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
                if self.airport_unit == 'Km':
                    self.airport_distance_m = round((float(self.airport_distance) * 0.621371))
                else:
                    self.airport_distance_m = self.airport_distance

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
        self.hotel_commercial_name = self.hotel_repo['HotelName']
        self.hotel_name = self._get_field('HotelInfo', 'HotelName', 'HotelShortName')
        
    def get_hotel_address(self):
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
        
        try:
            self.phone_code, self.phone = self.seperate_text(phone['PhoneNumber'])
        except TypeError:
            self.phone_code, self.phone = None, None
        
        fax = phone_detail.find('Phone', {'PhoneLocationType': '6',
                                   'PhoneTechType': '3'})
        try:
            self.fax_code, self.fax = self.seperate_text(fax['PhoneNumber'])
        except TypeError:
            self.fax_code, self.fax = None, None
        
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
                
        return structured_data
    
    def checkin_time(self):
        """Return Hotel Checkin time in format hh:mm"""
        policies = self.hotel_repo.find('Policies') 
        checkin_time = policies.find('PolicyInfo', {'CheckInTime': True})
        str_time = checkin_time['CheckInTime']
        str_time = str_time[:-3]
        return str_time
        
    def checkout_time(self):
        """Return Hotel Checkout time in format hh:mm"""
        policies = self.hotel_repo.find('Policies') 
        checkout_time = policies.find('PolicyInfo', {'CheckOutTime': True})
        str_time = checkout_time['CheckOutTime']
        str_time = str_time[:-3]
        return str_time
    
    def hotel_brand(self):
        """Return 3 letters Hotel Brand Code"""
        brand = self.hotel_repo['BrandCode']
        return brand
    
    def get_attractions(self):
        """Return dataframe of Attractions near by the Hotel"""
        area_info = self.hotel_repo.find('AreaInfo')
        attractions = area_info.find_all('Attractions')
        
        attraction_category_codes = []
        attraction_names = []
        directions = []
        distances = []
        distance_units = []
        index_point_codes = []
        to_from_list = []

        # Iterate through Attraction elements
        for attraction_elem in attractions:
            for attraction in attraction_elem.find_all('Attraction'):
                attraction_category_code = attraction['AttractionCategoryCode']
                attraction_name = attraction['AttractionName']
                attraction_category_codes.append(attraction_category_code)
                attraction_names.append(attraction_name)

            # Iterate through RefPoint elements
            for ref_point_elem in attraction_elem.find_all('RefPoint'):
                direction = ref_point_elem.get('Direction')
                distance = ref_point_elem.get('Distance')
                distance_unit = ref_point_elem.get('DistanceUnitName')
                index_point_code = ref_point_elem.get('IndexPointCode')
                to_from = ref_point_elem.get('ToFrom')

                # Append data to lists
                directions.append(direction)
                distances.append(distance)
                distance_units.append(distance_unit)
                index_point_codes.append(index_point_code)
                to_from_list.append(to_from)

        # Create a DataFrame
        df = pd.DataFrame({
            'AttractionCategoryCode': attraction_category_codes,
            'AttractionName': attraction_names,
            'Direction': directions,
            'Distance': distances,
            'DistanceUnitName': distance_units,
            'IndexPointCode': index_point_codes,
            'ToFrom': to_from_list
        })
        
        # Add new column with mile distance
        df['DistanceMiles'] = df.apply(lambda row: round((float(row['Distance']) * 0.621371), 0) if row['DistanceUnitName'] == 'Km' else row['Distance'], axis=1)
        return df
    
    def get_ref_point(self):
        """Return dataframe of Attractions near by the Hotel"""
        area_info = self.hotel_repo.find('RefPoints')
        attractions = area_info.find_all('RefPoint')
        
        names = []
        direction_list = []
        distances = []
        distance_units = []
        index_point_codes = []
        primary_indicaters= []
        shuttle_service = []
        # Parse XML and fill DataFrame
        for xml_element in attractions:
            name = xml_element.get('Name')
            direction = xml_element.get('Direction')
            distance = xml_element.get('Distance')        
            distance_unit = xml_element.get('DistanceUnitName')
            index_point_code = xml_element.get('IndexPointCode')
            primary_indicater = xml_element.get('PrimaryIndicator')
            shuttle = xml_element.find('Transportation', {"TransportationCode": "17"})
            
            # append to list
            names.append(name)
            direction_list.append(direction)
            distances.append(distance)
            distance_units.append(distance_unit)
            index_point_codes.append(index_point_code)
            primary_indicaters.append(primary_indicater)
            
            if shuttle:
                shuttle_service.append(True)
            else:
                shuttle_service.append(False)
     
                # Create a DataFrame
        df = pd.DataFrame({
            'RefPointName': names,
            'Direction': direction_list,
            'Distance': distances,
            'DistanceUnitName': distance_units,
            'IndexPointCode': index_point_codes,
            'ShuttleService' : shuttle_service,
            'PrimaryIndicator': primary_indicaters,
        })
        
        df['DistanceMiles'] = df.apply(lambda row: round((float(row['Distance']) * 0.621371), 0) if row['DistanceUnitName'] == 'Km' else row['Distance'], axis=1)
        return df
    
    def total_room(self):
        """Get the number of available rooms at this hotel."""
        total_room = self.hotel_repo.find('GuestRoomInfo', {"Code" : "28"})
        return total_room.get('Quantity')

