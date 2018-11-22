from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from string import ascii_uppercase
import pandas as pd

# Get player list and url
player_df = pd.DataFrame(columns=['player_name', 'player_page'])

for char in ascii_uppercase:
    print(char)
    char = 'A'
    hit_link = 'http://bwfbadminton.com/players/?char={}&country=&page_size=20000&page_no=1'.format(char)
    req = Request(hit_link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup_html = BeautifulSoup(webpage, 'html.parser')    
    raw_player_list = soup_html.findAll('div', attrs={'class': 'player'})
    for step in raw_player_list:
        for tag in step.findAll('a', title=True):
            p_url = tag['href']
            p_name = tag['title']
        player_df = player_df.append({'player_name': p_name, 'player_page': p_url}, ignore_index=True)

player_df.to_csv('./player_profile.csv',sep = '|', header=True,index=False)