from time import sleep
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import requests
import re

url = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/?page={}'

d_list = []

for i in tqdm(range(1, 11)):
    target_url = url.format(i)
    res = requests.get(target_url)
    sleep(0.5)
    soup = BeautifulSoup(res.text, "html.parser")
    contents = soup.find_all('div', class_='cassetteitem')

    for content in contents:
        detail = content.find('div', class_='cassetteitem-detail')
        table = content.find('table', class_='cassetteitem_other')

        title = detail.find('div', class_='cassetteitem_content-title').text
        address = detail.find('li', class_='cassetteitem_detail-col1').text
        access = detail.find('li', class_='cassetteitem_detail-col2').text
        age = detail.find('li', class_='cassetteitem_detail-col3').text

        tr_tags = table.find_all('tr', class_='js-cassette_link')

        for tr_tag in tr_tags:
            residence_data = tr_tag.find_all('td')
            floor, price, first_fee, capacity = residence_data[2:6]
            fee, management_fee = price.find_all('li')
            deposit, gratuity = first_fee.find_all('li')
            floor_plan, size = capacity.find_all('li')
            d = {
                'title': title,
                'address': address,
                'access': access,
                'age': age,
                'floor': floor.text,
                'fee': fee.text,
                'management_fee': management_fee.text,
                'deposit': deposit.text,
                'gratuity': gratuity.text,
                'floor_plan': floor_plan.text,
                'size': size.text
            }
            d_list.append(d)

df = pd.DataFrame(d_list)
df2 = df.applymap(lambda x: re.sub('\n', ' ', x))
df3 = df2.applymap(lambda x: re.sub('\r', ' ', x))
df4 = df3.applymap(lambda x: re.sub('\t', ' ', x))
df4.to_csv('result.csv', index=None, encoding='utf-8-sig')
