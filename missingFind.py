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
import re

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


# initializes the crawl for a race, takes a race url and the page it left off at and navigates to said page to start crawling the entire or remainder of the race, returns information regarding race location and date in a tuple, only updates the tuple if edge cases are not hit
def begin(race_url, page=int, info=tuple):
    try:
        print(f'scraping {race_url} starting at page {page}')
        driver.get(race_url)
    except:
        print('Could not get url')
        return info

    # locate the overall results element select to view the first page of results
    overall_dropdown = Select(driver.find_element(By.XPATH, f"//table[@class='formTable']//tr[1]//select"))
    
    race = driver.find_element(By.XPATH, '//*[@id="bodyInnerPageContents"]/p[2]/span').text
    race = re.sub(r'\W+', '_', race)

    # get text values of date and location, have to call soup again and make another request, which is annoying
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    summary_element = soup.find(id="bodyInnerPageContents")
    
    location_img = summary_element.find('img', alt='location icon')
    loc = location_img.next_sibling.strip()

    date_img = summary_element.find('img', alt='calendar icon')
    date = date_img.next_sibling.strip()

    info = (race, loc, date)

    # this try is different from the main try, as driver.get would fail first
    try:
        overall_dropdown.select_by_index(page)
    except:
        print('Race already completed')
        return info
    
    # locate and hit the view button to get to the page
    button = driver.find_element(By.NAME, 'SubmitButton')
    button.send_keys(Keys.RETURN)
    
    return info


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
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='pageNavLinks']//a/img[contains(@src, 'smallarrow_right.gif')]")
                )
            )
            button.click()
        
        except:
            print('looking for page 2+ link')
            try:
                button = WebDriverWait(driver, 5).until(
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
    column_names = [re.sub(r'\W+', '_', th.text.strip()) for th in tbody.find_all('th')]

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


def hold_place():
    global curr_page, races
    with open('./placeholders/bookmark.txt', 'w') as variables:
        # in case we hit a weird edge case or error, lets restart the race to be safe
        try:
            variables.write(str(curr_page))
        except:
            variables.write(str(1))
    
    with open('./placeholders/queue.pkl', 'wb') as pkl:
        pickle.dump(races, pkl)    

    with open('./placeholders/year.txt', 'w') as year_mark:
        year_mark.write(str(year))


# configure what we need to scrape
try:
    # load in our queue
    with open('./placeholders/queue.pkl', 'rb') as pkl:
        races = pickle.load(pkl)

        # initialize races for the year if we need to
        if len(races) <= 0:
            year = input('input the year to scrape: ')
            base_url = f"https://www.marathonguide.com/results/browse.cfm?Year={year}"
            races = get_urls(base_url)
        
        # edge_case for including year
        else:
            with open('./placeholders/year.txt', 'r') as year_mark:
                year = int(year_mark.read())

# queue doesn't exist
except:
    year = input('input the year to scrape: ')
    base_url = f"https://www.marathonguide.com/results/browse.cfm?Year={year}"
    races = get_urls(base_url)
    races.popleft()
    # races = deque(pd.read_csv('./keys/missingagain.csv')['URL'])
    print('loaded in queue')

# check where we stopped if scraper was exited
with open('./placeholders/bookmark.txt', 'r') as variables:
    curr_page = int(variables.read())

# check if there are any current pages scraped in the df pkl
if os.path.getsize('./placeholders/race.pkl') > 0:
    existing_race = pd.read_pickle('./placeholders/race.pkl')
else:
    existing_race = None

# initialize things
options = webdriver.ChromeOptions()
service = ChromeService(executable_path='./chromedriver')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'dbKey.json'       # set credentials (json key file that gives access to BigQuery)
client = bigquery.Client(project='marathondb')
dataset = str(year)

# ensure datasets existence before beginning crawl
try:
    client.get_dataset(f'marathondb.{dataset}')
except:
    print(f'{dataset} dataset non-existent -- Constructing now')
    client.create_dataset(f'marathondb.{dataset}')

# basic scrape algorithm
count = 0
while True:
    driver = webdriver.Chrome(service=service, options=options)
    while not len(races) <= 0:
        start = curr_page
        race = races[0]

        try: 
            info = begin(race, start)
        except:
            print(f'could not begin scrape for {race} at page: {start}')
            hold_place()
            break        

        try:
            client.get_table(f'marathondb.{dataset}.{race.split("=")[1]}')
            print('Race already exists in full, skip')
            races.popleft()
            continue

        except:
            None

        try:
            race_data, curr_page, complete = crawl(driver, start)
        except:
            complete = False
            print('Selenium error not caught in function')
            print(f'Placeholder Report\n\nrace: {race}\n\npage: {curr_page}\n\nyear: {dataset}\n\ncomplete: {complete}')
            break

        # when a race is complete
        if complete:
            # if there was previously scraped content... append it to the new
            if type(existing_race) != None:
                race_data = pd.concat([existing_race, race_data])

            # scraper went too fast edge case
            max_value = driver.current_url.split("&Max=")[1]
            
            # len(race_data) does not always work as places can be missing at times, we will fix this in SQL
            
            try:
                if int(max_value) < race_data['OverAllPlace'].astype(int).max():
                    print('max_value:', max_value, 'type:', type(max_value))
                    print(race_data['OverAllPlace'].astype(int).max())
                    
                    print(f'length of race data {race_data["OverAllPlace"].astype(int).max()} does not match maximum participants: {max_value}')
                    hold_place()
                    race_data.to_pickle('./placeholders/race.pkl')
                    break
            except KeyError:
                print('skip race for faulty data')
                curr_page = 1
                races.popleft()
                break

            print('\nrace completed')
            races.popleft()
            # races.to_pickle('./placeholders/queue.pkl')
            curr_page = 1
            
            print('writing finished race')
            race_data['Race'] = info[0]
            race_data['Location'] = info[1]
            race_data['Date'] = info[2]
            race_data['URL'] = race

            try:
                client.get_table(f'marathondb.{dataset}.{race.split("=")[1]}')
                print('Table exists in database -- appending new contents')
                
                # ref = f'marathondb.{year}.{info[0]}'
                # job_config = bigquery.LoadJobConfig(write_disposition='WRITE_APPEND', autodetect=True)
                # job = client.load_table_from_dataframe(race_data, ref, job_config=job_config)
                # print(job.result())
            except:
                print('Writing Contents to BigQuery')
                client.create_table(f'marathondb.{dataset}.{race.split("=")[1]}')
            
                ref = f'marathondb.{dataset}.{race.split("=")[1]}'
                job_config = bigquery.LoadJobConfig(autodetect=True)
                job = client.load_table_from_dataframe(race_data.drop_duplicates(), ref, job_config=job_config)
                print(job.result())

            # empty out race placeholder incase we get bumped on a finished race, so they don't overlap
            pd.DataFrame().to_pickle('./placeholders/race.pkl')

        # we need to make changes and hold our place
        else:
            print('\nNew IP edge case')
            hold_place()
            race_data.to_pickle('./placeholders/race.pkl')

            break

    print('BRUTE FORECE EDGE CASE')
    print('you should probably have a deque crash if you are actually done')
    driver.quit()
    count += 1
    
    # if we bonk 5 times on the race it is almost certain that it is empty
    if count == 5:
        races.popleft()
        count = 0
        curr_page = 1
        existing_race = None
        print('reset count and skip empty race')
    try:
        races[0]
    except:
        print('queue is empty')
        break
    # driver.quit()
