from bs4 import BeautifulSoup
import urllib
#import datetime
import pandas as pd
import time
import re

url_step_raw = pd.read_csv('../../data/00_source/url_step.csv', sep="|")

url_step = url_step_raw['week_url']
week_date = url_step_raw['week']
#match_type = [472, 473, 474, 475, 476]
match_type = [472, 473]

def get_link(weeks, match, page):
    hit_link = 'https://bwf.tournamentsoftware.com/ranking/category.aspx?id={}&category={}&C{}FOC=&p={}&ps=25'.format(weeks, match, match, page)
    response = urllib.request.urlopen(hit_link)
    raw_html = response.read()
    soup_html = BeautifulSoup(raw_html, 'html.parser')
    time.sleep(15) #sleep for 3 seconds
    return soup_html

for match in match_type:
    for weeks in url_step:
        #weeks = 17811
        player_ranks = []
        soup_html = get_link(weeks, match, 1) 
        
        get_page = soup_html.findAll('span', attrs={'class': 'page_caption'})
        page_text = get_page[0].text
        page_split = page_text.split()
        total_pages = page_split[3]
        
        rankdate = soup_html.findAll('span', attrs={'class': 'rankingdate'})
        rankdate_text = rankdate[0].text
        datetime_string = rankdate_text.strip("()")
#        datetime_string = rankdate_split.replace("/","_")
        
        for pages in range(1,int(total_pages)+1):
            print('Match type: ' + str(match) + ', Week: ' + str(weeks) + ', Page ' + str(pages) + ' of ' + str(total_pages))
            soup_html = get_link(weeks, match, pages) 
            page_table = soup_html.find('table', attrs={'class':'ruler'})
            table_elements = page_table.find_all('tr')
            for t_step in range(2, len(table_elements)-1):
                player_slice = table_elements[t_step]
                td_split = player_slice.find_all('td')
                step_rank = td_split[0].text    
                step_country = td_split[3].text
                
                href_split = player_slice.findAll('a', href=True)
                get_id = str(href_split[0])
                result = re.search('player=(.*)">', get_id)
                step_id = result.group(1)
                
                step_list = {'week': weeks, 
                             'date': datetime_string,
                             'rank': step_rank, 
                             'country': step_country, 
                             'pid': step_id}
            
                player_ranks.append(step_list)
                
        player_rank_df = pd.DataFrame(player_ranks)
        filename = "../../data/00_source/rank/{}/{}.csv".format(match,weeks)
        player_rank_df.to_csv(filename, index=False, sep='|')