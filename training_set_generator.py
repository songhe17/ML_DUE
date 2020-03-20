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

def link_generator(n,m,speed_limit=35, capacity=2):
    #n is the number of nodes 
    #m is the number of path
    random.seed(11)
    cords = np.random.rand(n,2)
    nodes = np.transpose(cords)
    all_links = [(a,b) for a,b in list(itertools.product(range(1,n+1),repeat = 2)) if a != b]

    links_nodes = np.array(random.sample(all_links, m))
    links = np.zeros((m,5))
    links[:,:2] = links_nodes
    links[:,2] = capacity
    for i, link in enumerate(links):
        node1, node2 = link[:2]
        node1 = cords[int(node1)-1]
        node2 = cords[int(node2)-1]
        length = np.sqrt(sum((node1 - node2) ** 2)) * 10000
        links[i][3] = length
        links[i][4] = length / (speed_limit * 1.609 / 3.6)
    #print(links)
        
    return links_nodes, links, nodes
        
def od_genertor(links_nodes, links, nodes):
    all_links = [(a,b) for a,b in list(itertools.product(range(1,len(nodes[0])+1),repeat = 2)) if a != b]
    def find_path(graph, od, points, arr):
        ori, des = od
        if points[-1] == des:
            path = []
            for i in range(len(points)-1):
                l = points[i:i+2]
                try:
                    path.append(graph.tolist().index(l)+1)
                except ValueError:
                    print(points)
                    
            arr.append(path)
            
        for link in graph:
            if link[0] == ori and link[1] not in points:
                find_path(graph, [link[1],des], points+[link[1]], arr)
        return arr
    
    od_paths = {}
    all_path = []
    path_list = []
    for od in all_links:
        paths = find_path(links_nodes, od, [od[0]], []) 
        if paths != []:
            od_paths[od] = paths
            for i in paths:
                path_list.append(i)
                for j in i:
                    all_path.append(j)
        else:
            continue

    all_path = Counter(all_path)

    all_path_ratio = deepcopy(all_path)
    for link in all_path:
        c = links[link-1][2]

        all_path_ratio[link] = c / all_path_ratio[link]
    #print(all_path_ratio)

    od_demand = {}
    for key, item in od_paths.items():
        value = sum(list(map(lambda x: sum(map(lambda y: all_path_ratio[y], x)), item)))
        od_demand[key] = np.random.rand() * value * 500
    
    
    return od_demand, od_paths, path_list
        
        
    
links_nodes, links, nodes = link_generator(5,10)

dict_od_demand, od_paths, path_list = od_genertor(links_nodes, links, nodes)

#start to formulate the output

od_set = np.zeros((len(dict_od_demand),3))
od_path_set = []
od_demand = []
t_a = []
for i, (od, path) in enumerate(od_paths.items()):
    od_set[i][2] = len(path)
    od_set[i][1] = od[1]
    od_set[i][0] = od[0]
    od_path_set.append([[]])
    for p in path:
        od_path_set[i][0].append(path_list.index(p)+1)
    od_demand.append(dict_od_demand[od])
    ta = np.random.randint(2,4) + np.random.rand()
    t_a.append(ta)

max_path_len = len(max(path_list, key=lambda x: len(x)))

for i in range(len(path_list)):
    path_list[i] += (max_path_len - len(path_list[i])) * [0]
print('path list')
print(path_list)
print('links')
print(links)
print('od demand')
print(od_demand)
print('target arrival time')
print(t_a)
print('od set')
print(od_set)
print('od path set')
print(od_path_set)    

dump = True
if dump:    
    import scipy.io as io
    io.savemat('data/test_paths.mat', dict(pathList=path_list))
    io.savemat('data/test_dat.mat', dict(linkData=links, networkName=['test'], nodeCoordinates=nodes))
    io.savemat('data/Network_planning_parameters.mat', dict(OD_demand=od_demand, T_A=t_a))
    io.savemat('data/OD_info.mat', dict(OD_set=od_set, ODpath_set=od_path_set))
#k = io.loadmat('/Users/songhewang/Downloads/Braess_dat.mat')

#print(k)




















