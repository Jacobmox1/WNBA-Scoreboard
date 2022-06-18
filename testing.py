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

date_today = date.today().strftime("%Y-%m-%d")
url = "https://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/2022/league/10_full_schedule.json"
response = urlopen(url)
data_json = json.loads(response.read())

all_games = []

league_schedule = data_json["lscd"]
for month in league_schedule:
    month_schedule = month['mscd']
    for game in month_schedule['g']:
        all_games.append(game)

use_game = [x for x in all_games if (x['gdte'] == date_today)][1]
natl_broadcasts = [x for x in use_game['bd']['b'] if (x['scope'] == 'natl')]

try:
    natl_tv = natl_broadcasts[0]['disp']
except IndexError:
    natl_tv = ''
