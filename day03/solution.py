import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since


def processLines(lines):
    #process, convert, etc etc
    h=len(lines)
    w=len(lines[0])
    pparts=dict()
    symbols=dict()
    for y in range(h):
        line = lines[y]
        part = 0
        px=-1
        prev = ""
        for x in range(w):
            # . or digit or symbol
            c = line[x]
            if c.isdigit():
                if not part:
                    part=1
                    px=x
                prev+=c
            else:
                if part:
                    pparts[Point(px,y)]=prev
                    part=0
                    prev=""
                    px=-1
                if c != ".":
                    symbols[Point(x,y)]=c
        if part:
            pparts[Point(px,y)]=prev
            part=0
            prev=""
            px=-1
    return h, w, pparts, symbols

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)


HEIGHT, WIDTH, pparts, symbols = readFile()
# dict{Point:value} for possible part numbers (values can repeat)
# dict{Point:symbol} for symbols


def allPoints(pp, s):
    l = len(s)
    allp=set()
    for x in range(pp.x, pp.x+l):
        allp.add(Point(x,pp.y))
    return allp

def findNeighbours(pp, s, h, w):
    l = len(s)
    neighbours = set()
    for x in range(pp.x-1,pp.x+l+1):
        for y in range(pp.y-1,pp.y+2):
            neighbours.add(Point(x,y))
    return neighbours

def filterParts(pparts, symbols, h, w):
    parts = dict()
    for pp in pparts:
        neighbours = findNeighbours(pp, pparts[pp], h, w)
        if any((n in symbols) for n in neighbours):
            parts[pp] = pparts[pp]
    return parts

parts = filterParts(pparts, symbols, HEIGHT, WIDTH)

sum_of_parts = sum(int(parts[p])for p in parts)

print(sum_of_parts)
# test passed but...
# 563584 was too high --> out by 1 error in x range
# 557705


print(elapsedTimeMs(),"starting part2")

pgears = set()
for sp in symbols:
    if symbols[sp] == "*":
        pgears.add(sp)
sum_ratios = 0
for pgp in pgears:
    neighbours = findNeighbours(pgp, "*", HEIGHT, WIDTH)
    nparts=set()
    for pp in parts:
        allp = allPoints(pp,parts[pp])
        if any((p in neighbours) for p in allp):
            nparts.add(pp)
    if len(nparts) == 2:
        ratio = math.prod(int(parts[p]) for p in nparts)
        sum_ratios += ratio

print(sum_ratios)
# find gears A*B
# find possible gears *
# for each find numbers in neighbours
# 
