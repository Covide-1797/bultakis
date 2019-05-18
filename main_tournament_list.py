import pandas as pd
from functions import get_tournament_list

year_step = [2014, 2015, 2016, 2017, 2018, 2019]
tournament_list = []
for step in year_step:
    tournament_list = get_tournament_list(step, tournament_list)
tournament_list_df = pd.DataFrame(tournament_list)
filename = "data/00_source/tournament_list.csv"
tournament_list_df.to_csv(filename, index=False, sep='|')