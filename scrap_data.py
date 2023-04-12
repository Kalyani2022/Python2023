from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime


df = pd.DataFrame()

today = datetime.datetime.now()
# print(today.year - 5)
frm_dt = today.year - 5
to_dt = today.year
for y in range(frm_dt, to_dt + 1):
        
    url = f"https://www.timeanddate.com/holidays/india/{y}"
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    content = soup.find('section', class_ = "table-data__table")
    print("~~~~~~~~~~~~~~~~~~~", content.h2.text.strip(), "~~~~~~~~~~~~~~~~~~~~~~~")

    for table in content.find_all('table', class_="table table--left table--inner-borders-rows table--full-width table--sticky table--holidaycountry"):
        head = table.find('thead')
        for col in head.tr.find_all('th'):
            col = col.text
            print(col,"\t\t\t", end= ' | ')
            

        body = table.find('tbody')
        for row in body.find_all('tr'):
            for col in row.find_all('th'):
                val = col.text
                print(val, "\t\t", end= ' | ')
            for col in row.find_all('td'):
                val = col.text
                print(val, "\t\t", end= ' | ')
            print()
    print('\n=============================================================\n')
