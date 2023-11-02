import pandas as pd

def compare_excel_sheets(file1, file2):
    xls1 = pd.ExcelFile(file1)
    xls2 = pd.ExcelFile(file2)

    sheet_names1 = xls1.sheet_names
    sheet_names2 = xls2.sheet_names

    common_sheets = set(sheet_names1) & set(sheet_names2)

    for sheet_name in common_sheets:
        df1 = pd.read_excel(file1, sheet_name=sheet_name)
        df2 = pd.read_excel(file2, sheet_name=sheet_name)

        diff = df1.compare(df2)

        if diff.empty:
            print(f"No differences found in sheet '{sheet_name}'")
        else:
            print(f"Differences found in sheet '{sheet_name}':")
            print(diff)
            # You can save the differences to a new Excel file if needed
            # diff.to_excel(f'differences_{sheet_name}.xlsx', index=False)

if __name__ == "__main__":
    file1 = 'D:\Hotel Distribution\On going\C265\C265 F_Content Book Hotel Creation Movenpick Living 06 Oct 2023 - Edited.xlsm'
    file2 = 'D:\Hotel Distribution\On going\C265\Copy of F_Content Book Hotel Creation Movenpick Living 06 Oct 2023 - Edited.xlsm'
    compare_excel_sheets(file1, file2)
