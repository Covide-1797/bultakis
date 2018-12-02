import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

player_list = pd.read_csv('../../data/01_raw/player_profile.csv', sep="|")
add_player_details = []
for step in range(0,len(player_list)):
    print(str(step+1) + " / " + str(len(player_list)))
    url_hit = player_list['player_page'][step]
    
    url_split = url_hit.split('/')
    pid = url_split[4]
    req = Request(url_hit, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup_html = BeautifulSoup(webpage, 'html.parser')
    temp = soup_html.find_all('div', attrs={'class':'player-profile-header'})  
    if len(temp) != 0:        
        get_ct=temp[0].find(attrs={'class':'player-profile-country-wrap'})
        get_ct2=get_ct.contents[1]
        country=get_ct2.get('title')    
        temp = soup_html.find_all('div', attrs={'class':'player-extra-wrap'})   
        
        get_age=temp[0].find(attrs={'class':'player-age'})
        get_dob=get_age.contents[5].contents[0]
        get_dob = get_dob.replace(" ", "")
        get_dob = get_dob.replace("\n", "")
        
        get_hand=temp[0].find(attrs={'class':'player-handed'})
        get_hand2=get_hand.contents[5].contents[0]
        get_hand2 = get_hand2.replace(" ", "")
        get_hand2 = get_hand2.replace("\n", "")
        
        player_details={
                'name': player_list['player_name'][step],
                'id': pid,
                'page': player_list['player_page'][step],
                'dob': get_dob,
                'hand': get_hand2,
                'country': country}
    else:
        player_details={
                'name': player_list['player_name'][step],
                'id': pid,
                'page': player_list['player_page'][step],
                'dob': '',
                'hand': '',
                'country': ''}
    add_player_details.append(player_details)
    if step%100 == 0:
        player_df = pd.DataFrame(add_player_details)
        filename = "../../data/02_intermediate/player_list_master.csv"
        player_df.to_csv(filename, index=False, sep='|', header=True)
        print('Save file...')
        
player_df = pd.DataFrame(add_player_details)
filename = "../../data/02_intermediate/player_list_master.csv"
player_df.to_csv(filename, index=False, sep='|', header=True)