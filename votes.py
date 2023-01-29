#!/usr/bin/env python3

from sys import stdin
import itertools

def scores(lineups, variants):
    __votes = {i: [0 for i in variants] for i in variants}
    for (order, number) in lineups.items():
        positions = order.split()
        n = 0
        for pos in positions:
            if pos not in variants: continue
            __votes[pos][n] += number
            n+=1
    return __votes

def winners(scores):
    winner = max(scores.values())
    return list(filter(lambda x: scores.get(x) == winner, scores))

def positional(votes, vals):
    scores = {i: 0 for i in votes}
    for (k, v) in votes.items():
        scores[k] = sum(x*y for (x, y) in zip(v, vals))
    return scores

def plurality(votes):
    __len = len(votes.get(next(iter(votes))))
    vals = [1]
    for i in range(__len - 1): vals.append(0)
    return positional(votes, vals)

def antiplurality(votes):
    __len = len(votes.get(next(iter(votes))))
    vals = [1 for i in range(__len - 1)]
    vals.append(0)
    return positional(votes, vals)

def plurality_runoff(lineups, variants):
    s = scores(lineups, variants)
    n_votes = sum(s.get(next(iter(s))))
    __scores = plurality(s)
    top = winners(__scores)
    if len(top) == 1:
        if __scores[top[0]] / n_votes > 0.5: return top[0]
        top2 = max(__scores, key=lambda x: 0 if x == top[0] else __scores.get(x))
        __variants = [top[0], top2]
    else:
        __variants = [top[0], top[1]]
    return winners(plurality(scores(lineups, __variants)))[0]

def borda(votes):
    __len = len(votes.get(next(iter(votes))))
    vals = [i for i in range(__len)[::-1]]
    return positional(votes, vals)

def stv(lineups, variants):
    __variants = variants.copy()
    for _ in lineups.keys():
        vals = plurality(scores(lineups, __variants))
        top = max(vals, key=vals.get)
        if vals[top] / sum(vals.values()) >= 0.5:
            return top
        __variants.remove(min(vals, key=vals.get))

def coombs(lineups, variants):
    __variants = variants.copy()
    for _ in lineups.keys():
        vals = plurality(scores(lineups, __variants))
        top = max(vals, key=vals.get)
        if vals[top] / sum(vals.values()) >= 0.5:
            return top
        bottom = antiplurality(scores(lineups, __variants))
        __variants.remove(min(bottom, key=bottom.get))

def baldwin(lineups, variants):
    __variants = variants.copy()
    ranking = []
    for _ in range(len(lineups.keys()) - 1):
        borda_scores = borda(scores(lineups, __variants))
        ranking.append(min(borda_scores, key=borda_scores.get))
        __variants.remove(ranking[-1])
    ranking.append(__variants[0])
    return ranking[::-1]


def condorcet(lineups, variants):
    duels = {i: {x: 0 for x in variants} for i in variants}
    for base in variants:
        for (key, val) in lineups.items():
            pos = key.find(base)
            for compare in variants:
                pos1 = key.find(compare)
                if pos < pos1: duels[base][compare] += val
    return duels

def condorcet_winner(duels, n_votes):
    for (key, val) in duels.items():
        if all([k == key or v / n_votes > 0.5 for (k, v) in val.items()]):
            return key

def copeland(duels):
    variants = duels.keys()
    wins = {i: 0 for i in variants}
    for i in variants:
        for j in variants:
            if duels[i][j] > duels[j][i]: wins[i] += 1
    return wins

def kemmeny(duels):
    variants = list(duels.keys())
    scores = {}
    for perm in itertools.permutations(variants):
        perm_str = " ".join(perm)
        scores[perm_str] = 0
        for (n, var) in enumerate(variants):
            for v in variants[n+1:]:
                if perm.index(var) < perm.index(v):
                    scores[perm_str] += duels[var][v]
    return scores

def maximin(duels):
    variants = duels.keys()
    scores = {}
    for (key, val) in duels.items():
        scores[key] = min([v for (k, v) in val.items() if k != key])
    return max(scores, key=scores.get)


if __name__ == '__main__':
    variants = input().split()
    lineups = {}

    for line in stdin:
        split = line.split(": ")
        if lineups.get(split[1]) == None:
            lineups[split[1]] = int(split[0])
        else:
            lineups[split[1]] += int(split[0])

    votes = scores(lineups, variants)

    print("antiplurality rule winners:", winners(antiplurality(votes)))
    print("plurality rule winners:", winners(plurality(votes)))
    print("plurality runoff winner :", plurality_runoff(lineups, variants))
    print("borda rule winners:", winners(borda(votes)))
    print("single transferable vote winner:", stv(lineups, variants))
    print("condorcet winner:",
        condorcet_winner(
            condorcet(lineups, variants),
            sum(lineups.values())))
    print("copeland winners:", winners(copeland(condorcet(lineups, variants))))
    print("kemmeny winner permutations:", winners(kemmeny(condorcet(lineups, variants))))
    print("maximin winner:", maximin(condorcet(lineups, variants)))
    print("coombs winner:", coombs(lineups, variants))
    print("baldwin ranking:", baldwin(lineups, variants))
