import pandas as pd

from functions import get_soup

tournament_list = pd.read_csv('data/00_source/tournament_list.csv', sep="|")

base_url_hit = 'https://bwf.tournamentsoftware.com/sport/tournament.aspx?id='

url_hit = base_url_hit + tournament_list['tournament_id'][0]

soup_html = get_soup(url_hit)



from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url_hit)
time.sleep(15)
html_source = driver.page_source
driver.quit()
soup_html = BeautifulSoup(html_source, 'html.parser')