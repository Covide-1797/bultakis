from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import secrets
from random import randint
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def sleep_scrape():
    random_int = randint(5, 15)
    time.sleep(random_int)


def user_agent_randomizer():
    # Read in User Agent list
    f = open('data/00_source/user-agents.txt', "r")
    ua_list = [line.rstrip('\n') for line in f]
    num = secrets.randbelow(len(ua_list)-1)
    return(ua_list[num])


def get_redirect_url(url):
    user_agent = user_agent_randomizer()
    req = Request(url, headers={'User-Agent': user_agent})
    webpage = urlopen(req)
    return webpage.geturl()


def get_soup(url_link):
    user_agent = user_agent_randomizer()
    req = Request(url_link, headers={'User-Agent': user_agent})
    data = urlopen(req)
    webpage = data.read()
    soup_html = BeautifulSoup(webpage, 'html.parser')
#    sleep_scrape()
    return soup_html


def get_hitlist_tourney_dates(soup_html):
    ajax_table = soup_html.findAll('div', attrs={'class':'wrapper-content-results'})
    ajax_el = ajax_table[0].findAll('ul', attrs={'class':'content-tabs'})
    href_split = ajax_el[0].findAll('a', href=True)
    hit_tourney_dates = []
    for i in range(1, len(href_split)-1):
        hit_tourney_dates.append(re.search('href="(.*)">', str(href_split[i])).group(1))
    return hit_tourney_dates


def get_tourney_day_game_list(url_hit):
    soup_html_tourney_day = get_soup(url_hit)
    game_list = soup_html_tourney_day.findAll('ul', attrs={'class':'list-sort-time'})
    return game_list


def get_game_details(game, tourney_id, tournament_game_scores):
    url_hit_game = re.search('href="(.*)" ', str(game))
    
    #Check if there is a game happening on that day
    if url_hit_game is not None:
        url_hit_game = url_hit_game.group(1).replace("&amp;", "&")
    
        soup_html_game = get_soup(url_hit_game)
        game_date = url_hit_game.split('/')[6]
        game_scores = get_game_scores(soup_html_game, game_date, tourney_id, tournament_game_scores)
    else:
        game_scores = tournament_game_scores
    return (game_scores)


def get_game_scores(soup, game_date, tourney_id, tournament_game_scores):
    check_game_type = soup.findAll('div', {'class':'player1-name'})
    if len(check_game_type) == 2:
        game_scores = get_game_score_double(soup, game_date, tourney_id, tournament_game_scores)
    else:
        game_scores = get_game_score_single(soup, game_date, tourney_id, tournament_game_scores)
    return game_scores


def get_game_score_single(soup, game_date, tourney_id, tournament_game_scores):
    # Player 1 id
    p1_chunk = soup.findAll('div', {'class':'player1-name'})
    if len(p1_chunk)==1:
        url_p1 = re.search('href="(.*)">', str(p1_chunk)).group(1)
        p1_split = url_p1.split('/')
        p1_pid = p1_split[4]
    else:
        p1_pid=''
    
    # Player 2 id
    p2_chunk = soup.findAll('div', {'class':'player2-name'})
    if len(p2_chunk)==1:
        url_p2 = re.search('href="(.*)">', str(p2_chunk)).group(1)
        p2_split = url_p2.split('/')
        p2_pid = p2_split[4]
    else:
        p2_pid=''
        
    game_det = soup.findAll('div', {'class':'game-completed-wrap'})
    games_played = len(game_det)
    for c, games in enumerate(game_det, 1):
        games_split = games.find_all('div')
        p1_score = games_split[2].text
        p1_score = p1_score.replace("\t","").replace("\n","")
        p2_score = games_split[4].text
        p2_score = p2_score.replace("\t","").replace("\n","")
        scores = {
                't_id': tourney_id,
                't_date': game_date,
                'games_played': games_played,
                'p1a_pid': p1_pid,
                'p1b_pid': '',
                'p2a_pid': p2_pid,
                'p2b_pid': '',
                'game': c,
                'p1_score': p1_score,
                'p2_score': p2_score}
        tournament_game_scores.append(scores)
    return tournament_game_scores


