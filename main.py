import pygame as pg
import argparse as argp
import sys
import json
import os


parser = argp.ArgumentParser()
parser.add_argument(
    "--logfonts",
    action='store_true',
    help="write all accesible fonts to text file")
parser.add_argument(
    "--nocycle",
    action='store_true',
    help="close program after showing all lines")
args = parser.parse_args()


if args.logfonts:
    fontlist = pg.font.get_fonts()
    fontlist.sort()
    with open("fonts.log", 'w') as f:
        for i in fontlist:
            f.write(i + '\n')


with open("settings.json") as f:
    config = json.load(f)

# get filenames
file_list = []
for name in os.listdir(config["folderpath"]):
    if name.endswith(".txt"):
        file_list.append(name)
file_list.sort()

# check files amount
if len(file_list) == 0:
    print("No files found.")
    sys.exit()
else:
    print("Found", len(file_list), "files:")
    for i in file_list:
        print("    " + i)

# load first file
with open(os.path.join(config["folderpath"], file_list[0])) as f:
    sub_lines = f.read().split("\n\n")
for i in range(len(sub_lines)):
    sub_lines[i] = sub_lines[i].replace('\n', '')

FPS = 60
SIZE = (config["width"], config["height"])
BG_COLOR = (240, 240, 240)
FG_COLOR = (100, 100, 255)

pg.init()
sc = pg.display.set_mode(SIZE)
pg.display.set_caption("LiveSubtitles by DimaDivan")
clock = pg.time.Clock()

# ls_font = pg.font.SysFont("arial", config["fontsize"])
ls_font = pg.font.Font(config['customfonts'][0], config['fontsize'])


ind = 0
ls_text = ls_font.render(sub_lines[ind], True, FG_COLOR)
x = SIZE[0]
y = (SIZE[1] - ls_text.get_height())//2

while True:
    clock.tick(FPS)

    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

    # --------

    # draw
    sc.fill(BG_COLOR)
    sc.blit(ls_text, (x, y))

    # shift text
    if x > -ls_text.get_width():
        x -= config["speed"]
    
    # change text
    if x <= -ls_text.get_width():
        x = SIZE[0]
        if args.nocycle:
            ind += 1
            if ind == len(sub_lines):
                sys.exit()
        else:
            ind = (ind + 1) % len(sub_lines)
            ls_text = ls_font.render(sub_lines[ind], True, FG_COLOR)
        
    # --------

    pg.display.update()