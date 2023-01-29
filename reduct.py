#!/usr/bin/env python

from sys import stdin

matrix = {i: {} for i in input().split()}
num = len(input().split()) - 1

def diff(line, lines, omit):
    for (x, ln) in lines.items():
        if all(line[i] == ln[i] for i in omit):
            return x
    return -1

i = 0
for line in stdin:
    ln = line.split()
    matrix[ln[-1][0]][i] = ln[:-1]
    i+=1

def upper_lower(omit):
    dic = {
        'lower': {'D': [], 'E': []},
        'upper': {'D': [], 'E': []}
    }
    for i in matrix.keys():
        for (num, j) in matrix[i].items():
            for k in matrix.keys():
                if i == k: continue
                ret = diff(j, matrix[k], omit)
                if ret != -1:
                    dic['upper'][i].append(ret)
                    break
            else: dic['lower'][i].append(num)
            dic['upper'][i].append(num)
    return dic

base = upper_lower(range(5))
print(base)

for i in range(2**5 - 1):
    li = []
    for j in range(5):
        if 2**j & i: li.append(j)
    ul = upper_lower(li)
    if (ul == base): print([1 + i for i in li])
