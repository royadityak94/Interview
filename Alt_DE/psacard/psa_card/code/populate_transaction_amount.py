# Module to scrap fine-grain details associated with a given amount on the summary listings

from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import os
import re

# Selenium Driver Handler
def load_driver(SELENIUM_EXECUTABLE_PATH=r'/mnt/c/Users/adity/Downloads/Chrome/geckodriver-v0.27.0-win64/geckodriver.exe'):
    driver = webdriver.Firefox(executable_path=SELENIUM_EXECUTABLE_PATH)
    return driver

# Utility to write as .csv file format
def save_to_csv(data, SAVE_PATH, MODE):
    flag = os.path.isfile(SAVE_PATH)
    with open(SAVE_PATH, MODE) as file:
        fileWriter = csv.DictWriter(file, fieldnames=data[0].keys(), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if not flag:
            fileWriter.writeheader() # Loading header only once, i.e., first-time load
        fileWriter.writerows(data)

# Main handler controlling population parsing
def parse_population_details(population, global_identifiers, tag=None, SAVE_PATH='logs/population_report.csv', MODE='a'):
    BASE_PATH='https://www.psacard.com'
    rel_url = population['href'].split('/')[3:]
    auction_year = rel_url[0]
    population_id = rel_url[-1]
    url = BASE_PATH + population['href']
    driver = load_driver()
    driver.get(url)
    soup=BeautifulSoup(driver.page_source, features="lxml")
    driver.quit()
    all_details = soup.find_all("div", attrs={"class": "dataTables_wrapper"})[0]

    population_arr = []
    for row in all_details.findAll('tr')[1:]:
        population_row = {}
        all_td = row.findAll('td')[1:]
        if len(all_td) == 0:
            continue
        metrices = [th.text.strip() for th in all_details.findAll('th')[3:]]
        auction_meta = str(all_td[0])
        population_row['auction_player'] = auction_meta[auction_meta.index('<strong>')+len('<strong>'):auction_meta.index('</strong>')].strip()
        population_row['auction_league'] = rel_url[1]
        population_row['population_id'] = population_id
        population_row['auction_year'] = auction_year
        population_row['fk_name'], population_row['fk_url'], population_row['fk_count'], population_row['fk_category'] = global_identifiers

        # Collecting all metrices for the player
        idx = 0
        for item in all_td[2:]:
            cells = item.findAll('span')
            population_row[metrices[idx]] = {'Grade': cells[0].contents[0], '+': cells[1].contents[0], 'Q': cells[2].contents[0]}
            idx += 1
        population_arr.append(population_row)


    # Append to the csv file
    save_to_csv(population_arr, SAVE_PATH, MODE)
    return

# Main handler controlling transaction parsing
def parse_amount_details(rel_url, global_identifiers, tag='None', SAVE_PATH='logs/transaction.csv', MODE='a'):
    BASE_PATH='https://www.psacard.com'
    identifiers = rel_url['href'].split('/')[3:]
    auction_name = identifiers[0]
    auction_player = identifiers[1]
    value = rel_url.text
    summary_id = re.sub(r'#.*', '', identifiers[-1])

    url = BASE_PATH + rel_url['href']
    driver = load_driver()
    driver.get(url)
    soup=BeautifulSoup(driver.page_source, features="lxml")
    driver.quit()
    all_details = soup.find_all("div", attrs={"class": "item-lots-summary"})[0].find_all("div", attrs={"class": "item-row"})
    amount_arr = []
    for fine_details in all_details[1:]:
        specifics = {}
        specifics['auction_name'] = auction_name
        specifics['auction_player'] = auction_player
        specifics['value'] = value
        specifics['summary_id'] = summary_id
        specifics['date'] = fine_details['data-date']
        specifics['price'] = fine_details['data-price']
        specifics['grade'] = fine_details['data-gradevalue']
        specifics['lot_number'] = fine_details['data-lot']
        specifics['auction_house'] = fine_details['data-auctionhouse']
        specifics['auction_seller'] = fine_details['data-auctionname']
        specifics['auction_type'] = fine_details['data-auctiontype']
        specifics['cert'] = fine_details['data-cert']
        specifics['tag'] = tag

        specifics['fk_name'], specifics['fk_url'], specifics['fk_count'], specifics['fk_category'] = global_identifiers
        amount_arr.append(specifics)

    # Save to File
    save_to_csv(amount_arr, SAVE_PATH, MODE)
    return

def main():
    # Main entry point to iterate over all associated transactions
    # from auction listing page with a valid URL
    CSV_FILE_PATH='logs/allauctionprices.csv'
    line_number = 0
    with open(CSV_FILE_PATH) as csvfile:
        line_number += 1
        try:
            auction_items= csv.reader(csvfile, delimiter=',')
            for row in auction_items:
                name, url, count, category = row
                if len(url) < 10:
                    continue
                global_identifiers = [name, url, count, category]
                driver = load_driver()
                driver.get(url)
                soup=BeautifulSoup(driver.page_source, features="lxml")
                driver.quit()
                # Iterating across grade_prices
                grade_prices = soup.find_all("table", attrs={"class": "set-items-results"})
                for idx in range(len(grade_prices)-1):
                    specifics = grade_prices[idx].findAll('tr')
                    grade = specifics[0].findAll('td')[-1].contents[0]
                    most_recent_prices = specifics[1].findAll('td')[-1].contents[0]
                    average_price = specifics[2].findAll('td')[-1].contents[0]
                    smr_price = specifics[3].findAll('td')[-1].contents[0]
                    population = specifics[4].findAll('td')[-1].contents[0]
                    pop_higher = specifics[5].findAll('td')[-1].contents[0]

                    # Nested parsing for the quantitative fields, should they
                    # carry an outward link
                    if str(most_recent_prices) != '—':
                        parse_amount_details(most_recent_prices, global_identifiers, 'Most Recent Price')

                    if str(average_price) != '—':
                        parse_amount_details(average_price, global_identifiers, 'Average Price')

                    if str(smr_price) != '—':
                        parse_amount_details(most_recent_prices, global_identifiers, 'SMR Price' )

                    if str(population) != '—':
                        parse_population_details(population, global_identifiers, 'Population')
        except Exception as ex:
            print (">> Error Logging : ", ex)

# Capability for stand-alone execution
if __name__ == '__main__':
    main()
