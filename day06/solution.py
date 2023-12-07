import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

@dataclass(unsafe_hash=True)
class Race:
    t: int
    d: int

def processLines(lines):
    times = list(map(int, lines[0].split(":")[1].split()))
    distances = list(map(int, lines[1].split(":")[1].split()))
    races=[]
    for i in range(len(times)):
        races.append(Race(times[i], distances[i]))

    k_time = int(lines[0].split(":")[1].replace(" ",""))
    k_dist = int(lines[1].split(":")[1].replace(" ",""))
    return races, Race(k_time, k_dist)

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

races, actual = readFile()

print(elapsedTimeMs(),"starting part1")
wins_per=[]
for race in races:
    wins=0
    for l in range(race.t):
        if l * (race.t - l) > race.d:
            wins+=1
    wins_per.append(wins)
print(wins_per)
print(math.prod(wins_per))

print(elapsedTimeMs(),"starting part2")
print("Actual race:", actual)
wins=0
for l in range(actual.t):
    if l * (actual.t - l) > actual.d:
        wins+=1
print(elapsedTimeMs(),wins)
# Actual race: Race(t=46828479, d=347152214061471)
# 0:00:06.237858 28360140
# Yuk brute force but it did it under 7s so :)
