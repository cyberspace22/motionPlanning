import Tkinter
import tkMessageBox
from Sanghatest11 import *
from test import *

initial_position=[0,0]
goal_position=[10,10]
print('\n\n')
gridsize=20
grid=backEndGrid(gridsize)
print(grid)
A4x4=[[100,100,200,200],[400,500,200,100],[500,100,700,400],[900,300,1000,200],[1900,1500,1300,700],[600,700,1100,1100],[600,1300,1100,1700]]
#A4x4=[[3,4,1,0],[4,0,6,3],[8,2,9,1],[18,14,12,6],[5,6,10,10],[5,12,10,16]]

rect=[]
list_line=[]
#e is scalling constant for everything
e=25
obstacle_list=[]
class obs_cord():
    #diagonally opposite 2 points are sufficicent, nothing else needed
    x1=0
    y1=0
    x2=0
    y2=0
    pass
class Horizontal_lines:
    a=10
    b=10
    c=400
    d=10
class Vertical_lines:
    a=10
    b=10
    c=10
    d=400
grid_lines=len(grid)+1
#so these are diagonally opposite points corodinates for the obsstacles rectangle
obj_obs11=obs_cord()
obj_obs11.x1=300
obj_obs11.y1=400
obj_obs11.x2=100
obj_obs11.y2=00

def obstcle_object_creation(a,b,c,d,obstacle_list1):
    obj_obs1new=obs_cord()
    obj_obs1new.x1=a
    obj_obs1new.y1=b
    obj_obs1new.x2=c
    obj_obs1new.y2=d
    obstacle_list1.append(obj_obs1new)

    return obstacle_list1

def obs_gen(Array4x4,obstacle_list12):
    for ele in Array4x4:
        a1=ele[0]
        b1=ele[1]
        c1=ele[2]
        d1=ele[3]
        obstacle_list12=obstcle_object_creation(a1,b1,c1,d1,obstacle_list12)
    obstacle_list12=np.array(obstacle_list12)
    return obstacle_list12

obstacle_list=obs_gen(A4x4,obstacle_list)

objs = [Horizontal_lines() for i in range(grid_lines)]

l=len(objs)
for xs in range (0,l):
    objs[xs].a=0
    objs[xs].b=0+e*xs
    objs[xs].c=e*gridsize
    objs[xs].d=0+e*xs
objs_h = [Vertical_lines() for i in range(grid_lines)]
l1=len(objs_h)
for xs1 in range (0,l1):
    objs_h[xs1].a=0+e*xs1
    objs_h[xs1].b=0
    objs_h[xs1].c=0+e*xs1
    objs_h[xs1].d=e*gridsize
    #obs(coord)
#here i will try showing a grid which will guide my testing and initial coding
def createGridVisible(l,objs,objs_h):
    in2=0
    for in2 in range(0,l):
        id = C.create_line(objs[in2].a,objs[in2].b,objs[in2].c,objs[in2].d,fill="red")
        id2 = C.create_line(objs_h[in2].a,objs_h[in2].b,objs_h[in2].c,objs_h[in2].d,fill="red")
    pass

def createVisibleObstacles(grid):
    lina=len(grid)
    m=0
    n=0
    for any31 in range(0,lina):#say xcord=n
        m=0
        for any32 in range(0,lina):#y coord=m
            if(grid[n][m]==1):
                #print('conditions satisfied')
                #n1,m1,n2,m2 is what corodinates are to send for obs
                coordinate2=m*e,n*e,(m+1)*e,(n+1)*e
                id = C.create_rectangle(coordinate2,fill="#000fff000" )
            m=m+1
        n=n+1
    #d = C.create_rectangle(coordinate2,fill="#000fff000" )
    pass
# so we need functions that can move along 2 perpendicular axes.
#only question remained is why al obstacles are not shown from the obstacle list

for any21 in obstacle_list:
    obj_obs11=any21
    print('\n\n')
    rect=Obstacle_from_pixel_to_grid(obj_obs11,rect)
    #this rect is all obstacles of square size ready to fit in grid
    #rect=np.array(rect)
    print(rect)
    print('\n\n')
    grid=update_grid_with_obs(grid,rect)
    #now the grid is up to date, it is allready an array
    #print "Final grid"
    print(grid)
# we have final grid enviornment with all posible obstacles
#here we have data from backend and graphics
#this is the place where backend affects front ended
#important note:- m up and down n right and left= mxn grid
def motion_snake():
    pass

top = Tkinter.Tk()
counter=0
coordinate=initial_position[0],initial_position[1],e,e
C = Tkinter.Canvas(top, bg="gray", height=1200, width =1200)
arc=C.create_arc(coordinate,start=30,extent=300,fill="red")
angle=45
close =1
flag1=True

def snake(coord,angle,close,flag12,l1,objs1,objs_h1,grid1,counter,orientation):

    if orientation == 'R':
        a=1
        b=0
        c=1
        d=0
        shut = 360
    elif orientation == 'D':
        a=0
        b=1
        c=0
        d=1
        shut = 270
    elif orientation == 'L' :
        a=-1
        b=0
        c=-1
        d=0
        shut = 180
    elif orientation == 'U' :
        a=0
        b=-1
        c=0
        d=-1
        shut = 90

    arc = C.create_arc(coord,outline="gray",start=shut + angle,extent=(360-2*angle),fill="gray")

    coord=coord[0]+1*a,coord[1]+1*b,coord[2]+1*c,coord[3]+1*d
    if angle >0 and close ==1:
        angle=angle-1
        if angle ==0:
            close =0
    elif angle<45 and close==0:
        angle =angle+1
        if angle ==45:
            close=1
    arc = C.create_arc(coord,start=shut + angle,extent= (360-2*angle),fill="red")
    top.after(30,lambda: snake(coord,angle,close,flag12,l1,objs1,objs_h1,grid1,counter,orientation))
    createGridVisible(l1,objs1,objs_h1)
    createVisibleObstacles(grid1)

C.pack()
#snake(coordinate,angle,close,flag1,l,objs,objs_h,grid)
# the main loop of the program
top.after(30,lambda: snake(coordinate,angle,close,flag1,l,objs,objs_h,grid,counter,'D'))
'''
while(flag1):
    #snake(coordinate,angle,close,flag1,l,objs,objs_h,grid)
    pass
'''
top.mainloop()
