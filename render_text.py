from samplebase import SampleBase
from RGBMatrixEmulator import graphics
import time

def _run_matchup(text,x_coord,y_coord):
    class RunMatchup(SampleBase):
        def __init__(self, *args):
            super(RunMatchup, self).__init__(*args)
            self.parser.add_argument("-t", "--text", default=text)

        def run(self):
            offscreen_canvas = self.matrix.CreateFrameCanvas()
            font = graphics.Font()
            font.LoadFont("assets/fonts/patched/4x6.bdf")
            textColor = graphics.Color(255, 255, 255)
            my_text = self.args.text

            while True:
                graphics.DrawText(offscreen_canvas, font, x_coord, y_coord, textColor, my_text)
                time.sleep(0.01)
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
    return RunMatchup(SampleBase)

# Main function
def render_home_name(matchup_text,x_coord,y_coord):
    run_text = _run_matchup(matchup_text,x_coord,y_coord)
    if (not run_text.process()):
        run_text.print_help()

def render_vis_name(matchup_text,x_coord,y_coord):
    run_text = _run_matchup(matchup_text,x_coord,y_coord)
    if (not run_text.process()):
        run_text.print_help()

def render_matchup_status(matchup_text,x_coord,y_coord):
    run_text = _run_matchup(matchup_text,x_coord,y_coord)
    if (not run_text.process()):
        run_text.print_help()