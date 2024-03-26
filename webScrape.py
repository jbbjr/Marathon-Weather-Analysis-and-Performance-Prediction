# packages
import requests
from bs4 import BeautifulSoup
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
import re

# gets the URLs for a given year of marathons (a broader URL) and returns them as a list
def get_urls(year_url):
    url = year_url
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # find the race links by alphabetical html class
    body_column = soup.find('div', class_='bodyColumn2')

    # get all the <a> tags within <p> tags inside this <div>
    links = body_column.find_all('a', class_='resultsLinksList')

    races = []
    for link in links:
        race = link['href']
        race_link = urllib.parse.urljoin(url, race)
        races.append(race_link)
    
    return races


def begin(race_url, page):
    driver.get(race_url)
    
    # locate the overall results element select to view the first page of results
    overall_dropdown = Select(driver.find_element(By.XPATH, f"//table[@class='formTable']//tr[1]//select"))
    overall_dropdown.select_by_index(page)


    # locate and hit the view button to get to the page
    button = driver.find_element(By.NAME, 'SubmitButton')
    button.send_keys(Keys.RETURN)
    

# walks the results pages to bypass anti-scrape measures and calls get_values to construct a race_df, returns them as a DataFrame
def crawl(driver, page):
    race_df = pd.DataFrame()

    # do this until we hit the edge case (will continue process through all pages)
    while True:
        sleep(3)
        
        # collect page source and get values accordingly
        html = driver.page_source

        page_values = get_values(html)
        
        # if we get proxy banned on the page we clicked into
        if len(page_values) > 0:
            page += 1
        
        else:
            print('Error collecting page source')


        race_df = pd.concat([get_values(html), race_df])

        # try and move to the next page, if it exists
        try:
            button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='pageNavLinks']//a/img[contains(@src, 'smallarrow_right.gif')]")
                )
            )
            button.click()
        except:
            print('Last page scraped -- move to next race')
            return (race_df.drop_duplicates().dropna(), page)

# takes
def get_values(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    # locate the table element
    table = soup.find('table', class_='colordataTable')

    # go into the <tbody> where the contents are stored
    tbody = table.find('tbody')

    # grab colum names by <th> before going into contents
    column_names = [th.text.strip() for th in tbody.find_all('th')]

    # extract all rows by <tr>
    rows = tbody.find_all('tr')
    
    data = []
    for row in rows:
            # Extract all cells (<td> tags) from the row
            cells = row.find_all('td')

            # Extract text from each cell and print
            row_data = [cell.get_text(strip=True) for cell in cells]
            data.append(row_data)
    
    return pd.DataFrame(data=data, columns=column_names)


# input and year
year = input('input the year to scrape: ')
base_url = f"https://www.marathonguide.com/results/browse.cfm?Year={year}"

# start = check_location()
start = 2

races = get_urls(base_url)

options = webdriver.ChromeOptions()
service = ChromeService(executable_path='./chromedriver')
driver = webdriver.Chrome(service=service, options=options)

for race in races:
    start = 0
    begin(races[7], start)
    df, page = crawl(driver, start)


print(df.info())
print(df)
print(page)

