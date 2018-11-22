from bs4 import BeautifulSoup
#import urllib
#from string import ascii_uppercase
import pandas as pd
import re
from urllib.request import Request, urlopen

get_years = ['2014', '2015', '2016', '2017', '2018', '2019']
#get_years = ['2018']
tournament_list = []

def get_tourney(sheet):
    temp = sheet
    temp2 = temp.find_all('td')
    get_country = temp2[1].text
    get_country = get_country.replace(" ", "")
    get_country = get_country.replace("\n", "")
    get_name = temp2[3].text
    get_name = get_name.replace(" \n", "")
    get_name = get_name.replace("\n", "")
    get_prize = temp2[4].text
    get_prize = get_prize.replace("\t", "")
    get_prize = get_prize.replace(" ", "")
    get_prize = get_prize.replace("\n", "")
    if get_prize == '-':
        get_prize = 'none'
    get_category = temp2[5].text
    get_category = get_category.replace("\n", "")
    get_city = temp2[6].text
    get_city = get_city.replace("\n", "")
    get_city = get_city.replace(" ", "")
    href_split = temp2[3].findAll('a', href=True)
    if len(href_split) != 0:
        get_link = str(href_split[0])
        get_link = re.search('a href="(.*)">', get_link).group(1)
    else:
        get_link = 'none'
    tourney_details = {
            't_year': year,
            't_name': get_name, 
            't_prize': get_prize,
            't_category': get_category,
            't_city': get_city, 
            't_country': get_country, 
            't_web_link': get_link}
    return tourney_details
    
            
for year in get_years:
    print(year)
#    year = '2018'
    
    url_hit = 'http://bwfbadminton.com/calendar/{}/all/'.format(year)
    req = Request(url_hit, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup_html = BeautifulSoup(webpage, 'html.parser')
#    test = soup_html.findAll('label', attrs={'class': 'category-select'})
    
    start = 1    
    for loop_table in range(1,-1,-1):
        
        if loop_table == 1:
            page_table = soup_html.find('table', attrs={'class':'hover-highlight tblResultLanding clearBorderTop'})  
            table_elements = page_table.find_all('tr')  
            for i in range(1,len(table_elements)):
                get_tourney_details = get_tourney(table_elements[i])
                tournament_list.append(get_tourney_details)   
            
        else:
            page_table = soup_html.find_all('table', attrs={'class':'hover-highlight tblResultLanding '})   
            for months in range(0,len(page_table)):
                table_elements = page_table[months].find_all('tr')  
                for i in range(0,len(table_elements)):
                    get_tourney_details = get_tourney(table_elements[i])
                    tournament_list.append(get_tourney_details)        

tournament_df = pd.DataFrame(tournament_list)    
filename = "../../data/01_raw/tournament_year.csv"
tournament_df.to_csv(filename, index=False, sep='|')