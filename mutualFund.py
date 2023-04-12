from loguru import logger
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import mysql.connector as mysql
import pymysql
import sqlite3
import sys
from configparser import ConfigParser
import warnings
warnings.simplefilter(action="ignore")
# logger.add('mf_info_extract.log', rotation='10 MB')
# logger.add('mf_details_extract.log', rotation='10 MB')
logger.add('mf_oes_extract.log', rotation='50 MB')


source = requests.get(f'https://www.amfiindia.com/nav-history-download')
soup = BeautifulSoup(source.text, 'lxml')

# Get all Mutual Fund List(mf_list)
mf_list = soup.find('div', class_="ui-widget auto-select").text
mf_list = mf_list.splitlines()
mf_list = mf_list[3:69]
# print(mf_list)

mf_id = soup.find('select', {'id': 'NavDownMFName'})
# get all <options> in a list
options = mf_id.find_all("option")
#print(options)
# for each element in that list, pull out the "value" attribute
values = [o.get("value") for o in options]
values = values[2:]
# print(values)


# connect to database
conn = pymysql.connect(host='localhost',
                        user='root',
                        password='Kalyani2022',
                        db='mutualfund',
                        autocommit=True,
                        local_infile=1)
print(f"Connected to DB: {'mutualfund'}".format('localhost'))


# try:
#     # define table name and list of data
#     table_name = 'mf_info'
#     data_list = list(zip(values, mf_list))

#     # define SQL query for inserting data
#     sql_query = f"INSERT INTO {table_name} (mf_ID, mf_Name) VALUES (%s, %s)"

#     # execute query for each item in the list
#     with conn:
#         # Create cursor and execute Load SQL
#         cursor = conn.cursor()

#         for item in data_list:
#             cursor.execute(sql_query, item)

#         logger.info(f'Succuessfully loaded the table from list.')

#     # close database connection
#     conn.close()

# except Exception as e:
#     print(e)


try:
    with conn:
        # create cursor
        cursor = conn.cursor()
        table_name = 'mf_details'

        for mfid in values:
            try:
                # logger.info(f"Extracting Data for : {mfid}")
                mf_type = '1'
                frm_dt = (date.today() - timedelta(days=1825)).strftime('%d-%b-%Y')
                to_dt = date.today().strftime('%d-%b-%Y')

                nav_url = 'https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?mf=' + mfid \
                    + '&tp=' + mf_type + '&frmdt=' + frm_dt + '&todt=' + to_dt
                # print(nav_url)
                
                try:
                    print(nav_url)
                    stockdata = pd.read_csv(nav_url)
                except Exception as e:
                    print(f"No Data")
                else:
                    mf_df = stockdata.iloc[2:, :]
                    mf_df[['scheme_Code','scheme_name','dividend_payout_growth','dividend_reinvestment','net_asset_value','repurchase_amount',
                    'Sale_amount','invest_date']] = mf_df['Scheme Code;Scheme Name;ISIN Div Payout/ISIN Growth;ISIN Div Reinvestment;Net Asset Value;Repurchase Price;Sale Price;Date'].str.split(';', expand=True)
                    # print(mf_df)
                    mf_df1 = mf_df.iloc[:,1:]
                    # print(mf_df1)
                    # print(type(mf_df1))

                    # with conn:
                    #     # create cursor
                    #     cursor = conn.cursor()
                    #     table_name = 'mf_details'

                    cols = ",".join([str(i) for i in mf_df1.columns.tolist()])
                    logger.info(f" Writing Data For {mfid}")

                    for i,row in mf_df1.iterrows():
                        sql = f"INSERT INTO {table_name} (" + cols + ") VALUES (" + "%s," *(len(row)-1) + "%s)"
                        cursor.execute(sql, tuple(row))

                        # connection.commit()
                    logger.info(f" Write Successful.{mf_df1.shape}")
                    
                # conn.close()            
                
            except Exception as E:
                print(E)
        
        conn.close()

except Exception as ex:
    print(ex)