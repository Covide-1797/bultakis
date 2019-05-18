import pandas as pd

from functions import get_redirect_url, \
                        get_soup, \
                        get_hitlist_tourney_dates, \
                        get_tourney_day_game_list, \
                        get_game_details

def main():
    # Load tourney list
    tourney_list = pd.read_csv('data/01_raw/tournament_year.csv', sep="|")
    
    # Loop through tournament list
    for t_step in (range(905, 0, -1)):
        url_hit_tourney = tourney_list['t_web_link'][t_step]
        if url_hit_tourney != 'none':
            print(url_hit_tourney)
            print(t_step)

            # Get tournament details
            tournament_game_scores = []
            
            # Get tournament ID
            tourney_id = url_hit_tourney.split('/')[4]
            
            # Hit podium page of tourney
            soup_html_tourney = get_soup(get_redirect_url(url_hit_tourney) + 'podium')
            
            # Get tourney dates
            hit_tourney_dates = get_hitlist_tourney_dates(soup_html_tourney)
            
            for tourney_day in hit_tourney_dates:
            
                # Get tourney day game list
                game_list = get_tourney_day_game_list(tourney_day)
                
                # Check if there are any matches being played that day
                if len(game_list) != 0:
                    game_day_split = game_list[0].find_all('li')
                    
                    for game in game_day_split:
                        tournament_game_scores = get_game_details(game, tourney_id, tournament_game_scores)
                    tourney_scores_df = pd.DataFrame(tournament_game_scores)
                    # Save to csv
                    filename = "data/01_raw/tourney_details_{}.csv".format(tourney_id)
                    tourney_scores_df.to_csv(filename, index=False, sep='|', header=True)

if __name__ == '__main__':
    main()