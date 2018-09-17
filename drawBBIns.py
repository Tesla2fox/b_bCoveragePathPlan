# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 15:41:37 2018

@author: robot
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 21:43:14 2018

@author: robot
"""

import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import random
import numpy as np
import copy as cp
import copy
import readCfg.read_cfg as rd
from IPython.display import HTML,display 
import colorlover as cl
import math
#import read_cfg 


class Pnt:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    def pnt2dict(self):
        dic = dict(x = x,y= y)
        return dic
    def display(self):
        print('x = ',self.x,'y = ',self.y)

class Circle:
    def __init__(self,pnt = Pnt(),rad = 0):
        self.x = pnt.x
        self.y = pnt.y
        self.rad = rad
        self.x0 = self.x  - self.rad
        self.y0 = self.y  - self.rad
        self.x1 = self.x  + self.rad
        self.y1 = self.y  + self.rad
    def circle2dict(self):
        dic = dict()
        dic['type'] = 'circle'
        dic['xref'] = 'x'
        dic['yref'] = 'y'
        dic['x0'] = self.x0
        dic['y0'] = self.y0
        dic['x1'] = self.x1
        dic['y1'] = self.y1        
        dic['line'] = dict(color = 'rgba(50, 171, 96, 1)')
        return dic
class Line:
    def __init__(self,pnt0 =Pnt(),pnt1=Pnt()):
        self.x0 = pnt0.x
        self.y0 = pnt0.y
        self.x1 = pnt1.x
        self.y1 = pnt1.y
    def line2dict(self):
        dic= dict()
        dic['type']='line'
        dic['x0'] =self.x0
        dic['y0'] =self.y0
        dic['x1'] =self.x1
        dic['y1'] =self.y1
        dic['line'] = dict(color = 'rgb(128, 0, 128)')
        return dic
class Rect:
    def __init__(self,pnt =Pnt(),width =0,height =0):
        self.x0 = pnt.x
        self.y0 = pnt.y
        self.x1 = self.x0 + width
        self.y1 = self.y0 + height
    def rect2dict(self):
        dic = dict()
        dic['type']='rect'
        dic['x0'] = self.x0
        dic['y0'] = self.y0
        dic['x1'] = self.x1
        dic['y1'] = self.y1
        dic['line'] = dict(color = 'rgb(128, 0, 128)')
        return dic

def getLevelColor(level):
    strcolor = 'rgba('
    for i in range(3):
        strcolor = strcolor + str(level*50)+','
    strcolor = strcolor + str(1/level) +')'
    return strcolor    

colorLst = ['white','black']

class Env:
    def __init__(self, mat = np.zeros((2,2))):
        self.mat = mat
        self.shapeLst = []
        self.drawData = []
        self.annotations = []
        self.proLevNum = 0
    def addgrid(self):        
        g_color = 'blue'
        row = len(self.mat)        
        for i in range(row):
            for j in range(len(self.mat[i])):
                pnt = Pnt(i,j)
                rect = Rect(pnt,1,1)
                rectDic = rect.rect2dict()
                rectDic['line']['color'] = g_color
                rectDic['line']['width'] = 0.5
#                rectDic['opacity'] =  1/(int(self.mat[i][j])+1)                
#                rectDic['fillcolor'] = colorLst[int(self.mat[i][j])]
                if(int(self.mat[i][j])==1):
                    rectDic['fillcolor'] = 'black'                
#                if(int(self.mat[i][j])==0):
#                    rectDic['fillcolor'] = colorLst[int(self.mat[i][j])]
#                getLevelColor(mat[i][j])
                self.shapeLst.append(copy.deepcopy(rectDic))
        print(len(self.shapeLst))

    def addEdges(self,edges = []):
        mark_x = []
        mark_y = []     
        for p in range (len(edges[0])):
            pnt0 = Pnt(edges[0][p] + 0.5,edges[1][p]+ 0.5)
            pnt1 = Pnt(edges[2][p] + 0.5,edges[3][p]+ 0.5)
            mark_x.append(pnt0.x)
            mark_x.append(pnt1.x)
            mark_y.append(pnt0.y)
            mark_y.append(pnt1.y)
            line = Line(pnt0,pnt1)
            lineDic = line.line2dict()
#                print(randColor())
            lineDic['line']['color'] = 'rgba(15,15,15,0.5)'
            lineDic['line']['width'] = 3
            self.shapeLst.append(copy.deepcopy(lineDic))
        markTrace = go.Scatter(mode ='markers',
                                   x= mark_x,
                                   y= mark_y,
                                   marker =dict(size =3),
                                   name = 'Spanning-Tree')
        self.drawData.append(markTrace)    
    def addProGrid(self,proLevLst = []):
        line_color = 'red'
        ind = 0 
        row = len(self.mat)        
        bupu = cl.scales['9']['seq']['YlGnBu']        
        bupuNum = cl.interp(bupu,500)
        bupuUnit  = math.floor(500/4)
        for i in range(row):
            for j in range(len(self.mat[i])):
                pnt = Pnt(i,j)
                rect = Rect(pnt,1,1)
                rectDic = rect.rect2dict()
                rectDic['line']['color'] = line_color
                rectDic['line']['width'] = 0.5
                if int(proLevLst[ind]) == 0:
                    rectDic['fillcolor'] = 'black'
                else:
                    rectDic['fillcolor'] = bupuNum[int((proLevLst[ind] - 1) *bupuUnit)]
                    rectDic['opacity'] =  0.7
                ind  += 1
                self.shapeLst.append(copy.deepcopy(rectDic))
    def addRobotStartPnt(self,lst= []):
        for i in range(len(lst[0])):
            lst[0][i] = lst[0][i] + 0.5
            lst[1][i] = lst[1][i] + 0.5
            startTrace = go.Scatter(x =[lst[0][i]], y = [lst[1][i]],mode ='markers',marker = dict(symbol = 'cross-dot',size = 20),
                                    name = 
#                                    'start')
                                    'Robot_'+ str(i+1))
            self.drawData.append(startTrace)
                
    def drawPic(self,name ='env',fileType = True):
        layout = dict()
        layout['shapes'] = self.shapeLst
        layout['xaxis'] = {'range':[0,len(self.mat[0])]}
        layout['yaxis'] = {'range':[0,len(self.mat)]}
        layout['xaxis'] = dict(
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=True,
        ticks='',
        showticklabels = False)
        layout['yaxis'] = dict(
        scaleanchor = "x",
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=True,
        ticks='',
        showticklabels = False)
        layout['font'] = dict(
            family='sans-serif',
            size=25,
            color='#000'
        )
        layout['legend'] =   dict(font=dict(
            family='sans-serif',
            size=25,
            color='#000'
        ))
        layout['autosize'] = False
        layout['height'] = 1000
        layout['width']= 1000
        layout['annotations'] = self.annotations
#        print(layout)
        fig = dict(data = self.drawData ,layout = layout)
        if(fileType):
            plotly.offline.plot(fig,filename = name + '.html',validate=False)
        else:
            py.image.save_as(fig,filename = name+'.jpeg')
    
        
def drawIns(cfgFileName = '5_20_20_80_Outdoor_Cfg.txt',drawType = 1,
            fileName = 'nothing',
            fileType = False ):
    py.sign_in('tesla_fox', 'HOTRQ3nIOdYUUszDIfgN')
    readCfg = rd.Read_Cfg(cfgFileName)
    
    data = []
    readCfg.get('row',data)
    row = int(data.pop())

    readCfg.get('col',data)
    col = int(data.pop())
        
    mat = np.zeros((row,col))
    
    obRowLst = []
    obColLst = []
    readCfg.get('obRow',obRowLst)
    readCfg.get('obCol',obColLst)
    
    for i in range(len(obRowLst)):
        obRow = int(obRowLst[i])
        obCol = int(obColLst[i])
        mat[obRow][obCol] = 1 


    robRowLst = []
    robColLst = []
    readCfg.get('robRow',robRowLst)
    readCfg.get('robCol',robColLst)
    
    proLevLst = []
    readCfg.get('proLevGrid',proLevLst)
    env = Env(mat)

    env.proLevNum = int(readCfg.getSingleVal('proLevNum'))
#    proMat  = np.zeros((row,col),dtype = int)
    
        
    #case 1 draw Environment
    if(drawType == 1):
        env.addgrid()
#        env.addProGrid(proLevLst = proLevLst)
        robLst = []
        robLst.append(robRowLst)
        robLst.append(robColLst)
        env.addRobotStartPnt(robLst)
        cfgFileName  = cfgFileName.split('data//')[1]
        cfgFileName  = cfgFileName.split('.dat')[0]
        env.drawPic('./png/env_'+cfgFileName,fileType)    
    #case 2 draw Environment with edges
def drawEdge(cfgFileName = '5_20_20_80_Outdoor_Cfg.txt',
             edges = []):
    py.sign_in('tesla_fox', 'HOTRQ3nIOdYUUszDIfgN')
    readCfg = rd.Read_Cfg(cfgFileName)    
    data = []
    readCfg.get('row',data)
    row = int(data.pop())
    readCfg.get('col',data)
    col = int(data.pop())        
    mat = np.zeros((row,col))    
    obRowLst = []
    obColLst = []
    readCfg.get('obRow',obRowLst)
    readCfg.get('obCol',obColLst)
    
    for i in range(len(obRowLst)):
        obRow = int(obRowLst[i])
        obCol = int(obColLst[i])
        mat[obRow][obCol] = 1 

    robRowLst = []
    robColLst = []
    readCfg.get('robRow',robRowLst)
    readCfg.get('robCol',robColLst)    
    env = Env(mat)
    env.addgrid()
    robLst = []
    robLst.append(robRowLst)
    robLst.append(robColLst)
    env.addRobotStartPnt(robLst)
    env.addEdges(edges)
    cfgFileName  = cfgFileName.split('data//')[1]
    cfgFileName  = cfgFileName.split('.dat')[0]
    env.drawPic('./png/env_'+cfgFileName)    

    
        
if __name__ == '__main__':
    drawIns( cfgFileName = './/data//1_20_20_50_Cfg.dat',fileType = True)
    pass
