import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os

#Set working directory to project file
path = os.path.dirname(__file__)
os.chdir(path)


#Define the search function that will locate the desired item
def search(s):
    general = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'
    new_search = s.replace(' ', '+')
    new = general.format(new_search)
    new += '&page={}'
    return new


#Create an extraction model that will retrieve the desired product information 
def extract(item):
    atag = item.h2.a
    description = atag.text.strip()
    
    url = 'https://www.amazon.com' + atag.get('href')
    try:
        price_parent = item.find('span','a-price')
        price = price_parent.find('span','a-offscreen').text
    except AttributeError:
        return
    
    try:
        rating = item.i.text
        num_review = item.find('span',{'class': 'a-size-base','dir':'auto'}).text
    except:
        rating = ''
        num_review = 0
    result = (description,price,rating,num_review,url)
    
    return result

#Main program function where the the search and extract functions are used to apply the extraction model to the first 20 pages of amazon.
#The data extracted is formatted and added to a csv file named after the desired product. 
def main(item):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    records = []
    url = search(item)
    
    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div',{'data-component-type':"s-search-result"})
        
        for i in results:
            record = extract(i)
            if record:
                records.append(record)
    driver.close()
    
    with open('{}.csv'.format(item), 'w', newline= '', encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['description','Price','Rating','Review Count', 'URL'])
        writer.writerows(records)


search_term = input('What would you like to search Amazon for? ')
main(search_term)