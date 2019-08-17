#!/usr/bin/env python

import requests
import urllib.request
import time
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from pprint import pprint
import datetime

teams = {}
week = '1'
url = 'https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=2018&year_max=2018&season_start=1&season_end=-1&age_min=0&age_max=99&game_type=A&league_id=&team_id=&opp_id=&game_num_min=0&game_num_max=99&week_num_min={}&week_num_max={}&game_day_of_week=&game_location=&game_result=&handedness=&is_active=&is_hof=&c1stat=pass_att&c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=pass_att&from_link=1'.format(week, week)

response = requests.get(url)

soup = bs(response.text, 'html.parser')


table = soup.find(class_='stats_table')
tbody = table.find('tbody')
tr_tbody = tbody.find_all('tr')

# make a dictionary of all teams
for i in range(33):
    if i != 20:
        try:
            tr = tr_tbody[i]
            team = tr.find('td', {'data-stat': 'team'}).find('a').text
            teams[team] = {
                'pass_yds_per_att': [0],
                'TO_diff': [0],
                'OL-Rank': 0
            }
        except Exception as e:
            print("Error at " + str(i) + " | " + str(e))
            pass

# get data for each week
for week in tqdm(range(16)):
    try:
        week = str(week + 1)
        url = 'https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=2018&year_max=2018&season_start=1&season_end=-1&age_min=0&age_max=99&game_type=A&league_id=&team_id=&opp_id=&game_num_min=0&game_num_max=99&week_num_min={}&week_num_max={}&game_day_of_week=&game_location=&game_result=&handedness=&is_active=&is_hof=&c1stat=pass_att&c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=pass_att&from_link=1'.format(week, week)
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        table = soup.find(class_='stats_table')
        tbody = table.find('tbody')
        tr_tbody = tbody.find_all('tr')
        for i in range(33):
            if i != 20:
                try:
                    tr = tr_tbody[i]
                    team = tr.find('td', {'data-stat': 'team'}).find('a').text
                    pass_yards_per_attempt = float(tr.find('td', {'data-stat': 'pass_yds_per_att'}).text)
                    teams[team]['pass_yds_per_att'].append((sum(teams[team]['pass_yds_per_att']) + pass_yards_per_attempt)/len(teams[team]['pass_yds_per_att']))
                except Exception as e:
                    print("Error at " + str(i) + " | " + str(e))
                    pass
    except Exception as e:
        print("error at week " + week + " | " + str(e))
        break

date = datetime.datetime(2018, 9, 11)
week = datetime.timedelta(days=7)
for i in tqdm(range(16)):
    date_string = date.strftime('%Y-%m-%d')
    try:
        url = "https://www.teamrankings.com/nfl/stat/turnover-margin-per-game?date={}".format(date_string)
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        table = soup.find(class_='datatable')
        tbody = table.find('tbody')
        tr_tbody = tbody.find_all('tr')
        for tr in tr_tbody:
            td_tr = tr.find_all('td')
            team = get_abbrv(td_tr[1].find('a').text)
            to_diff = float(td_tr[2].text)
            teams[team]['TO_diff'].append(to_diff)
        date += week
    except Exception as e:
        print("error at week + " + date_string + " | " + str(e))
        pass


url = 'https://www.footballoutsiders.com/stats/ol'
response = requests.get(url)
soup = bs(response.text, 'html.parser')
table = soup.find(class_='stats')
tbody = table.find('tbody')
tr_tbody = tbody.find_all('tr')
for tr in tr_tbody:
    td_tr = tr.find_all('td')
    team = get_abbrv_2(td_tr[1].text)
    rank = int(td_tr[0].text)
    teams[team]['OL-Rank'] = rank

def team_eff(abbrv, week, at_home):
    team = teams[abbrv]
    passing = 10*team['pass_yds_per_att'][week]
    TO_diff = 10*team['TO_diff'][week]
    rank = team['OL-Rank']
    if at_home:
        bonus = 5
    else:
        bonus = -5
    return passing + TO_diff - rank + bonus

def get_abbrv_2(team):
    if team == 'NO':
        return 'NOR'
    elif team == 'NE':
        return 'NWE'
    elif team == 'GB':
        return 'GNB'
    elif team == 'SF':
        return 'SFO'
    elif team == 'KC':
        return 'KAN'
    elif team =='TB':
        return 'TAM'
    else:
        return team

def get_abbrv(team):
    abbreviations = {
         "Arizona":"ARI",
         "Atlanta":"ATL",
         "Baltimore":"BAL",
         "Buffalo":"BUF",
         "Carolina":"CAR",
         "Chicago":"CHI",
         "Cincinnati":"CIN",
         "Cleveland":"CLE",
         "Dallas":"DAL",
         "Denver":"DEN",
         "Detroit":"DET",
         "Green Bay":"GNB",
         "Houston":"HOU",
         "Indianapolis":"IND",
         "Jacksonville":"JAX",
         "Kansas City":"KAN",
         "Miami":"MIA",
         "Minnesota":"MIN",
         "New England":"NWE",
         "New Orleans":"NOR",
         "NY Giants":"NYG",
         "NY Jets":"NYJ",
         "Oakland":"OAK",
         "Philadelphia":"PHI",
         "Pittsburgh":"PIT",
         "LA Chargers":"LAC",
         "Seattle":"SEA",
         "San Francisco":"SFO",
         "LA Rams":"LAR",
         "Tampa Bay":"TAM",
         "Tennessee":"TEN",
         "Washington":"WAS",
    }
    return abbreviations[team]
