import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

SPELT = "zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty".split(", ")
REV = SPELT[::-1]
def lastdigit(line):
    l = len(line)
    for i in range(len(line)):
        j = l-1-i
        #print(line,i,line[j],line[:j+1],file=sys.stderr)
        if line[j].isdigit():
            return line[j]
        for num in REV:
            le = line[:j+1]
            if le.endswith(num):
                return str(SPELT.index(num))[-1]
            # else:
            #     print(le,"does not end with",num,file=sys.stderr)
    return "last-error" # error

def firstdigit(line):
    for i in range(len(line)):
        if line[i].isdigit():
            return line[i]
        for num in REV:
            if line[i:].startswith(num):
                return str(SPELT.index(num))[0]
    return "first-error" # error

def processLines(lines):
    tot = 0
    for line in lines:
        fd = firstdigit(line)
        ld = lastdigit(line)
        #print(line,fd,ld,file=sys.stderr)
        fl = int(fd) * 10 + int(ld)
        tot+=fl
    return tot

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

data = readFile()

# @dataclass(unsafe_hash=True)
# class Point:
#     x: int
#     y: int

print(elapsedTimeMs(),"starting part1")
print(data)

# print(elapsedTimeMs(),"starting part2")
