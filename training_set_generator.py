#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 00:53:47 2020

@author: songhewang
"""

import numpy as np
import itertools
import random
from collections import Counter
from copy import deepcopy
def generate_graph(n,m,speed_limit=35, capacity=2):
    #n is the number of nodes 
    #m is the number of path
    cords = np.random.rand(n,2)
    nodes = np.transpose(cords)
    all_links = list(itertools.product(range(n),repeat = 2))
    for i,link in enumerate(all_links):
        if link[0] == link[1]:
            all_links.remove(link)

    links_nodes = np.array(random.sample(all_links, m))
    print(links_nodes)
    links = np.zeros((m,5))
    links[:,:2] = links_nodes
    links[:,2] = capacity
    for i, link in enumerate(links):
        node1, node2 = link[:2]
        node1 = cords[int(node1)]
        node2 = cords[int(node2)]
        length = np.sqrt(sum((node1 - node2) ** 2)) * 1000
        links[i][3] = length
        links[i][4] = length / (speed_limit * 1.609 / 3.6)
    
    def find_path(graph, od, points, arr):
        ori, des = od
        if points[-1] == des:
            path = []
            for i in range(len(points)-1):
                l = points[i:i+2]
                try:
                    path.append(graph.tolist().index(l))
                except ValueError:
                    print(points)
                    
            arr.append(path)
            
        for link in graph:
            if link[0] == ori and link[1] not in points:
                find_path(graph, [link[1],des], points+[link[1]], arr)
        return arr
    
    od_paths = {}
    all_path = []
    for od in all_links:
        paths = find_path(links_nodes, od, [od[0]], []) 
        if paths != []:
            od_paths[od] = paths
            for i in paths:
                for j in i:
                    all_path.append(j)
        else:
            continue
    
    print(od_paths)
    print(len(od_paths))
    all_path = Counter(all_path)
    all_path_ratio = deepcopy(all_path)
    for link in all_path:
        c = links[link][2]
        all_path_ratio[link] = c / all_path_ratio[link]
    #print(all_path_ratio)
    
    max_od_demand = {}
    for key, item in od_paths.items():
        value = sum(list(map(lambda x: sum(map(lambda y: all_path_ratio[y], x)), item)))
        max_od_demand[key] = value
    print(Counter(max_od_demand))
    
    
    return max_od_demand, od_paths, links, nodes
        
        
    
generate_graph(5,10)
