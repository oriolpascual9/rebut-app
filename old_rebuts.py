import os
import pandas as pd
import re
from src.DataHandler import DataHandler
from src.OutputPDF import OutputPDF

def cleanDataFrame(df):
    clean_df = pd.DataFrame()
    df.fillna('0',inplace=True)
    for index, row in df.iterrows():
        data = row['data']
        importe = row['total']
        nberenars = int(re.search(r'\d+', row['berenars']).group())
        npicapica = int(re.search(r'\d+', row['pica-pica']).group())
        nxuxes = int(re.search(r'\d+', row['xuxes']).group())

        new_row = pd.DataFrame({'data': [data], 'import': [importe], 'berenar':[nberenars], 'pica-pica': [npicapica], 'xuxes':[nxuxes]})
        clean_df = pd.concat([clean_df, new_row])

    return clean_df

if __name__ == '__main__':
    path = '../old_rebuts/'

    filelist = os.listdir(path)

    df = pd.DataFrame()
    for file in filelist:
        tempdf = pd.read_excel(path + file, sheet_name='IVA MLT')
        tempdf.columns = [['data','bi','iva','total','berenars','pica-pica','xuxes']]
        clean_df = cleanDataFrame(tempdf)
        
        df = pd.concat([df, clean_df])

    df['Date'] = pd.to_datetime(df['data'])
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    df['data'] = df['data'].apply(lambda x: x.strftime('%d-%m-%Y'))

    print(df.head(10))

    for index, row in df.iterrows():
        if (row['berenar'] != 0):
            dh = DataHandler(row.to_dict())
            print(row['data'])
            rebuts, no_festa_days = dh.generateRebuts(unhandeled=True)

            i = 0
            for rebut in rebuts:
                OutputPDF(rebut, i).generatePDF()
                i+=1