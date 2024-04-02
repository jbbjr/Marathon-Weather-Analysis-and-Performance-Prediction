# scraping needs
import requests
from bs4 import BeautifulSoup

# selenium stuff for website navigation
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# structures & file formats
from collections import deque
import pickle
import pandas as pd

# misc
from time import sleep
import urllib.parse
import os

# db stuff
from google.cloud import bigquery
import os

# gets the URLs for a given year of marathons (a broader URL) and returns them as a Queue
def get_urls(year_url):
    url = year_url
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # find the race links by alphabetical html class
    body_column = soup.find('div', class_='bodyColumn2')

    # get all the <a> tags within <p> tags inside this <div>
    links = body_column.find_all('a', class_='resultsLinksList')

    races = deque()
    for link in links:
        race = link['href']
        race_link = urllib.parse.urljoin(url, race)
        races.append(race_link)
    
    return races


# initializes the crawl for a race, takes a race url and the page it left off at and navigates to said page to start crawling the entire or remainder of the race, void - no return
def begin(race_url, page=int):
    try:
        print(f'scraping {race_url} starting at page {page}')
        driver.get(race_url)
    except:
        print('Could not get url')
        return

    # locate the overall results element select to view the first page of results
    overall_dropdown = Select(driver.find_element(By.XPATH, f"//table[@class='formTable']//tr[1]//select"))
    
    # this try is different from the main try, as driver.get would fail first
    try:
        overall_dropdown.select_by_index(page)
    except:
        print('Race already completed')
        return
    
    # locate and hit the view button to get to the page
    button = driver.find_element(By.NAME, 'SubmitButton')
    button.send_keys(Keys.RETURN)
    

# walks the results pages to bypass anti-scrape measures and calls get_values to construct a race_df
# returns them as a DataFrame, along with a page and boolean to indicate the last unsuccessful page and whether or not the race was finsihed
def crawl(driver, page=int):
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
            return (race_df.drop_duplicates().dropna(), page, False)

        race_df = pd.concat([get_values(html), race_df])

        # try and move to the next page, if it exists
        try:
            print('first page link')
            button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='pageNavLinks']//a/img[contains(@src, 'smallarrow_right.gif')]")
                )
            )
            button.click()
        
        except:
            print('looking for page 2+ link')
            try:
                button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//div[@class='pageNavLinks']//a[1]/img[contains(@src, 'smallarrow_right.gif')]")
                    )
                )
                button.click()
            
            except:
                print('Last page scraped -- move to next race')
                return (race_df.drop_duplicates().dropna(), page, True)


# takes the page source at the current location of the crawl and scrapes the table with bs4, returns a pandas DataFrame
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

# configure what we need to scrape
try:
    # load in our queue
    with open('queue.pkl', 'rb') as pkl:
        races = pickle.load(pkl)

        # initialize races for the year if we need to
        if len(races) <= 0:
            year = input('input the year to scrape: ')
            base_url = f"https://www.marathonguide.com/results/browse.cfm?Year={year}"
            races = get_urls(base_url)
        
        # edge_case for including year
        else:
            with open('year.txt', 'r') as year_mark:
                year = int(year_mark.read())

# queue doesn't exist
except:
    year = input('input the year to scrape: ')
    base_url = f"https://www.marathonguide.com/results/browse.cfm?Year={year}"
    races = get_urls(base_url)

# check where we stopped if scraper was exited
with open('bookmark.txt', 'r') as variables:
    curr_page = int(variables.read())

# check if there are any current pages scraped in the df pkl
if os.path.getsize('race.pkl') > 0:
    existing_race = pd.read_pickle('race.pkl')
else:
    existing_race = None

# initialize things
options = webdriver.ChromeOptions()
service = ChromeService(executable_path='./chromedriver')
driver = webdriver.Chrome(service=service, options=options)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'JSONKEY'       # set credentials (json key file that gives access to BigQuery)
client = bigquery.Client(project='marathondb')
dataset = year

# basic scrape algorithm
while not len(races) <= 0:
    start = curr_page
    race = races[0]
     
    begin(race, start)
    
    try:
        race_data, page, complete = crawl(driver, start)
    except:
        complete = False
        print('Selenium error not caught in function')
        print(f'Placeholder Report\n\nrace: {race}\n\npage: {page}\n\nyear: {year}\n\ncomplete: {complete}')

    # when a race is complete
    if complete:
        print('\nrace completed')
        races.popleft()
        curr_page = 1
        
        # if there was previously scraped content... append it to the new
        if type(existing_race) != None:
            race_data = pd.concat([existing_race, race_data])
            
        print('writing finished race')
        race_data.to_csv(f'{year}_raceindex_{1}_test.csv')
        
        # empty out race placeholder incase we get bumped on a finished race, so they don't overlap
        pd.DataFrame().to_pickle('race.pkl')

    # we need to make changes and hold our place
    else:
        print('\nNew IP edge case')
        
        with open('bookmark.txt', 'w') as variables:
            # in case we hit a weird edge case or error, lets restart the race to be safe
            try:
                variables.write(str(page))
            except:
                variables.write(str(1))
        
        with open('queue.pkl', 'wb') as pkl:
            pickle.dump(races, pkl)    

        with open('year.txt', 'w') as year_mark:
            year_mark.write(str(year))

        race_data.to_pickle('race.pkl')
        break


