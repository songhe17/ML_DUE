#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 03:13:05 2020

@author: songhewang
"""

def seq(start, end):
    arr = []
    while start <= end:
        arr.append(start)
        start += 1
    return arr

def output(n,l):
    res = []

    for start in range(1, 1000000001):
        if start >= n:
            break
        for end in range(start+1, 1000000001):
            s = sum(seq(start, end))
            if s > n:
                break
            elif s == n and end - start < 100 and end - start + 1 >= l:
                res.append((start, end))
        if s >= n:
            continue
    if res == []:
        print('No')
        return 0
        
    outs = max(res, key = lambda x:x[0] - x[-1])
    outs = seq(outs[0], outs[1])
    
    return outs


outs = output(100, 7)
if outs:
    string = ''
    for i in outs:
        string += ' '
        string += str(i)
    print(string[1:])
    
for i in range(15):
    print(i, 7**i)