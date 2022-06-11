from asyncio.windows_events import NULL
import json
from pickle import APPEND, TRUE
from urllib.request import urlopen
from pprint import pprint
from datetime import datetime, date, timedelta
import ctypes
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
import time
from RGBMatrixEmulator.adapters import ADAPTER_TYPES
from RGBMatrixEmulator.emulators.options import RGBMatrixEmulatorConfig
from PIL import Image
import re

colors_json = open('colors/teams.json')
team_colors = json.load(colors_json)

#home_team_colors = [x for x in team_colors if (x['team'] == 'ATL')]


## Pull In Schedule For Given Day
date = date.today().strftime("%Y-%m-%d")
#'2022-06-10'
url = "https://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/2022/league/10_full_schedule.json"
response = urlopen(url)
data_json = json.loads(response.read())

all_games = []

league_schedule = data_json["lscd"]
for month in league_schedule:
    month_schedule = month['mscd']
    for game in month_schedule['g']:
        all_games.append(game)

preference_games = [x for x in all_games if (x['gdte'] == date) and (x['h']['ta'] == 'MIN')]

game_id = preference_games[0]['gid']

url = "https://data.wnba.com/data/10s/v2015/json/mobile_teams/wnba/2022/scores/gamedetail/" + game_id + "_gamedetail.json"
response = urlopen(url)
data_json = json.loads(response.read())['g']

print_this = re.sub(':.*','',re.sub(' +', ' ',data_json['lpla']['de']))

last_play_desc = re.sub(' : ',':',re.sub('(.*\] )','',re.sub(' +', ' ',data_json['lpla']['de'])))
if len(last_play_desc) >= 15:
    last_play_desc_1 = last_play_desc[:15]
    last_play_desc_2 = '- ' + last_play_desc[15:]
else:
    last_play_desc_1 = last_play_desc
    last_play_desc_2 = ''


pprint(preference_games[0])
