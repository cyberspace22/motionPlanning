#This is the skeleton code for our project. Currently I am working on adding the RRT potion of the code. I have commented
#where the different blocks of code will go. the pygame imports can be removed as we will be using Tkinter()
import sys, random, math, pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2
from lineIntersect import *

numNodes = 10
radMov = 10

class Node:
    x = 0
    y = 0
    cost=0
    parent=None
    def __init__(self,xcoord, ycoord):
         self.x = xcoord
         self.y = ycoord

def dist(xy1,xy2):
    return sqrt((xy1[0]-xy2[0])*(xy1[0]-xy2[0])+(xy1[1]-xy2[1])*(xy1[1]-xy2[1]))

def nodeInDir(xy1,xy2):
    if(dist(xy1,xy2) < radMov):
        return xy2
    else:
        theta = atan2(xy2[1]-xy1[1],xy2[0]-xy1[0])
        return xy1[0] + EPSILON*cos(theta), xy1[1] + EPSILON*sin(theta)


def main():
    nodes = []
    #insert start node
    nodes.append(Node(0.0,0.0))
    startnode = nodes[0]
    goalnode = Node(500.0,500.0)
    for i in range(numNodes):
        #voronoi section
        #ends with giving a point (x,y)
        xpt = 0
        ypt = 0
        vnode = Node(xpt,ypt)
        cnode = nodes[0] #start from the start node
        #find closest node to the selected voronoi node
        for n in nodes:
            if (dist([n.x,n.y],[vnode.x,vnode.y]) < dist([cnode.x,cnode.y],[vnode.x,vnode.y])):
                cnode = n
        #interpolation towards the voronoi node from the closest node
        #the function should return the closest 'node' in the direction
        tnode = nodeInDir([vnode.x,vnode.y],[cnode.x,cnode.y])
        nodeint = Node(tnode[0],tnode[1])


if __name__ == '__main__':
    main()
    '''running = True
    while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
                 running = False'''
