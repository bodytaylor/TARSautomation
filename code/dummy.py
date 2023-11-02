import pandas as pd

excel_file_path = f'hotel_workbook\B9F8\B9F8.xlsm'
sheet_name = "Roomtypes"
room_df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=8, dtype=str)
room_df = room_df.dropna(subset=['TARS product code'])
room_df = room_df.dropna(axis=1, how='all')
room_df = room_df.drop(columns=['Unnamed: 1'])
room_df = room_df.reset_index(drop=True)
room_df = room_df.drop(index=0)
columns_to_drop = [col for col in room_df.columns if 'Unnamed' in col]
room_df = room_df.drop(columns=columns_to_drop)
room_df = room_df.drop(room_df.index[0:13])

print(room_df)

for index, row in room_df.iterrows():
    print(row['TARS product code'])
