'''
@author Rudrani Angira and Soumya Achar

'''
import pdb
import csv
import re
from collections import deque
import re
import sys

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}    
        
    def __iter__(self):
        return iter(self.adjacent.values())
   
    
    def __repr__(self):
        return str(self.id)

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        if neighbor in self.adjacent.keys():
            #print 'self.adjacent[neighbor %s =' % self.adjacent[neighbor]
            return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
          
        else:
            #print n
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()


class X:
    
    
    def dfs_1(self,graph, start,end):
        visited, stack = set(), [start]
        visited.add(start)
        cost=0
        pred={}
        pred[start]=None
        
        while stack:
            
            vertex = stack.pop()
            
           
            for x in vertex.get_connections():
                
                
                if x not in visited:
                    pred[x]=vertex
                    visited.add(g.get_vertex(str(x)))
                    stack.append(g.get_vertex(str(x)))
    

        myDFSpath =[]
        while end!=None:
            myDFSpath.append(end)
            if pred[end]==None:
                break
            
            cost=cost+end.get_weight(pred[end])
            end=pred[end]
        print 'DFS cost = %d' % cost  
        if cost==0:
            print "Path does not exist"
        else:
            print 'DFS path : ',
            while myDFSpath:
                print "%s "%myDFSpath.pop(),   
            print"\n"    
        return visited
    
    
    
    
    
    def bfs_1(self,graph, start,end):
        pred={}
        
        #print 'start %s=' % start
        pred[start]=None
        visited, queue = set(), deque([start])
        visited.add(start)
        cost=0
        #visited.add(start)
        while queue:
            #print 'stack = %s' % queue
            vertex = queue.popleft()           
            for x in vertex.get_connections():
                #print 'x =%s' % x
                if x not in visited:
                    pred[x]=vertex
                    visited.add(g.get_vertex(str(x)))
                    queue.append(g.get_vertex(str(x)))  
        
        myBFSpath = []
        while end!=None:
            myBFSpath.append(end)
            if pred[end]==None:
                break
            
            cost=cost+end.get_weight(pred[end])
            end=pred[end]
           
        print '\nBFS cost = %d' % cost
        if cost == 0:
            print"Path does not exist"
        else:
            print"BFS path: ",
            while myBFSpath:
                print"%s "%myBFSpath.pop(),
            print"\n\n"
        return visited
    
    
    
    
    def dfs_2(self,start,end,maxDepth,pred):
        
        if  str(end)==str(start) or maxDepth<=0  :            
            return start
        
        #print 'maxDepth  %d' % maxDepth
        for x in start.get_connections():
                #print 'start x %s %s' % (start,x)
                if x!=None and start!=None:
                    
                    if x not in pred.keys():
                        pred[x]=start
                    
                    found=self.dfs_2(x,end, maxDepth-1,pred)
                    if str(found)==str(end):
                        return found
        return None   
        
    
    
    
    def iterativeDeepening(self,start,end):
        
        cost=0
        pred={}
        pred[start]=None
        for maxDepth in range(1,20):
        #while 1:   
            pred={}
            pred[start]=None

            #print 'About to enter %d' % maxDepth
            found=self.dfs_2(start,end, maxDepth,pred)
            if found==end:
                break
                
        myIDdfsPath = []  
        #print "%s"% pred    
        while end!=start and end!=None:
            
            if pred[end] == None:
                break
            
            myIDdfsPath.append(end)
            cost=cost+end.get_weight(pred[end])
            end=pred[end]
            
            if end==start:
                break
        myIDdfsPath.append(start)
        print"ID-DFS cost : %d"%cost
        if cost == 0:
            print "Path Does not exist"
        else: 
            print "ID-DFS path: ",
            while myIDdfsPath:
                print"%s "%myIDdfsPath.pop(),
        return pred
            


if __name__ == '__main__':
    
    g = Graph()
    lst=[]
    myFilepath = raw_input("\n Enter the path of .csv input File\n")
    with open(myFilepath,'rb') as f:
        csv_f = csv.reader(f)

        for row in csv_f:
    
        
            if g.get_vertex(row[0]) is None:
                g.add_vertex(row[0])
            if g.get_vertex(row[1]) is None:
                g.add_vertex(row[1]) 
            
            if g.get_vertex(row[0]) and g.get_vertex(row[1]):
                g.add_edge(row[0], row[1], int(row[2]))
        
        
    while 1:
        x = X()
        beg=raw_input("Enter SPACE separated nodes and algorith(BFS/DFS/ID). ")
        data = beg.split(' ')
        present = g.get_vertex(data[0])
        if(present is None):
            print "Invalid Source"
            continue
            
        if data[2]=='DFS':
            x.dfs_1(g,g.get_vertex(data[0]),g.get_vertex(data[1]))
        elif data[2]=='BFS':
            x.bfs_1(g,g.get_vertex(data[0]),g.get_vertex(data[1]))
        elif data[2]=='ID':
            x.iterativeDeepening(g.get_vertex(data[0]),g.get_vertex(data[1]))
        
        terminate=raw_input("\n Enter 1 to exit and anything else to continue")
        if(terminate == '1'):
            sys.exit()
         
