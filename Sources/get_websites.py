import io
import requests
import zipfile
import os
import pandas as pd



ALEXA_LIST = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
CURR_DIR = os.path.dirname(os.path.realpath(__file__))+'/'

def get_top_websites():
    if not os.path.exists("AlexaTopSites"):
        os.mkdir("AlexaTopSites")
        print("AlexaTopSites folder created.")

    site_list = os.path.join(CURR_DIR, '/AlexaTopSites', '/top-1m.csv')
    if not os.path.exists(site_list):
        print("top-1m.csv does not exist, downloading a copy.")
        r = requests.get(ALEXA_LIST)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(CURR_DIR+"/AlexaTopSites")

def create_website_config(quantity):
    
    df = pd.read_csv(CURR_DIR+"/AlexaTopSites/top-1m.csv", header=None, usecols=[1])
    new_f = df[:quantity]
    new_f.to_csv(CURR_DIR+"/AlexaTopSites/top-1m.csv", index=False)

    with open(CURR_DIR+"/AlexaTopSites/top-1m.csv", 'r') as fin:
        data = fin.read().splitlines(True)
    with open(CURR_DIR+"/AlexaTopSites/top-1m.csv", 'w') as fout:
        fout.writelines(data[1:])

