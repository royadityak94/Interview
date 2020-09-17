# Module to scrap all auction listings on the auction prices page
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import os

# Utility to write as .csv file format
def save_to_csv(data, SAVE_PATH, MODE):
    if not os.path.exists(SAVE_PATH.split('/')[0]):
        os.makedirs(SAVE_PATH.split('/')[0])

    fileWriter = csv.DictWriter(open(SAVE_PATH, MODE), data[0].keys(), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    fileWriter.writeheader()
    fileWriter.writerows(data)

# Selenium Driver Handler
def load_driver(SELENIUM_EXECUTABLE_PATH=r'/mnt/c/Users/adity/Downloads/Chrome/geckodriver-v0.27.0-win64/geckodriver.exe'):
    driver = webdriver.Firefox(executable_path=SELENIUM_EXECUTABLE_PATH)
    return driver

# Main handler controlling all auction listing parsing
def fetch_auction_items(AUCTION_PRICES_PATH, BASE_PATH, SAVE_PATH, MODE):
    driver = load_driver()
    driver.get(AUCTION_PRICES_PATH)
    soup=BeautifulSoup(driver.page_source, features="lxml")
    auction_items = soup.find_all("table", attrs={"class": "auction-summary-results"})
    auction_data = []

    # Iteratiing over full-auction set
    for item in auction_items:
        item_info = {}
        item_info['name'] = item.find('a').contents[0]
        item_info['url'] = BASE_PATH + item.find('a')['href']
        item_info['count'] = int(item.findAll('td')[-1].contents[0])
        item_info['category'] = 'basketball_cards'
        auction_data.append(item_info)

    # Write to file
    save_to_csv(auction_data, SAVE_PATH, MODE)
    driver.quit()
    return

# Entry-point of the progran
def main():
    BASE_PATH='https://www.psacard.com'
    AUCTION_PRICES_PATH=BASE_PATH + '/auctionprices/#2basketball%20cards%7Cbasketb'
    SAVE_PATH='logs/allauctionprices.csv'
    fetch_auction_items(AUCTION_PRICES_PATH, BASE_PATH, SAVE_PATH, 'w')

# Capability for stand-alone execution
if __name__ == '__main__':
    main()
