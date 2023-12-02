import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

@dataclass(unsafe_hash=True)
class RGB:
    r: int
    g: int
    b: int

LMT = RGB(12,13,14)

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

def rgbify(s_rgb):
    r=g=b=0
    for n_x in s_rgb.split(", "):
        n, clr = n_x.split()
        if clr == "red":
            r = int(n)
        elif clr == "green":
            g = int(n)
        elif clr == "blue":
            b = int(n)
        else:
            raise Exception(f"unknown colour: {clr}")
    return RGB(r,g,b)

def processLines(lines):
    games = dict()
    for line in lines:
        #Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        s_game, s_rgbs = line.split(": ")
        gid = int(s_game.split()[1])
        rgbs=[]
        for s_rgb in s_rgbs.split("; "):
            rgb = rgbify(s_rgb)
            rgbs.append(rgb)
        games[gid] = rgbs
    return games

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

print(elapsedTimeMs(),"starting part1")

games = readFile()

def maxRgb(rgbs): # move to dataclass
    r=g=b=0
    for rgb in rgbs:
        if rgb.r>r:r=rgb.r
        if rgb.g>g:g=rgb.g
        if rgb.b>b:b=rgb.b
    return RGB(r,g,b)

def rgbPwr(rgb):
    return rgb.r * rgb.g * rgb.b

def isPossible(rgb, lmt): # move to dataclass
    if rgb.r > lmt.r or rgb.g > lmt.g or rgb.b > lmt.b:
        return False
    return True

poss_id_tot = 0
sum_pwr = 0
for gid in games:
    rgbs = games[gid]
    max_rgb = maxRgb(rgbs)
    if isPossible(max_rgb,LMT):
        poss_id_tot+=gid
    sum_pwr += rgbPwr(max_rgb)
print(f"part1: {poss_id_tot}")
print(f"part2: {sum_pwr}")

print(elapsedTimeMs(),"done!")
