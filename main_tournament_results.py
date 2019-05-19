import pandas as pd
from functions import get_soup
import re

# Get tournament days
def get_tournament_days(step):
    base_url_hit = 'https://bwf.tournamentsoftware.com/sport/matches.aspx?id='
    url_hit = base_url_hit + step
    soup_html = get_soup(url_hit)
    
    t_days = soup_html.find('ul', attrs={'class':'tournamentcalendar'})
    test = t_days.find_all('li')
    
    base_hit = 'https://bwf.tournamentsoftware.com'
    url_hit_tourney_days = []
    for i in test:
        url_hit_tourney_days.append(base_hit+re.search('href="(.*)"><span', str(i)).group(1))
    return url_hit_tourney_days

def get_game_results(soup_tournament_day, game_scores):
    match_table = soup_tournament_day.find('table', attrs={'class':'ruler matches'})
    match_table = match_table.find_all('tr')
    
    for step_match in match_table:
#    step_match = match_table[8]
        match_type = len(step_match.find_all('tr'))
        if match_type > 0:
            match_det = step_match
            match_step = match_det.find_all('tr')
            if match_type == 2:
                match_type = 'singles'
                p1a = match_step[0].text.split('[')[0].replace('\n', '')
                p2a = match_step[1].text.split('] ')[1].replace('\n', '')
                p1b = 'none'
                p2b = 'none'
                match_duration = match_det.find_all('td')[13].text
    #            a = match_det.find_all('td')[10].text.split(' ')
            elif match_type == 4:
                match_type = 'doubles'
                p1a = match_step[0].text.split('[')[0].replace('\n', '')
                p1b = match_step[1].text.split('[')[0].replace('\n', '')
                p2a = match_step[2].text.split('] ')[1].replace('\n', '')
                p2b = match_step[3].text.split('] ')[1].replace('\n', '')
                match_duration = match_det.find_all('td')[17].text
    #            a = match_det.find_all('td')[14].text.split(' ')
            if match_det.find('span', attrs={'class':'score'}) is None:
                a = 'Walkover'
            else:
                a = match_det.find('span', attrs={'class':'score'}).text
            if ((a == 'Walkover') | (a == 'No match')):
                if 'strong' in str(match_step[0]):
                    scores = ['Walkover Win', 'Walkover Loss']
                else:
                    scores = ['Walkover Loss', 'Walkover Win']
                build_list = {
                        'p1a': p1a,
                        'p1b': p1b,
                        'p2a': p2a,
                        'p2b': p2b,
                        'p1_scores': scores[0],
                        'p2_scores': scores[1],
                        'tournament_id': tournament_id,
                        'date': tournament_date,
                        'duration': match_duration,
                        'type': match_type
                        }
                game_scores.append(build_list)
            else:
                a = re.sub("\s+", " ", a.strip())
                a = a.split(' ')
                for i in a:
                    if i == 'Retired':
                        if 'strong' in str(match_step[0]):
                            scores = ['Walkover Win', 'Walkover Loss']
                        else:
                            scores = ['Walkover Loss', 'Walkover Win']
                    else:
                        scores = i.split('-')
                    build_list = {
                            'p1a': p1a,
                            'p1b': p1b,
                            'p2a': p2a,
                            'p2b': p2b,
                            'p1_scores': scores[0],
                            'p2_scores': scores[1],
                            'tournament_id': tournament_id,
                            'date': tournament_date,
                            'duration': match_duration,
                            'type': match_type
                            }
                    game_scores.append(build_list)
    return game_scores

tournament_list = pd.read_csv('data/00_source/tournament_list.csv', sep="|")

skip_list = [14, 21, 32, 52, 54, 57, 61, 63, 67, 69, 88, 93, 94, 95, 96, 116, 121, 122, 126, 129, 136, 138, 149, 155, 171, 177, 178, 179, 180, 183, 188, 194, 198, 200, 201, 204, 231, 233, 237, 241, 268, 270, 271, 282, 285, 293, 298, 324, 325, 340, 343, 362, 363, 367, 371, 375, 377, 383, 387, 405, 425, 430, 437, 453, 461, 465, 471, 474, 476, 479, 491, 492, 503, 518, 520, 522, 526, 533, 534, 537, 539, 547, 559, 570, 584, 590, 594, 600, 613, 623, 624, 647, 657, 658, 659, 685, 686, 702, 723, 760, 764, 807, 815, 818, 823, 831, 835, 836, 849, 850, 858, 875, 876, 878, 881, 890, 891, 898, 936, 942]


for step in range(max(skip_list), len(tournament_list)):
#step = 32
    if step not in skip_list:
    #        print(step)
        tournament_id = tournament_list['tournament_id'][step]
        print('{}: {}'.format(step, tournament_id))
        game_scores = []
        url_hit_tourney_days = get_tournament_days(tournament_id)
        
        test_t = get_soup(url_hit_tourney_days[0])
        
        if 'printonly flag' in str(test_t):
        
            for tourney_day in range(0, len(url_hit_tourney_days)):
                hit_tourney = url_hit_tourney_days[tourney_day]
                tournament_date = hit_tourney.split(';d=')[1]
                soup_tournament_day = get_soup(hit_tourney)
                game_scores = get_game_results(soup_tournament_day, game_scores)
            
            game_scores_df = pd.DataFrame(game_scores)  
            filename = "data/00_source/match_results_{}.csv".format(tournament_id)
            game_scores_df.to_csv(filename, index=False, sep='|', header=True)
        else:
            skip_list.append(step)
            print(skip_list)