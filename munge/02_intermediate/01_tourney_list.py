import pandas as pd
tourney_list = pd.read_csv('../../data/01_raw/tournament_year.csv', sep="|")

# Fix data
name_replace='https://bwfworldtour.bwfbadminton.com/tournament/3317/hsbc-bwf-world-tour-finals-2018/'
tourney_list['t_web_link'][928] = name_replace

tourney_id_list=[]
for step in range(0,len(tourney_list)):
    t_url=tourney_list['t_web_link'][step]
    if t_url != 'none':
        url_split = t_url.split('/')
        tourney_id = url_split[4]        
    else:
        tourney_id = ''
    t_id={
                't_id': tourney_id}        
    tourney_id_list.append(t_id)
    
t_id_df=pd.DataFrame(tourney_id_list)    

tourney_list = tourney_list.assign(t_id_df=t_id_df.values)
tourney_list = tourney_list.rename(columns={'t_id_df':'t_id'})
filename = "../../data/02_intermediate/tourney_list.csv"
tourney_list.to_csv(filename, index=False, sep='|', header=True)