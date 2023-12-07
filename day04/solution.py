import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

def processLines(lines):
    card_values=[]
    card_wins=dict()
    cards=dict()
    card_ids=[]
    for line in lines:
        card_s, values_s = line.split(": ")
        card_id = int(card_s.split()[1])
        win_s, have_s = values_s.split("| ")
        winners = set(map(int, win_s.split()))
        hand = set(map(int, have_s.split()))
        tot_winners = sum(1 for h in hand if h in winners)
        card_value = 0
        if tot_winners > 0:
            card_value = 2**(tot_winners-1)
        card_values.append(card_value)
        wins=set()
        if tot_winners>0:
            wins.update(range(card_id+1, card_id+tot_winners+1))
        card_wins[card_id]=wins
        cards[card_id]=1
        card_ids.append(card_id)
    return card_values, card_wins, cards, card_ids

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

card_values, card_wins, cards, card_ids = readFile()
print(sum(card_values))


for card_id in card_ids:
    n_card_id = cards[card_id]
    #print(f"have {n_card_id} od card {card_id}", file=sys.stderr)
    for win in card_wins[card_id]:
        cards[win]+=n_card_id
        #print(f"\twon {n_card_id} of card id {win}", file=sys.stderr)
    #print(f"\t\tnow holding {cards}")

#print(cards)

print(f"total cards: {sum(cards[card_id] for card_id in cards)}")
