# packages
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from tqdm import tqdm
import os

# retrives an integer value representing how many columns are in a given table
def getLength():
    length = 0
    col = 1

    while True:
        try:
            colName = '//tbody/tr[2]/th[i]'
            colName = colName.replace('i', str(col))
            driver.find_element(By.XPATH, colName)
            length += 1
            col += 1
        except:
            return length

# takes the value returned from getLength and iterates through that many title elements of a table
# returns a list of column names for the table
def getTitles(columns):
    titles = []
    
    for i in range(1, int(columns) + 1, 1):
        title = '//tbody/tr[2]/th[i]'
        title = title.replace('i', str(i))
        colTitle = str(driver.find_element(By.XPATH, title).text)
        titles.append(colTitle)

    return titles

# gets the values of the table for the current page and returns a temp df that will append to the master df of the race
def getValues(columns, titles):
    df = pd.DataFrame(columns=titles)
    
    for i in range(1, int(columns) + 1, 1):
        values = []
        for j in range(3, 104, 1):
            path = ''
            # path = '//table[2]/tbody/tr[1]/td[2]/table[3]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[j]/td[i]'
            
            # row 1 col 1 returns date if you don't make path more specific
            if i == 1:
                path = '//table[2]/tbody/tr[1]/td[2]/table[3]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[j]/td[i]'
            else:
                path = '//tbody/tr[j]/td[i]'

            try:
                xpath = path.replace("i", str(i)).replace("j", str(j))
                contents = driver.find_element(By.XPATH, xpath)
                values.append(contents.text)
                contents = driver.find_element(By.TE)
            except:
                continue
        
        df[str(titles[i - 1])] = pd.Series(values).astype(str)
    
    return df

# takes a str(URL) for a year of races
# gets the URLs for a given year of marathons (a broader URL) and returns them as a List
def getURLs(yearURL, year):   
    driver.get(str(yearURL))

    URLs = []

    raceLink = '//p/table/tbody/tr/td[2]/a[i]'
    i = restart("path" + year + "/")
    print("starting at " + str(i) + " race")
    while True:
        try:
            iterateLink = raceLink.replace("i", str(i))
            val = driver.find_element(By.XPATH, iterateLink);
            url = str(val.get_attribute('href'))
            URLs.append(url)
            i += 1
        except:
            return URLs

# start over at the last complete race and begin scraping again (good check for when the site boots us)
def restart(path):
    num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    if num_files == 0:
        return 1
    else:
        return num_files

# inpurt the year and create the directory if not exists
year = str(input("enter year to scrape: "))

if not os.path.exists(r"../path" + year):
    os.mkdir(r"../path" + year)
    print("creating path for year")
else:
    print("path exists for year")

# set up our web driver
driver = webdriver.Chrome(executable_path=r"path/chromedriver")

URLs = getURLs('http://www.marathonguide.com/results/browse.cfm?Year=' + str(year), year)

print(URLs)

# main
for link in tqdm(range(len(URLs))):
    driver.get(URLs[link])
    
    raceName = driver.find_element(By.XPATH, '//td/table[1]/tbody/tr/td[1]/b[1]').text
    location = driver.find_element(By.XPATH, '//td/table[1]/tbody/tr/td[1]/b[2]').text
    date = driver.find_element(By.XPATH, '//td/table[1]/tbody/tr/td[1]/b[3]').text
    
    filename = driver.title
    filename = filename.replace(" ", "_").replace("/", "_")
    dir = str(r"path" + year + "/" + str(filename) + ".csv")

    # get the drop down for overall racers
    dropDown = Select(driver.find_element(By.NAME, "RaceRange"))
    dropDown.select_by_index(1)

    # hit view results and move to the next page
    button = driver.find_element(By.NAME, "SubmitButton")
    button.send_keys(Keys.RETURN)

    colAmount = getLength()
    colTitles = getTitles(colAmount)
    temp = getValues(colAmount, colTitles)
    master_df = pd.concat([temp], ignore_index=True)

    go = True
    try:
        nextPage = driver.find_element(By.XPATH, '//td/table/tbody/tr/td[2]/a')
        nextPage.send_keys(Keys.RETURN)
        temp = getValues(colAmount, colTitles)
        master_df = pd.concat([master_df, temp], ignore_index=True)
    except:
        print('none')
        go = False

    # move past 200 and go through rest of race
    go = True
    while go == True:
        try:
            nextPage = driver.find_element(By.XPATH, '//td/table/tbody/tr/td[2]/a[2]')
            nextPage.send_keys(Keys.RETURN)
            temp = getValues(colAmount, colTitles)
            master_df = pd.concat([master_df, temp], ignore_index=True)
        except:
            go = False
            print("no more runners")

    # use these for our API requests
    master_df.insert(len(master_df.columns), 'Date', date)
    master_df.insert(len(master_df.columns), 'Location', location)
    master_df.insert(len(master_df.columns), "Race", raceName)

    print(master_df.head)
    master_df.to_csv(dir)
    print('in folder now!')

driver.quit()
print("year is scraped")
