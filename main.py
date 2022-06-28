import pygame as pg
import sys
import json
import os

# load config file
with open("settings.json") as f:
    config = json.load(f)

# print fonts
if config["printfonts"]:
    fontlist = pg.font.get_fonts()
    fontlist.sort()
    with open("fonts.txt", 'w') as f:
        for i in fontlist:
            f.write(i + '\n')

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
    sub_text = f.read()
    sub_text = sub_text.replace("\n", " ")

FPS = 60
SIZE = (config["width"], config["height"])

pg.init()
sc = pg.display.set_mode(SIZE)
pg.display.set_caption("LiveSubtitles by DimaDivan")
clock = pg.time.Clock()

ls_font = pg.font.SysFont("arial", config["fontsize"])
ls_text = ls_font.render(sub_text, True, (200, 200, 200))

x = SIZE[0] - 1
y = (SIZE[1] - ls_text.get_height())//2

while True:
    clock.tick(FPS)

    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

    # --------
    sc.fill((0, 0, 0))
    sc.blit(ls_text, (x, y))
    if x > -ls_text.get_width():
        x -= config["speed"]
    if x <= -ls_text.get_width():
        x = SIZE[0] - 1
    # --------

    pg.display.update()