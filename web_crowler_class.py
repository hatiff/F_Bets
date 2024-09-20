from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
from pathlib import Path
from pathlib import Path
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.implicitly_wait(3)
url = 'https://www.oddsportal.com/results/#soccer'
driver.get(url)




def get_links(xpath):
    links_array = []
    print("Getting links")
    block = driver.find_element_by_xpath(xpath)
    links = block.find_elements_by_xpath(".//a")
    for link in links:
        link = link.get_attribute("href")
        links_array.append(link)
    return links_array

def get_odds(folder_name, file_name):
    print("Getting odds")
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #time.sleep(5)
    
    last_height = 0
    while True:
    # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # wait for the remaining elements to be loaded
    try:
        page = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/main/div[2]/div[7]/div[1]')
        Path('Archive/' + folder_name).mkdir(parents=True, exist_ok=True)
        with open('Archive/' + folder_name + '/' + file_name + '.txt', "a") as myfile:
            myfile.write(page.text)
    except:
        print("No text: ", file_name)
    #page = driver.find_element_by_xpath('//*[@id="W6yHo7aQ"]')

    
    #return page.text
 

def years_block():
    print("Getting years")
    years_links = []
    try:
        years = get_links('//*[@id="app"]/div/div[1]/div/main/div[2]/div[6]/div[2]/div[2]') 
    except:
        return years_links
    for year in years:
        pass_year = False
        for str_year in str_array:
            if str_year in year:
                pass_year = True
                break
        if pass_year:
            continue
        else:
            years_links.append(year)
        
    return years_links
        

def pages_block(year):
    print("getting pages")
    pages_links = []
    try:
        pages = driver.find_elements_by_xpath('//*[@id="pagination"]')
    except:
        return pages_links
    for page in pages:
        if len(page.text) > 1:
            for number in page.text:
                if number.strip():
                    if number == '1':
                        pages_links.append(year)
                        continue
                    pages_links.append(year + "#/page/" + number + "/")
    return pages_links


if __name__ == '__main__':
    years_array = list(range(1950, 2020))
    str_array = [str(num) for num in years_array]
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    country_links = get_links('//*[@id="app"]/div/div[1]/div/main/div[2]/div[6]/div[3]')
    print(len(country_links))
    # Print the href attribute of each link
    count = 0
    for tournament_link in country_links:
        folder_name = tournament_link.split('/')[4]
        years = False
        with open('Archive/Finished.txt') as f:
            if tournament_link in f.read():
                count += 1
                print("passing by")
                print("Left: ", len(country_links) - count)
                continue
        if len(tournament_link.split('/')) < 7:
            continue
        count += 1
        driver.get(tournament_link)  #open country/cup/legue 
        years_links = years_block()
        if len(years_links) != 0:
            for year in years_links:
                driver.get(year)
                pages_links = pages_block(year)
                file_name = year.split('/')[5]
                if len(pages_links) != 0:
                    for page_link in pages_links:
                        if page_link == year:
                            text = get_odds(folder_name, file_name) 
                            continue
                        driver.get(page_link)
                        driver.refresh()
                        text = get_odds(folder_name, file_name)
                else:
                    text = get_odds(folder_name, file_name)
        else:
            pages_links = pages_block(tournament_link)
            file_name = tournament_link.split('/')[4]
            if len(pages_links) != 0:
                for page_link in pages_links:
                    if page_link == tournament_link:
                        text = get_odds(folder_name, file_name)
                        continue
                    driver.get(page_link)
                    driver.refresh()
                    text = get_odds(folder_name, file_name)
            else:
                text = get_odds(folder_name, file_name)
        with open('Archive/Finished.txt', "a") as myfile:
            myfile.write(tournament_link)
        print("Done: ", count)
        print("Left: ", len(country_links) - count)
        time.sleep(30)
