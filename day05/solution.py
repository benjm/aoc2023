import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

@dataclass(unsafe_hash=True)
class Range:
    start: int
    delta: int

@dataclass(unsafe_hash=True)
class MapperRange:
    a0: int
    b0: int
    delta: int
    def contains(self, a):
        d = a - self.a0
        return d >= 0 and d < self.delta
    def map(self, a, typ_a="?", typ_b="?"):
        d = a - self.a0
        if self.contains(a):
            #print(f"\t\tmapping {typ_a} {a} to {typ_b} {self.b0 + d}")
            return self.b0 + d
        else:
            raise Exception(f"mapper {self} called with unknown value {a}")
    def map_range(self, unmr): #new_unmrs, new_range
        print(f"\t\t {self}")
        print(f"\t\t {unmr}")
        new_unmrs=[]
        new_range=None
        if unmr.start > self.a0+self.delta or unmr.start+unmr.delta < self.a0:
            new_unmrs.append(unmr)
        else:
            # overlap:
            start = max(unmr.start, self.a0)
            end = min(unmr.start+unmr.delta, self.a0+self.delta)
            new_range = Range(self.map(start), end-start)
            # possible unmr: before any overlap
            new_unmrs = []
            if unmr.start < self.a0:
                new_unmrs.append(Range(unmr.start, self.a0-unmr.start))
            # possible unmr: after any overlap
            if unmr.start+unmr.delta > self.a0+self.delta:
                start = self.a0+self.delta
                end = unmr.start+unmr.delta
                new_unmrs.append(Range(start, (end-start)))
        print(f"\t\t still unmapped: {new_unmrs}")
        print(f"\t\t mapped: {new_range}")
        return new_unmrs, new_range

@dataclass(unsafe_hash=True)
class Mapper:
    typ_a: str
    typ_b: str
    maps: set
    def map(self, a):
        for map_r in self.maps:
            if map_r.contains(a):
                return map_r.map(a, self.typ_a, self.typ_b)
        return a
    
def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

def processLines(lines):
    seed_ids = list(map(int, lines[0].split(": ")[1].split()))
    mappers = dict()
    typ_a = typ_b = None
    maps = set()
    for line in lines[1:]:
        if len(line)<1:
            if typ_a:
                #print(f"mapping out {typ_a}:{typ_b}")
                mapper = Mapper(typ_a, typ_b, maps)
                mappers[typ_a] = mapper
            typ_a = typ_b = None
            maps=set()
        elif ":" in line:
            typ_a, typ_b = line.split()[0].split("-to-")
        else:
            b0,a0,delta=map(int,line.split())
            mapper_range = MapperRange(a0, b0, delta)
            maps.add(mapper_range)
    #print(f"mapping out {typ_a}:{typ_b}")
    mapper = Mapper(typ_a, typ_b, maps)
    mappers[typ_a] = mapper
    return seed_ids, mappers

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

seed_ids, mappers = readFile()

ids=seed_ids

from_typ = "seed"
#print(from_typ, ids)
to_typ = None
while to_typ != "location":
    new_ids = list()
    mapper = mappers[from_typ]
    to_typ = mapper.typ_b
    #print(f"\tusing mapper {mapper}")
    for i in ids:
        j = mapper.map(i)
        new_ids.append(j)
    from_typ = to_typ
    #print(from_typ, new_ids)
    ids = new_ids

print(min(ids))

print(elapsedTimeMs(),"starting part two")


ids=seed_ids
print(ids)
ranges = []
for si in range(0,len(ids),2):
    s0 = ids[si]
    s1 = ids[si+1]
    ranges.append(Range(s0,s1))
print(ranges)

# start+range as not mapped
# for each map range, break into mapped (<=one) and not mapped (<=two)
# once all mapped or no more map ranges move to next
# [optional: recombine any neighouring ranges]

def reRange(in_range, mapper):
    unmapped = [in_range]
    ranges = []
    for mapper_range in mapper.maps:
        if len(unmapped) < 1:
            print("\t all mapped!")
            return ranges # return early
        new_unmapped = []
        for unmr in unmapped:
            new_unmrs, new_range = mapper_range.map_range(unmr)
            if new_range != None:
                ranges.append(new_range)
            new_unmapped+=new_unmrs
        unmapped = new_unmapped
    ranges+=unmapped
    return ranges

from_typ = "seed"
#print(from_typ, ids)
to_typ = None
while to_typ != "location":
    new_ranges = []
    mapper = mappers[from_typ]
    print(mapper)
    to_typ = mapper.typ_b
    for r in ranges:
        new_ranges += reRange(r, mapper)
    from_typ = to_typ
    ranges = new_ranges
    print(ranges)

ranges.sort(key=lambda r:r.start)
print(ranges[0].start)

# Yikes that was some ugly code :')
