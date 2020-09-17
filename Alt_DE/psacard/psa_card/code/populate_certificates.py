# Module to scrap fine-grain details associated with a given certificate id
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import os
import re
from dateutil.parser import parse

# Selenium Driver Handler
def load_driver(SELENIUM_EXECUTABLE_PATH=r'/mnt/c/Users/adity/Downloads/Chrome/geckodriver-v0.27.0-win64/geckodriver.exe'):
    driver = webdriver.Firefox(executable_path=SELENIUM_EXECUTABLE_PATH)
    return driver

# Utility to write as .csv file format
def save_to_csv(data, SAVE_PATH, MODE):
    flag = os.path.isfile(SAVE_PATH)
    if not os.path.exists(SAVE_PATH.split('/')[0]):
        os.makedirs(SAVE_PATH.split('/')[0])

    fileWriter = csv.DictWriter(open(SAVE_PATH, MODE), data[0].keys(), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    if not flag:
        fileWriter.writeheader() # Loading header only once, i.e., first-time load
    fileWriter.writerows(data)

# Data-field validation (data-integrity)
def validate_date(date):
    try:
        parse(date)
        return True
    except ValueError:
        return False

# Cleaning noisy, structureless field to extract reference URL
def format_registry_url(str_msg):
    try:
        url_ref = ''
        if 'href' in str_msg:
            href_subset = str_msg[str_msg.index('href')+6:]
            url_ref = '/'.join(BASE_PATH.split('/')[:-1]) + href_subset[:href_subset.index('">')]
        return url_ref
    except:
        return None

# Fetch a dataframe row as an unique set
def get_particular_unique_rows(file_path, index):
    rows = []
    try:
        with open(file_path) as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            for row in data:
                if row[index] not in rows:
                    rows.append(row[index])
    except:
        pass
    return rows

# Main handler controlling certificate parsing
def persist_certification_details(certificate_id, SAVE_PATH='logs/certificate.csv'):
    BASE_PATH='https://www.psacard.com/cert'
    url = '/'.join([BASE_PATH, certificate_id])
    driver = load_driver()
    driver.get(url)
    soup=BeautifulSoup(driver.page_source, features="lxml")
    driver.quit()

    certificate_details = soup.find_all("div", attrs={"class": "cert-container"})[0].findAll('tr')[2:]
    if len(certificate_details) == 0:
        return

    # Certificate Map is the dataframe we are interested in growing in our scrapping scheme
    certificate_map = {'certificate_number': certificate_id}
    ptr = 0
    try:
        if not len(certificate_details[0].contents[-1].contents[0]) == 4:
            certificate_map['reverse_cert_number'] = certificate_details[ptr].contents[-1].contents[0]
            ptr += 1
        else:
            certificate_map['reverse_cert_number'] = None
    except:
        certificate_map['reverse_cert_number'] = None

    certificate_map['year'] = certificate_details[ptr].contents[-1].contents[0]
    ptr += 1
    certificate_map['brand'] = certificate_details[ptr].contents[-1].contents[0]
    ptr += 1
    certificate_map['sport'] = certificate_details[ptr].contents[-1].contents[0]
    ptr += 1
    certificate_map['card_number'] = certificate_details[ptr].contents[-1].contents[0]
    ptr += 1
    certificate_map['player'] = certificate_details[ptr].contents[-1].contents[0]
    ptr += 1
    certificate_map['variety_or_pedigree'] = certificate_details[ptr].contents[-1].contents[0]
    ptr += 1
    certificate_map['grade'] = certificate_details[ptr].contents[-1].contents[0]
    ptr += 1

    # Adding PSA Auction Prices Realized
    realized_auction_prices = soup.find_all('table', attrs={"class": "apritem-results"})[0].findAll('tr')
    date = realized_auction_prices[0].contents[-1].contents[0]
    if validate_date(date):
        certificate_map['date'] = date
        certificate_map['price'] = realized_auction_prices[1].contents[-1].contents[0]
        certificate_map['auction_house'] = realized_auction_prices[2].contents[-1].contents[0]
        certificate_map['lot_number'] = realized_auction_prices[3].contents[-1].contents[0]
    else:
        certificate_map['date'] = certificate_map['price'] = certificate_map['auction_house'] = certificate_map['lot_number'] = None

    # Adding current PSA registry sets
    registry_sets = soup.find_all('div', attrs={"class": "col-xs-12"})
    certificate_map['registry_set_msg'] = str(soup.find_all('p')[3].contents)
    certificate_map['registry_set_url'] = format_registry_url(certificate_map['registry_set_msg'])
    certificate_map['population'] = registry_sets[0].find('span').contents[0]
    certificate_map['population_w_equal'] = registry_sets[1].find('span').contents[0]
    certificate_map['population_higher'] = registry_sets[2].find('span').contents[0]

    # Save to CSV
    save_to_csv([certificate_map], SAVE_PATH, 'a')
    return

def main():
    # Main entry point to iterate over all incremental (new) certificates loaded
    # - This utility only differntially runs for new certificates
    TRANSACTION_FILE_PATH = 'logs/transaction.csv'
    CERTIFICATION_FILE_PATH = 'logs/certificate.csv'
    existing_certificates_in_transaction = set(get_particular_unique_rows(TRANSACTION_FILE_PATH, 11))
    existing_certificates_in_certificates = set(get_particular_unique_rows(CERTIFICATION_FILE_PATH, 0))
    new_certificates = existing_certificates_in_transaction - existing_certificates_in_certificates

    # Iterating over new certificates to load them into our ecosystem (raw-layer)
    for new_certificate in new_certificates:
        persist_certification_details(new_certificate)

    print ("Total New Certificates Added = ", len(new_certificates))

# Capability for stand-alone execution
if __name__ == '__main__':
    main()
