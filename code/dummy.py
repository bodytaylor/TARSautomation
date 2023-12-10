main_attractions = {'AER1': ['NE', 'Yes paying', 'On call', 10, 100, 12], 'APT1': ['NE', 'Yes paying', 'Scheduled', 10, 100, 12], 'PCN': ['NE', 'Yes paying', 'Scheduled', 9, 
120, 13], 'PCC': ['NE', 'Yes paying', 'Scheduled', 9, 120, 13], 'NCN': ['NE', 'Yes paying', 'Scheduled', 9, 120, 13], 'NCC': ['NE', 'Yes paying', 'Scheduled', 9, 120, 13], 'CTR1': ['NE', 'Yes paying', 'Scheduled', 4.8, 50, 6], 'CENT': ['NE', 'Yes paying', 'Scheduled', 9, 120, 13], 'HEXI': ['NE', 'No', 'None', 3.7, 10, 10], 'COMP': ['W', 'No', 'None', 1, 5, 1], 'CONG': ['E', 'No', 'None', 8, 95, 11], 'EXHI': ['E', 'No', 'None', 8, 95, 11], 'EXPO': ['E', 'No', 'None', 8, 95, 11]}
    
for code, *info in main_attractions.items():
    ofi, shuttle, shuttle_service_type, distance, minute_walk, minute_drive = info[0]
    print(ofi, shuttle, shuttle_service_type, distance, minute_walk, minute_drive)