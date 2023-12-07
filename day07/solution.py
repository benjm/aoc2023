import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

@dataclass(unsafe_hash=True)
class Hand:
    typ: int
    cards: str
    value: int
    bid: int

VALUES = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", ")[::-1]

def getType(cards): # YUK :)
    grp = dict()
    for c in cards:
        grp[c]=grp.get(c,0)+1
    jokers = grp.get("J",0)
    #TODO: map out best possible change with jokers

    l = len(grp)
    if l == 1:
        return 6 # 5 of a kind
    if l == 2:
        if 4 in grp.values():
            return 5 + (jokers > 0) # four of a kind [5 with jokers]
        return 4 + ((jokers > 0) * 2) # full house [5 with jokers]
    if l == 3:
        if 3 in grp.values():
            return 3 + ((jokers > 0) * 2) # three of a kind [4 with a joker or 3 jokers]
        return 2 + ((jokers == 1) * 2) + ((jokers == 2) * 3) # two pairs [full house or 4 with jokers]
    if l == 4:
        return 1  + ((jokers > 0) * 2) # one pair [3 with jokers]
    return 0 + (jokers > 0) # high card [pair with jokers]

def processLines(lines):
    hands = []
    for line in lines:
        cards, bid_s = line.split()
        bid = int(bid_s)
        typ = getType(cards)
        value = int(str(typ)+''.join(hex(VALUES.index(c))[2:] for c in cards),16)
        hand = Hand(typ, cards, value, bid)
        hands.append(hand)
    return hands

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = [VALUES]
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

print(elapsedTimeMs(),"starting part1")
hands = readFile()
hands.sort(key=lambda h: h.value)
winnings = 0 
for r in range(len(hands)):
    hand = hands[r]
    winnings += (r+1) * hand.bid
print(winnings)

print(elapsedTimeMs(),"starting part2")
