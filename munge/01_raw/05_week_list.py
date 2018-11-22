from bs4 import BeautifulSoup
import urllib
import pandas as pd

hit_link = 'https://bwf.tournamentsoftware.com/ranking/category.aspx?id={}&category={}&C{}FOC=&p={}&ps=25'.format(17811, 472, 472, 1)
response = urllib.request.urlopen(hit_link)
raw_html = response.read()
soup_html = BeautifulSoup(raw_html, 'html.parser')

soup_html

rank_week = []
for option in soup_html.find_all('option'):
    if (len(option.text) < 12) & (len(option.text) > 8):
        print ('value: {}, text: {}, len: {}'.format(option['value'], option.text, len(option.text)))
        
        week_det = {
                'week': option.text, 
                'week_url': option['value']}
        rank_week.append(week_det)
        
rank_week_df = pd.DataFrame(rank_week)
filename = "../../data/00_source/url_step.csv"
rank_week_df.to_csv(filename, index=False, sep='|', header=True)