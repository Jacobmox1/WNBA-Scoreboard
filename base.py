import json
from pickle import APPEND, TRUE
from urllib.request import urlopen
from pprint import pprint
from datetime import datetime, date, timedelta
import ctypes
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
from PIL import Image
import re
from math import trunc
from utils import args, led_matrix_options
from numpy import append

command_line_args = args()
matrixOptions = led_matrix_options(command_line_args)

matrix = RGBMatrix(options = matrixOptions)
canvas = matrix.CreateFrameCanvas()
colors_json = open('colors/teams.json')
team_colors = json.load(colors_json)

font_1 = graphics.Font()
font_2 = graphics.Font()
font_1.LoadFont("assets/fonts/patched/4x6.bdf")
font_2.LoadFont("assets/fonts/patched/5x7.bdf")
textColor = graphics.Color(255, 255, 255)

logo = "assets/wnba.png"
logo = Image.open(logo)
matrix.SetImage(logo.convert("RGB"))
time.sleep(5)
logo.close()

while True:    
    def _render_pregame(today_games):
        home_name = today_games['h']['ta']
        home_record = '(' + today_games['h']['re'] + ')'
        vis_name = today_games['v']['ta']
        vis_record = '(' + today_games['v']['re'] + ')'
        tip_time = (datetime.strptime(today_games['utctm'],"%H:%M") - timedelta(hours=5)).strftime("%-I:%M %p")
        game_location = today_games['ac'] + ', ' + today_games['as']
        home_text_Color = graphics.Color(team_colors[today_games['h']['ta']]["text"]["r"], team_colors[today_games['h']['ta']]["text"]["g"], team_colors[today_games['h']['ta']]["text"]["b"])
        vis_text_Color = graphics.Color(team_colors[today_games['v']['ta']]["text"]["r"], team_colors[today_games['v']['ta']]["text"]["g"], team_colors[today_games['v']['ta']]["text"]["b"])
        for x in range(2,43):
            for y in range(0,8):
                canvas.SetPixel(x, y, team_colors[today_games['h']['ta']]["banner"]["r"], team_colors[today_games['h']['ta']]["banner"]["g"], team_colors[today_games['h']['ta']]["banner"]["b"])
        for x in range(0,2):
            for y in range(0,8):
                canvas.SetPixel(x, y, team_colors[today_games['h']['ta']]["accent"]["r"], team_colors[today_games['h']['ta']]["accent"]["g"], team_colors[today_games['h']['ta']]["accent"]["b"])
        for x in range(2,43):
            for y in range(9,17):
                canvas.SetPixel(x, y, team_colors[today_games['v']['ta']]["banner"]["r"], team_colors[today_games['v']['ta']]["banner"]["g"], team_colors[today_games['v']['ta']]["banner"]["b"])
        for x in range(0,2):
            for y in range(9,17):
                canvas.SetPixel(x, y, team_colors[today_games['v']['ta']]["accent"]["r"], team_colors[today_games['v']['ta']]["accent"]["g"], team_colors[today_games['v']['ta']]["accent"]["b"])
        graphics.DrawText(canvas, font_2, 3, 7, home_text_Color, home_name)
        graphics.DrawText(canvas, font_2, 3, 16, vis_text_Color, vis_name)
        graphics.DrawText(canvas, font_1, 19, 7, home_text_Color, home_record)
        graphics.DrawText(canvas, font_1, 19, 16, vis_text_Color, vis_record)
        graphics.DrawText(canvas, font_1, 1, 24, textColor, tip_time)
        graphics.DrawText(canvas, font_1, 1, 30, textColor, game_location)
        matrix.SwapOnVSync(canvas)
    

    def _render_game(today_games):
        for q in range(1,5):    
            home_name = today_games['hls']['ta']
            home_score = str(today_games['hls']['s'])
            vis_name = today_games['vls']['ta']
            vis_score = str(today_games['vls']['s'])
            quarter = 'Q' + str(today_games['p'])
            last_play_clock = today_games['lpla']['cl']

            score_x = 21
            if int(today_games['hls']['s']) >= 100 or int(today_games['hls']['s']) >= 100:
                score_x = 19
            clock_adj = 0
            try:
                last_play_clock = datetime.strptime(last_play_clock,"%M:%S.%f").strftime("%#S.%f")[:-5]
                clock_adj = 3
            except ValueError:
                last_play_clock = last_play_clock
            
            last_play_desc = re.sub(' : ',':',re.sub('(.*\] )','',re.sub(' +', ' ',today_games['lpla']['de'])))
            last_play_desc = re.sub('Substitution replaced by','Sub for',last_play_desc)
            last_play_desc = re.sub('Out-of-Bounds','OB',last_play_desc)
            last_play_desc = re.sub('3pt Shot','3PT',last_play_desc)
            last_play_desc = re.sub('PTS','P',last_play_desc)
            last_play_desc = re.sub('ThreePoints','3PT',last_play_desc)
            last_play_desc = re.sub('TwoPoints','2PT',last_play_desc)
            last_play_desc = re.sub('Turnover','TOV',last_play_desc)
            last_play_desc = re.sub('Free Throw','FT',last_play_desc)
            last_play_desc = re.sub(' of ','-',last_play_desc)
            last_play_desc = re.sub('Jump Shot:','2PT:',last_play_desc)
            last_play_desc = re.sub('Missed Block','Blocked',last_play_desc)
            last_play_desc = re.sub('Rebound','REB',last_play_desc)
            last_play_desc = re.sub('Timeout','TO',last_play_desc)
            last_play_desc = re.sub('Regular','Full',last_play_desc)
            last_play_desc = re.sub('Jumper: Blocked','Blocked',last_play_desc)
            last_play_desc = re.sub('Driving Layup Shot','Layup',last_play_desc)
            last_play_desc = re.sub('Off:','O:',last_play_desc)
            last_play_desc = re.sub('Def:','D:',last_play_desc)
            last_play_desc = re.sub('Foul: Shooting','Shooting Foul',last_play_desc)
            last_play_desc = re.sub('Foul: Offensive','Offensive Foul',last_play_desc)
            last_play_desc = re.sub('Missed','Miss',last_play_desc)
            if len(last_play_desc) >= 15:
                last_play_desc_1 = last_play_desc[:15] + '-'
                last_play_desc_2 = last_play_desc[15:]
            else:
                last_play_desc_1 = last_play_desc
                last_play_desc_2 = ''
            home_text_Color = graphics.Color(team_colors[today_games['hls']['ta']]["text"]["r"], team_colors[today_games['hls']['ta']]["text"]["g"], team_colors[today_games['hls']['ta']]["text"]["b"])
            vis_text_Color = graphics.Color(team_colors[today_games['vls']['ta']]["text"]["r"], team_colors[today_games['vls']['ta']]["text"]["g"], team_colors[today_games['vls']['ta']]["text"]["b"])
            home_fouls_check = int(today_games['hls']['ftout'])
            vis_fouls_check =  int(today_games['vls']['ftout'])
            home_banner_r = team_colors[today_games['hls']['ta']]["banner"]["r"]
            home_banner_g = team_colors[today_games['hls']['ta']]["banner"]["g"]
            home_banner_b = team_colors[today_games['hls']['ta']]["banner"]["b"]
            vis_banner_r = team_colors[today_games['vls']['ta']]["banner"]["r"]
            vis_banner_g = team_colors[today_games['vls']['ta']]["banner"]["g"]
            vis_banner_b = team_colors[today_games['vls']['ta']]["banner"]["b"]
            home_accent_r = team_colors[today_games['hls']['ta']]["accent"]["r"]
            home_accent_g = team_colors[today_games['hls']['ta']]["accent"]["g"]
            home_accent_b = team_colors[today_games['hls']['ta']]["accent"]["b"]
            vis_accent_r = team_colors[today_games['vls']['ta']]["accent"]["r"]
            vis_accent_g = team_colors[today_games['vls']['ta']]["accent"]["g"]
            vis_accent_b = team_colors[today_games['vls']['ta']]["accent"]["b"]
            canvas.Clear()
            for x in range(2,34):
                for y in range(0,8):
                    canvas.SetPixel(x, y, home_banner_r, home_banner_g, home_banner_b)
            for x in range(0,2):
                for y in range(0,8):
                    canvas.SetPixel(x, y, home_accent_r, home_accent_g, home_accent_b)
            for x in range(2,34):
                for y in range(9,17):
                    canvas.SetPixel(x, y, vis_banner_r, vis_banner_g, vis_banner_b)
            for x in range(0,2):
                for y in range(9,17):
                    canvas.SetPixel(x, y, vis_accent_r, vis_accent_g, vis_accent_b)
            if (home_fouls_check) >= 1:
                for x in range(35,36):
                    for y in range(2,2 + home_fouls_check):
                        canvas.SetPixel(x, y, 255, 255, 0)
            if (vis_fouls_check) >= 1:
                for x in range(35,36):
                    for y in range(11,11 + home_fouls_check):
                        canvas.SetPixel(x, y, 255, 255, 0)

            graphics.DrawText(canvas, font_2, 3, 7, home_text_Color, home_name)
            graphics.DrawText(canvas, font_2, 3, 16, vis_text_Color, vis_name)
            graphics.DrawText(canvas, font_2, score_x, 7, home_text_Color, home_score)
            graphics.DrawText(canvas, font_2, score_x, 16, vis_text_Color, vis_score)
            graphics.DrawText(canvas, font_1, 46, 12, textColor, quarter)
            graphics.DrawText(canvas, font_1, 40 + clock_adj, 6, textColor, last_play_clock)
            graphics.DrawText(canvas, font_1, 1, 23, textColor, last_play_desc_1)
            graphics.DrawText(canvas, font_1, 1, 31, textColor, last_play_desc_2)
            matrix.SwapOnVSync(canvas)
            print("Again")
            time.sleep(2)

    def _render_postgame(today_games):
        home_name = today_games['hls']['ta']
        pprint( today_games)
        #home_record = '(' + today_games['hls']['re'] + ')'
        home_score = today_games['hls']['s']
        vis_name = today_games['vls']['ta']
        #vis_record = '(' + today_games['vls']['re'] + ')'
        vis_score = today_games['vls']['s']
        home_text_Color = graphics.Color(team_colors[today_games['hls']['ta']]["text"]["r"], team_colors[today_games['hls']['ta']]["text"]["g"], team_colors[today_games['hls']['ta']]["text"]["b"])
        vis_text_Color = graphics.Color(team_colors[today_games['vls']['ta']]["text"]["r"], team_colors[today_games['vls']['ta']]["text"]["g"], team_colors[today_games['vls']['ta']]["text"]["b"])
        home_banner_r = team_colors[today_games['hls']['ta']]["banner"]["r"]
        home_banner_g = team_colors[today_games['hls']['ta']]["banner"]["g"]
        home_banner_b = team_colors[today_games['hls']['ta']]["banner"]["b"]
        vis_banner_r = team_colors[today_games['vls']['ta']]["banner"]["r"]
        vis_banner_g = team_colors[today_games['vls']['ta']]["banner"]["g"]
        vis_banner_b = team_colors[today_games['vls']['ta']]["banner"]["b"]
        home_accent_r = team_colors[today_games['hls']['ta']]["accent"]["r"]
        home_accent_g = team_colors[today_games['hls']['ta']]["accent"]["g"]
        home_accent_b = team_colors[today_games['hls']['ta']]["accent"]["b"]
        vis_accent_r = team_colors[today_games['vls']['ta']]["accent"]["r"]
        vis_accent_g = team_colors[today_games['vls']['ta']]["accent"]["g"]
        vis_accent_b = team_colors[today_games['vls']['ta']]["accent"]["b"]
        while True:
            for x in range(2,64):
                for y in range(0,8):
                    canvas.SetPixel(x, y, home_banner_r, home_banner_g, home_banner_b)
            for x in range(0,2):
                for y in range(0,8):
                    canvas.SetPixel(x, y, home_accent_r, home_accent_g, home_accent_b)
            for x in range(2,64):
                for y in range(9,17):
                    canvas.SetPixel(x, y, vis_banner_r, vis_banner_g, vis_banner_b)
            for x in range(0,2):
                for y in range(9,17):
                    canvas.SetPixel(x, y, vis_accent_r, vis_accent_g, vis_accent_b)
            graphics.DrawText(canvas, font_2, 3, 7, home_text_Color, home_name)
            graphics.DrawText(canvas, font_2, 3, 16, vis_text_Color, vis_name)
            #graphics.DrawText(canvas, font_1, 19, 7, home_text_Color, home_record)
            #graphics.DrawText(canvas, font_1, 19, 16, vis_text_Color, vis_record)
            graphics.DrawText(canvas, font_1, 55, 7, home_text_Color, home_score)
            graphics.DrawText(canvas, font_1, 55, 16, vis_text_Color, vis_score)
            graphics.DrawText(canvas, font_1, 1, 24, textColor, "Final")
            matrix.SwapOnVSync(canvas)

    def _render_no_games():
        home_name = 'Sorry, no games today :('
        graphics.DrawText(canvas, font_1, 2, 7, textColor, home_name)
        matrix.SwapOnVSync(canvas)
        time.sleep(10)

    def _get_game_detail(game_id):
        game_id = "".join(game_id)
        url = "https://data.wnba.com/data/10s/v2015/json/mobile_teams/wnba/2022/scores/gamedetail/" + game_id + "_gamedetail.json"
        response = urlopen(url)
        game_detail = json.loads(response.read())['g']
        return game_detail

    def iserror(live_game):
        try:
            return (live_game['lpla'] == {})
        except KeyError:
            return True

    ## Pull In Schedule For Given Day
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

    today_games = [x for x in all_games if (x['gdte'] == date_today)]
    preference_games = [x for x in all_games if (x['gdte'] == date_today) and (x['h']['ta'] == 'MIN')]

    if (len(preference_games) == 1):
        game_id = preference_games[0]['gid']
        live_game = _get_game_detail(game_id)

    if len(preference_games) == 1:
        if (live_game['hls']['s'] == '' and live_game['vls']['s'] == ''):
            _render_pregame(preference_games[0])
        else:
            if (preference_games[0]['stt'] != 'Final'):
                while True:
                    game_id = preference_games[0]['gid']
                    live_game = _get_game_detail(game_id)
                    canvas.Clear()
                    _render_game(live_game)
                    time.sleep(10)
            else:
                canvas.Clear()
                _render_postgame(preference_games[0])

    else:
        if (len(today_games) >= 1):
            today_game_ids = []
            live_game_ids = []
            not_live_game_ids = []
            for g in today_games:
                append_this = [str(g['gid'])]
                today_game_ids.append(append_this)
            for l in 0,len(today_game_ids)-1:
                live_game = _get_game_detail(today_game_ids[l])
                pprint(today_games[l]['stt'])
                if ((today_games[l]['stt'] == 'Final') or iserror(live_game)):
                    not_live_game_ids.append(today_game_ids[l])
                else:
                    live_game_ids.append(today_game_ids[l])

                if len(live_game_ids) >= 1:
                    #Loop trhough live games
                    for l_1 in live_game_ids:
                        print(l_1)
                        live_game = _get_game_detail(l_1)
                        _render_game(live_game)
                        time.sleep(10)
                else:
                    #Loop through final and pregame games
                    for l_2 in not_live_game_ids:
                        live_game = _get_game_detail(l_2)
                        
                        if (live_game['stt'] != 'Final'):
                            pregame_game = [x for x in all_games if (x['gid'] == "".join(l_2))]
                            _render_pregame(pregame_game[0])
                        
                        if (live_game['stt'] == 'Final'):
                            _render_postgame(live_game)
                        
                        time.sleep(10)
        
        else:
            _render_no_games()
    
    time.sleep(3)
