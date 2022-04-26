import pygame as pg
import sys
import re
import json
import configparser
# fontlist = pg.font.get_fonts()
# fontlist.sort()
# print(fontlist)

# load config file
config = configparser.ConfigParser()
config.read("settings.ini")
def_conf = config["default"]

# load text
f = open(def_conf["textpath"])
sub_text = f.read()
f.close()
sub_text = re.sub("\n", " ", sub_text)

FPS = 60
SIZE = (def_conf.getint("width"), def_conf.getint("height"))

pg.init()
sc = pg.display.set_mode(SIZE)
pg.display.set_caption("LiveSubtitles by DimaDivan")
clock = pg.time.Clock()

ls_font = pg.font.SysFont(def_conf["font"], def_conf.getint("fontsize"))
ls_text = ls_font.render(sub_text, True, (200, 200, 200))

x = 0
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
        x -= def_conf.getint("speed")
    if x <= -ls_text.get_width():
        x = 0
    # --------

    pg.display.update()