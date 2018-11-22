from bs4 import BeautifulSoup
import urllib
from string import ascii_uppercase

def get_ListOfPlayers():
    for char in ascii_uppercase:
        print(char)
        hit_link = 'http://bwfbadminton.com/players/?char={}&country=&page_size=20000&page_no=1'.format(char)
        response = urllib.request.urlopen(hit_link)
        raw_html = response.read()
        soup_html = BeautifulSoup(raw_html, 'html.parser')    
        filename = "../../data/01_raw/bwf_html/player_list_{}.html".format(char)
        with open(filename, "w") as file:
            file.write(str(soup_html))
            
def get_Tourneys(years):
#    http://bwfbadminton.com/calendar/2018/all/
    for get_year in years:
        print(get_year)
        hit_link = 'http://bwfbadminton.com/calendar/{}/all/'.format(get_year)
        response = urllib.request.urlopen(hit_link)
        raw_html = response.read()
        soup_html = BeautifulSoup(raw_html, 'html.parser')    
        filename = "../../data/01_raw/bwf_html/tourney_{}.html".format(get_year)
        with open(filename, "w") as file:
            file.write(str(soup_html))
            
def get_PlayerRankings(weeks, years):
#http://bwfbadminton.com/rankings/2/bwf-world-rankings/6/men-s-singles/2018/31/?rows=100&page_no=1
#http://bwfbadminton.com/rankings/1/bwf-junior-rankings/1/men-s-singles/2018/31/?rows=100&page_no=1
#http://bwfbadminton.com/rankings/9/hsbc-race-guangzhou/57/men-s-singles/2018/31/?rows=100&page_no=1
    for get_year in years:
        for get_week in weeks:
            print('Year: {}, Week: {}'.format(get_year, get_week))
            hit_link = 'http://bwfbadminton.com/rankings/2/bwf-world-rankings/6/men-s-singles/{}/{}/?rows=500&page_no=1'.format(get_year, get_week)
            response = urllib.request.urlopen(hit_link)
            raw_html = response.read()
            soup_html = BeautifulSoup(raw_html, 'html.parser')    
            filename = "../../data/01_raw/bwf_html/player_rank_bwf_wr_{}_{}.html".format(get_year, get_week)
            with open(filename, "w") as file:
                file.write(str(soup_html))


#get_ListOfPlayers()
get_years = ['2014', '2015', '2016', '2017', '2018']
#get_Tourneys(get_years)
    
get_weeks = range(1,31)
get_PlayerRankings(get_weeks, ['2018'])           
