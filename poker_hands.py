#!/usr/bin/env python3

import random

suits = ["H","D","S","C"]
ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
deck  = [(S,R) for S in suits for R in ranks]

hands = [
    "Straight Flush",
    "Four of a Kind",
    "Full House (high)",
    "Full House (low)",
    "Flush",
    "Straight",
    "Trip >= 10",
    "Trip < 10",
    "Two Pair >= 10",
    "Two Pair < 10",
    "Pair >= 10",
    "Pair < 10",
    "Ace High",
    "All Others"
    ]

def groupings(cards):
    g = {r : 0 for r in ranks}
    s = {S : 0 for S in suits}
    for (S, R) in cards:
        g[R] += 1
        s[S] += 1
    return g, s

def isFlush(s):
    for k, v in s.items():
        if v == 5:
            return True
    return False

def isStraight(g):
    prev = False
    count = 0
    straight = False
    for k, v in g.items():
        if v == 1:
            prev = True
        else:
            prev = False
            count = 0
        if prev:
            count += 1
            if count == 5:
                straight = True
    return straight

def getFours(g):
    result = [k for k,v in g.items() if v == 4]
    return result

def getTrips(g):
    result = [k for k,v in g.items() if v == 3]
    return result

def getPairs(g):
    result = [k for k,v in g.items() if v == 2]
    return result

def fullHigh(trips, pairs):
    trip = trips[-1] if trips else -1
    pair = pairs[-1] if pairs else -1
    if trips and pairs:
        return trip > pair
    return False

def fullLow(trips, pairs):
    trip = trips[-1] if trips else -1
    pair = pairs[-1] if pairs else -1
    if trips and pairs:
        return pair > trip
    return False

def hasAce(g):
    return g[-1]

def getHand(cards):
    g, s = groupings(cards)
    flush = isFlush(s)
    straight = isStraight(g)
    fours = getFours(g)
    trips = getTrips(g)
    pairs = getPairs(g)
    fh = fullHigh(trips, pairs)
    fl = fullLow(trips, pairs)
    if flush and straight:
        return 0
    elif fours:
        return 1
    elif fh:
        return 2
    elif fl:
        return 3
    elif flush:
        return 4
    elif straight:
        return 5
    elif trips and trips[-1] >= 10:
        return 6
    elif trips:
        return 7
    elif (len(pairs) > 1) and (pairs[-1] >= 10):
        return 8
    elif len(pairs) > 1:
        return 9
    elif pairs and (pairs[-1] >= 10):
        return 10
    elif pairs:
        return 11
    elif g[14]:
        return 12
    return 13

counts_pre = {}
counts_post = {}

winners = {}
for i in range(10, 13):
    counts_pre[i] = 0
    for j in range(13):
        counts_post[j] = 0
        winners[(i,j)] = 0

num = 100000

for i in range(num):
    random.shuffle(deck)
    pre = getHand(sorted(deck[0:2]))
    post = getHand(sorted(deck[0:5]))
    if post < 13:
        counts_post[post] += 1
    if (pre < 13):
        counts_pre[pre] += 1
        winners[(pre, post)] += 1

for k, v in winners.items():
    pre, post = k
    prob_pre = 100 * (counts_pre[pre] / num)
    prob_post = 100 * (counts_post[post] / num)
    p_giv_pre = 100 * (v / counts_pre[pre])
    if v != 0.:
        print(f"{hands[pre]:20} {hands[post]:20} | {prob_pre:9.5f} {prob_post:9.5f} {p_giv_pre:9.5f}")

