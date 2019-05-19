import pandas as pd

from functions import get_soup, \
                        player_rank_total_pages, \
                        player_rank_date, \
                        get_player_rank_details, \
                        get_doubles_rank_details

url_step_raw = pd.read_csv('data/00_source/url_step.csv', sep="|")
url_step = url_step_raw['week_url']
week_date = url_step_raw['week']

match_types = [473, 474, 475]

match_type = 474

for match_type in match_types:
    for i in range(0, len(url_step)):
        step = url_step[i]
    #for step in url_step:
        player_ranks = []
        hit_link = 'https://bwf.tournamentsoftware.com/ranking/category.aspx?id={}&category={}&C{}FOC=&p=1&ps=25'.format(step, match_type, match_type)
        soup_html = get_soup(hit_link)
        total_pages = player_rank_total_pages(soup_html)
        rank_date = player_rank_date(soup_html)
        print(rank_date)
        
        # Step through all player rank pages for that week
        for pages in range(0, int(total_pages)+1):
            hit_link = 'https://bwf.tournamentsoftware.com/ranking/category.aspx?id={}&category={}&C{}FOC=&p={}&ps=25'.format(step, match_type, match_type, pages)
            soup_html = get_soup(hit_link)
            page_table = soup_html.find('table', attrs={'class':'ruler'})
            table_elements = page_table.find_all('tr')
            for i in range(2, len(table_elements)-1):
                if (match_type == 472) | (match_type == 473):
                    player_ranks.append(get_player_rank_details(table_elements[i], step, rank_date))
                else:
                    player_ranks.append(get_doubles_rank_details(table_elements[i], step, rank_date))
        player_ranks_df = pd.DataFrame(player_ranks)
        file_date = rank_date.replace('/', '_')
        filename = "data/00_source/rank/{}/{}.csv".format(match_type,file_date)
        player_ranks_df.to_csv(filename, index=False, sep='|')