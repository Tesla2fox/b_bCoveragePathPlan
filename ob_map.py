# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 09:40:11 2018

@author: robot
"""
import readCfg.read_cfg as rd
import numpy as np
import networkx as nx


class ObMap(object):
    def __init__(self,cfgFileName):
        readCfg = rd.Read_Cfg(cfgFileName)        
        data = []
        readCfg.get('row',data)
        self.row = int(data.pop())    
        readCfg.get('col',data)
        self.col = int(data.pop())            
        self.mat = np.zeros((self.row,self.col))
        
        obRowLst = []
        obColLst = []
        readCfg.get('obRow',obRowLst)
        readCfg.get('obCol',obColLst)
        
        for i in range(len(obRowLst)):
            obRow = int(obRowLst[i])
            obCol = int(obColLst[i])
            self.mat[obRow][obCol] = 1 
#        print(self.mat)
        self.constructGraph()        
    def constructGraph(self):
        self.Graph = nx.Graph()
        for i in range(self.row):
            for j in range(self.col):
                center = (i,j)
                self.Graph.add_node((i,j))
                if (self.mat[center] == 1):
                    continue
                neiLst = self.getNeighbor(center)
                for unit in neiLst:
                    self.Graph.add_edge(center,unit)
#        print(self.Graph.number_of_nodes())
#        print(self.Graph[center])        
    def getSpanningTree(self):
        edges = nx.traversal.dfs_edges(self.Graph,(0,0))
        print(list(edges))
#        tree = nx.minimum_spanning_tree(self.Graph)
#        data = tree.edges(data = True )
#        print(data)
        n_lst = self.getNeighbor(center = (1,2))
        print(n_lst)
    def getNeighbor(self,center = (0,0)):
        n_lst = []
        if self.mat[center] == 1:
            return n_lst        
        for i in range(center[0]-1,center[0]+2):
            for j in range(center[1]-1,center[1]+2):
                n_center = (i,j)
                if n_center == center:
                    continue
                if 0<=n_center[0]<self.row and 0<=n_center[1]<self.col:
                    if self.mat[i][j] != 1:
                        n_lst.append(n_center)
        return n_lst
                    

if __name__ == '__main__':
    ob_map = ObMap('.//data//1_20_20_50_Cfg.dat')
    ob_map.constructGraph()
    ob_map.getSpanningTree()
    for i in range(5,8):
        print(i)
        