def get_game_score_double(soup, game_date, tourney_id, tournament_game_scores):
    # Player 1 id
    p1_chunk = soup.findAll('div', {'class':'player1-name'})
    if len(p1_chunk)==2:
        url_p1a = re.findall('href="(.*)">', str(p1_chunk))[0]
        url_p1b = re.findall('href="(.*)">', str(p1_chunk))[1]
        p1_split = url_p1a.split('/')
        p1a_pid = p1_split[4]
        p1_split = url_p1b.split('/')
        p1b_pid = p1_split[4]
    else:
        p1a_pid=''
        p1b_pid=''
    
    # Player 1 id
    p2_chunk = soup.findAll('div', {'class':'player2-name'})
    if len(p2_chunk)==2:     
        url_p2a = re.findall('href="(.*)">', str(p2_chunk))[0]
        url_p2b = re.findall('href="(.*)">', str(p2_chunk))[1]
        p2_split = url_p2a.split('/')
        p2a_pid = p2_split[4]
        p2_split = url_p2b.split('/')
        p2b_pid = p2_split[4]
    else:
        p2a_pid=''
        p2b_pid=''
    
    game_det = soup.findAll('div', {'class':'game-completed-wrap'})
    games_played = len(game_det)
    for c, games in enumerate(game_det, 1):
        games_split = games.find_all('div')
        p1_score = games_split[2].text
        p1_score = p1_score.replace("\t","").replace("\n","")
        p2_score = games_split[4].text
        p2_score = p2_score.replace("\t","").replace("\n","")
        scores = {
                't_id': tourney_id,
                't_date': game_date,
                'games_played': games_played,
                'p1a_pid': p1a_pid,
                'p1b_pid': p1b_pid,
                'p2a_pid': p2a_pid,
                'p2b_pid': p2b_pid,
                'game': c,
                'p1_score': p1_score,
                'p2_score': p2_score}
        tournament_game_scores.append(scores)
    return tournament_game_scores

def player_rank_total_pages(soup_html):
    get_page = soup_html.findAll('span', attrs={'class': 'page_caption'})
    page_text = get_page[0].text
    page_split = page_text.split()
    total_pages = page_split[3]
    return total_pages

def player_rank_date(soup_html):
    rankdate = soup_html.findAll('span', attrs={'class': 'rankingdate'})
    rankdate_text = rankdate[0].text
    datetime_string = rankdate_text.strip("()")
    return datetime_string

def get_player_rank_details(player_slice, step, rank_date):
    td_split = player_slice.find_all('td')
    step_rank = td_split[0].text
    step_country = td_split[3].text
    step_id = td_split[6].text
    
    step_list = {'week': step, 
                 'date': rank_date,
                 'rank': step_rank, 
                 'country': step_country, 
                 'pid': step_id}
    return step_list

def get_tournament_list(year_step, tournament_list):
    url_hit = 'https://bwf.tournamentsoftware.com/find/tournament?StartDate={}-01-01&EndDate={}-12-31&page=100'.format(year_step,year_step)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url_hit)
    time.sleep(15)
    html_source = driver.page_source
    driver.quit()
    soup_html = BeautifulSoup(html_source, 'html.parser')
    tournament_table = soup_html.findAll('div', attrs={'class':'media'})
    
    for step in tournament_table:
        tournament_id = re.search('id=(.*)" title', str(step.findAll('a', attrs={'class':'media__link'}))).group(1)
        tournament_name = step.findAll('span', attrs={'class':'nav-link__value'})[1].text
        tournament_type = step.findAll('span', attrs={'class':'tag tag--soft'})
        if str(tournament_type) != '[]':
            tournament_type = tournament_type[0].text
        else:
            tournament_type = 'none'
        tournament_date = []
        
        for i in step.findAll('time'):
            if i.has_attr('datetime'):
                tournament_date.append(i['datetime'])
        
        tournament_location = step.findAll('span', attrs={'class':'media__subheading'})[0].text.split(' | ')[1]
        
        if str(tournament_name) == '[]':
            tournament_name = 'none'
        if str(tournament_id) == '[]':
            tournament_name = 'none'
        if len(tournament_date) == 1:
            tournament_date.append('none')
            
        tournament_details = {'tournament_id' : tournament_id,
                              'tournament_name': tournament_name,
                              'tournament_type': tournament_type,
                              'tournament_location': tournament_location,
                              'tournament_start': tournament_date[0],
                              'tournament_end': tournament_date[1]}
        tournament_list.append(tournament_details)
    return tournament_list