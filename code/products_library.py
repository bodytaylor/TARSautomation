from functions import *
import pandas as pd

csv_path = 'products_lib.csv'
df = pd.read_csv(
    csv_path,
    header=0,
    sep=';'
)

def product_search(code, df):
    if code in df['code'].values:
        row_data = df.loc[df['code'] == code].values[0].astype(str).tolist()
        joined = ','.join(row_data)
        return joined
    else:
        return None

search = product_search('AIRC', df)
print(search)