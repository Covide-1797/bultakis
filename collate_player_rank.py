import pandas as pd
from os import listdir
from os.path import isfile, join

mypath = 'data/00_source/rank/472/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

full_rank = []
#for i in onlyfiles[0:3]:
for i in onlyfiles:
    filename = i
    data = pd.read_csv(mypath + filename, sep = '|')
    full_rank.append(data)

full_rank = pd.concat(full_rank, axis=0)
#full_rank['date'] = pd.to_datetime(full_rank['date'])

player_list = pd.read_csv('data/01_raw/player_profile.csv', sep='|')

new_col = player_list['player_page'].str.split('/', expand = True)
player_list['pid'] = pd.to_numeric(new_col[4])
player_rank = pd.merge(full_rank, player_list, on = 'pid', how = 'left')

#player_rank = player_rank.where(player_rank['rank'] <= 500)

rank1_hist = player_rank[player_rank['rank'] == 2]
rank1_hist = rank1_hist.groupby(['player_name','pid'], as_index=True).size().reset_index().rename(columns={0:'count'})

vik = player_rank[player_rank['pid'] == 25831]
vik['date'] = pd.to_datetime(vik['date'])