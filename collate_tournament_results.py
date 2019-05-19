import pandas as pd
from os import listdir
from os.path import isfile, join
import re
mypath = 'data/00_source/tournament_results/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

full_results = []
for i in onlyfiles[0:3]:
    filename = i
    data = pd.read_csv(mypath + filename, sep = '|')
    full_results.append(data)

full_results = pd.concat(full_results, axis=0)

player_names = full_results[['p1a', 'p1b', 'p2a', 'p2b']]
player_names = player_names.stack().reset_index().rename(columns={0:'player_name'})
player_names = player_names.drop(['level_0', 'level_1'], axis=1)
player_names = player_names[player_names['player_name'] != 'none']
player_names['player_name'] = player_names['player_name'].drop_duplicates()
player_names = player_names['player_name'].dropna()

mult = re.compile('\[.+?\]\s*')

player_names = player_names.str.replace(mult, '')
player_names = player_names.drop_duplicates().dropna()



player_list = pd.read_csv('data/01_raw/player_profile.csv', sep='|')

new_col = player_list['player_page'].str.split('/', expand = True)
player_list['pid'] = pd.to_numeric(new_col[4])

# Need to join based on first and last names