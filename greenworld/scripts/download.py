import urllib.request
import pandas as pd
import shutil
import ssl
import re
import os
from greenworld.lib import Greenworld

# Convert some Excel file into CSV form
def excel_to_csv(filepath):
    dest = re.sub('\.[a-z]+$', '.csv', filepath)
    data = pd.read_excel(filepath)
    data.to_csv(dest, header = False, index = False)

# Download a file from the internet
def download(filepath, url):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    data = urllib.request.urlopen(url, context = context).read()
    with open(filepath, 'wb') as file:
        file.write(data)

def main(gw):
    shutil.rmtree('referenced-data')
    os.mkdir('referenced-data')

    # Clements & Long (1923) - https://iwdb.nceas.ucsb.edu/html/clements_1923.html
    gw.log('Downloading from Clements & Long (1923)...')
    download('referenced-data/clements_1923.xls', 'https://iwdb.nceas.ucsb.edu/data/plant_pollinator/excel/clements_1923.xls')
    excel_to_csv('referenced-data/clements_1923.xls')

    # USDA Plants Database - https://plants.usda.gov/home/downloads
    gw.log('Downloading from USDA Plants Database...')
    download('referenced-data/usda_plants_database.csv', 'https://plants.usda.gov/assets/docs/CompletePLANTSList/plantlst.txt')

    # Entomological Society of America - https://www.entsoc.org/publications/common-names
    gw.log('Downloading from Entomological Society of America...')
    download('referenced-data/Common_names_list_07-30-23.xlsx', 'https://entsoc.org/sites/default/files/files/Common_names_list_07-30-23.xlsx')

if __name__ == '__main__':
    main(Greenworld())