import os
from time import sleep

import pandas as pd
import requests

IMAGE_DIR = './images/'
# read csv
df = pd.read_csv('image_urls_20220609.csv') 

# create a folder for saving images if it does not exist
if os.path.isdir(IMAGE_DIR):
    print('already exists')
else:
    os.makedirs(IMAGE_DIR)

# save image
for file_name, yahoo_image_url in zip(df.filename[:50], df.yahoo_image_url[:50]):
    res = requests.get(yahoo_image_url)
    with open(IMAGE_DIR + file_name + '.jpg', 'wb') as f:
        f.write(res.content)
    sleep(2)

