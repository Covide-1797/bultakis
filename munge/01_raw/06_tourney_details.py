import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import time

def get_soup(url_link):
    req = Request(url_link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup_html = BeautifulSoup(webpage, 'html.parser')    
    time.sleep(15) #sleep for 3 seconds
    return soup_html

#game_score = []
# Load tourney list
tourney_list = pd.read_csv('../../data/01_raw/tournament_year.csv', sep="|")

for t_step in range(0, len(tourney_list)):
    game_score = []
    print("Tourney " + str(t_step) + " of " + str(len(tourney_list)))
#for t_step in range(0, 2):
    url_hit = tourney_list['t_web_link'][t_step]
    print(url_hit)
    if url_hit != 'none':    
        url_split = url_hit.split('/')
        tourney_id = url_split[4]
    
        # Hit podium page of tourney    
        soup_html = get_soup(url_hit+'podium')
        ajax_table = soup_html.findAll('div', attrs={'class':'wrapper-content-results'})  
        ajax_el = ajax_table[0].findAll('ul', attrs={'class':'content-tabs'})      
        href_split = ajax_el[0].findAll('a', href=True)
        
        # All tournament days
        for i in range(1,len(href_split)-1):
            print("Day " + str(i+1) + " of " + str(len(href_split)))
            get_id = str(href_split[i])
            # Url page of day i-th of tourney
            url_day = re.search('href="(.*)">', get_id).group(1)
            day_soup = get_soup(url_day)
            game_table = day_soup.findAll('ul', attrs={'class':'list-sort-time'})  
            game_table_split = game_table[0].find_all('li')
            
            for get_game_details in range(1, len(game_table_split), 2):
                print("Game " + str(get_game_details+1) + " of " + str(len(game_table_split)))
                get_id = str(game_table_split[get_game_details])
                url_match = re.search('href="(.*)" id', get_id).group(1)
                url_match = url_match.replace("&amp;", "&")        
                match_soup = get_soup(url_match)
                
                get_date = url_match.split('/')
                tourney_date = get_date[6]
                # Player 1 id
                p1_chunk = match_soup.findAll('div', {'class':'player1-name'})
                url_p1 = re.search('href="(.*)">', str(p1_chunk)).group(1)
                p1_split = url_p1.split('/')
                p1_pid = p1_split[4]
        
                # Player 2 id
                p2_chunk = match_soup.findAll('div', {'class':'player2-name'})
                url_p2 = re.search('href="(.*)">', str(p2_chunk)).group(1)
                p2_split = url_p2.split('/')
                p2_pid = p2_split[4]
                
                game_det = match_soup.findAll('div', {'class':'game-completed-wrap'})        
                games_played = len(game_det)
                for c, games in enumerate(game_det, 1):
                    games_split = games.find_all('div')
                    p1_score = games_split[2].text
                    p1_score = p1_score.replace("\t","").replace("\n","")
                    p2_score = games_split[4].text
                    p2_score = p2_score.replace("\t","").replace("\n","")
                    scores = {
                            't_id': tourney_id,
                            't_date': tourney_date,
                            'games_played': games_played,
                            'p1_pid': p1_pid,
                            'p2_pid': p2_pid,
                            'game': c,
                            'p1_score': p1_score,
                            'p2_score': p2_score}
#                    print(scores)
                    game_score.append(scores)   
        tourney_scores_df = pd.DataFrame(game_score)  
        filename = "../../data/01_raw/tourney_details_{}.csv".format(tourney_id)
        tourney_scores_df.to_csv(filename, index=False, sep='|', header=True)