#This is the skeleton code for our project. Currently I am working on adding the RRT potion of the code. I have commented
#where the different blocks of code will go. the pygame imports can be removed as we will be using Tkinter()
import sys, random, math, pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2
from lineIntersect import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
from shapely.geometry import Polygon

numNodes = 10
radMov = 10

def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.
    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()*2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)

def vrni_region(points):
    vor = Voronoi(points)
    # plot
    regions, vertices = voronoi_finite_polygons_2d(vor)

    min_x = vor.min_bound[0] - 0.1
    max_x = vor.max_bound[0] + 0.1
    min_y = vor.min_bound[1] - 0.1
    max_y = vor.max_bound[1] + 0.1

    mins = np.tile((min_x, min_y), (vertices.shape[0], 1))
    bounded_vertices = np.max((vertices, mins), axis=0)
    maxs = np.tile((max_x, max_y), (vertices.shape[0], 1))
    bounded_vertices = np.min((bounded_vertices, maxs), axis=0)

    box = Polygon([[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]])
    #print(regions)
    polygons = []
    for region in regions:
        poly_for_region = vertices[region]
        poly = Polygon(poly_for_region)
        poly = poly.intersection(box)
        poly_for_region = [p for p in poly.exterior.coords]
        print(poly_for_region)
        polygons.append(poly_for_region)
    #the variable polygons contains the coordinates for all voronoi regions
    #I am working on isolating the regions and relating them to their respective
    #polygons

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
        return xy1[0] + radMov*cos(theta), xy1[1] + radMov*sin(theta)


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
        nodes.append(nodeint)

if __name__ == '__main__':
    main()
    '''running = True
    while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
                 running = False'''
