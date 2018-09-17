# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 10:48:36 2018

@author: robot
"""

from ob_map import ObMap
import readCfg.read_cfg as rd
import networkx as nx
import drawBBIns 
from drawBBIns import *

#import ob_map


class B_BCoveragePathPlan(ObMap):
    def __init__(self,cfgFileName):
        super(B_BCoveragePathPlan,self).__init__(cfgFileName)
        self.cfgFileName = cfgFileName 
        readCfg = rd.Read_Cfg(cfgFileName)                        
        self.robRow = int(readCfg.getSingleVal('robRow'))
        self.robCol = int(readCfg.getSingleVal('robCol'))
        self.robPos = (self.robRow,self.robCol)
        
#        self.row = 0
    def getDFSTree(self):
        edges = nx.traversal.dfs_edges(self.Graph,self.robPos)
        edges = list(edges)
#        print(edges)
#        print(list(edges))
        return edges
    
    def getSegments(self):
        edges = self.getDFSTree()
        '''
        drawPicWithEdges        
        '''
        edgeLst =  [[] for i in range(4)]
        for edge in edges:
            edgeLst[0].append(edge[0][0])
            edgeLst[1].append(edge[0][1])
            edgeLst[2].append(edge[1][0])
            edgeLst[3].append(edge[1][1])
#        drawEdge(self.cfgFileName,edgeLst)
        
#        print(edges)
    
        self.sgTree = nx.DiGraph()
        self.sgTree.add_node(self.robPos)
        self.sgTree.add_edges_from(edges)
        print(self.sgTree.number_of_nodes())
        print(self.sgTree.out_degree((2,19)))
#        self.sgSet = set()
#        self.sgSet.add(self.robPos)
#        for i in range(len(edges) - 1):
#            if edges[i][1] != edges[i+1][0]:                
#                print(edges[i+1][0])
#                self.sgTree.add_node(edges[i + 1][0])
#                self.sgSet.add(edges[i + 1][0])
#                self.sgSet.add(edges[i][1])
#        lst = []
#        lastNode = self.robPos
#        print('robPos = ',self.robPos)
#        print(self.sgSet)
#        for edge in edges:
#            if edge[1] in self.sgSet:
#                if lastNode != edge[1]:                    
#                    self.sgTree.add_edge(lastNode,edge[1],sg = lst)                    
#                    lst = []
#                    lastNode = edge[1]
#            else:
#                lst.append(edge[1])
        
        print(self.sgTree[self.robPos])
        print(self.sgTree[(2,19)])
#        lst = [[] for i in range(4)]
#        print(self.)
#        for n,n
#        for i in range()
    def sg2Path(self):
        print('')
    
        
if __name__ == '__main__':
    bb_cpp = B_BCoveragePathPlan('.//data//1_20_20_50_Cfg.dat')
    print(bb_cpp.getSegments())
#    bb_cpp.getDFSTree()
#    print(bb_cpp.row)
    
    