import Tkinter
import tkMessageBox
from Sanghatest11 import *
from astar_sid import astar_v2
from random import randint
from math import ceil
from test import ghostPlan
import pygame

pygame.init()

drawVels = True
QUIT = False
paused = False
step = False

initial_position=[0,0,3]
goal_position=[11,11]
print('\n\n')
gridsize=30
grid=backEndGrid(gridsize)
print(grid)

<<<<<<< HEAD
A4x4=[[800,200,900,100],[1800,1400,1200,600],[500,600,1000,2000],[500,1200,1000,200], [2000,2000,2500,2500]]

A4x4=[[300,400,100,0],[400,0,600,300],[800,200,900,100],[1800,1400,1200,600],[500,600,1000,1000],[500,1200,1000,1600],]

=======
A4x4 = []
#A4x4=[[100,200,300,300],[500,500,800,800],[800,200,900,100],[1800,1400,1200,600],[500,600,1000,1000],[500,1200,1000,1600],]
for i in range(100,2800,400):
    for j in range(100,2800,400):
        A4x4.append([i,j,i+200,j+200])
>>>>>>> 230b12af9250f78611d26f2c97ed6d5c6c73d6d3
rect=[]
list_line=[]
obstacle_coord=[]
snake_coord = []
snake_size=2
song = pygame.mixer.Sound('pacman_eatfruit.wav')
ghosteatssnake = pygame.mixer.Sound('smb_bowserfalls.wav')
#details for ghost
gstart = [10,20]
ggoal = []
obsgh = []
ghcoord = [10,20]
#e is length of a square in the grid
e=40

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
#print("obstacle list = %s" %obstacle_list)
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
grid_coord=[]
def createGridVisible(l,objs,objs_h):
    in2=0
    for in2 in range(0,l):
        grid_coord.append(C.create_line(objs[in2].a,objs[in2].b,objs[in2].c,objs[in2].d,fill="red"))
        grid_coord.append(C.create_line(objs_h[in2].a,objs_h[in2].b,objs_h[in2].c,objs_h[in2].d,fill="red"))

    pass

def drawGrid():
    for grid in grid_coord:
        C.itemconfig(grid,fill="red")

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
                #id = C.create_rectangle(coordinate2,fill="#000fff000" )
                obstacle_coord.append(C.create_rectangle(coordinate2,fill="#000fff000" ))
            m=m+1
        n=n+1
    #d = C.create_rectangle(coordinate2,fill="#000fff000" )
#    pass
# so we need functions that can move along 2 perpendicular axes.
#only question remained is why al obstacles are not shown from the obstacle list

def drawObstacles():
    for coordinate2 in obstacle_coord:
        C.itemconfig(coordinate2)


for any21 in obstacle_list:
    obj_obs11=any21
    #print('\n\n')
    rect=Obstacle_from_pixel_to_grid(obj_obs11,rect)
    #this rect is all obstacles of square size ready to fit in grid
    #rect=np.array(rect)
    #print(rect)
    #print('\n\n')
    grid=update_grid_with_obs(grid,rect)
    global obsgh
    #print("obsgh = %s" %obsgh)
    obsgh = rect
    #now the grid is up to date, it is allready an array
    #print "Final grid"
#    print(grid)
# we have final grid enviornment with all posible obstacles
#here we have data from backend and graphics
#this is the place where backend affects front ended
#important note:- m up and down n right and left= mxn grid
#=======================================================================================================================
# keyboard events
#=======================================================================================================================
def on_key_press(event):
    global paused, step, QUIT, drawVels

    if event.keysym == "space":
        paused = not paused
    if event.keysym == "s":
        step = True
        paused = False
    if event.keysym == "v":
        drawVels = not drawVels
    if event.keysym == "Escape":
        QUIT = True


apple=[]


top = Tkinter.Tk()

# keyboard interaction
top.bind("<space>",on_key_press)
top.bind("s",on_key_press)
top.bind("<Escape>",on_key_press)
top.bind("v",on_key_press)

appleimage = Tkinter.PhotoImage(file = 'apple.png')
ghostimage = Tkinter.PhotoImage(file = 'ghost2.png')

#yet to complete
def generateApple():
    x,y=-1,-1
    while (x==-1 and y==-1) or grid[x][y]!=0 :
        x= randint(0,gridsize-1)
        y= randint(0,gridsize-1)

    apple.append([x,y])
    C.create_image(x*e+e/2, y*e+e/2, image=appleimage)
    return x,y

def regenerateApple():
    [x,y]=apple[-1]
    C.create_image(x*e+e/2, y*e+e/2, image=appleimage)

def drawGhost(gcoord):
    C.create_image(gcoord[0]*e+e/2,gcoord[1]*e+e/2, image = ghostimage)

counter=0
coordinate=initial_position[0],initial_position[1],e,e


C = Tkinter.Canvas(top, bg="gray", height=1200, width =1200)
arc=C.create_arc(coordinate,start=30,extent=300,fill="red")
angle=45
close =1
shut = 360
flag1=True
createVisibleObstacles(grid)
#createGridVisible(l,objs,objs_h)
snake_coord.append(coordinate)
#grid[coordinate[0]/e,coordinate[1]/e]=1

staticgrid=grid


def snake(coord,angle,close,flag12,l1,objs1,objs_h1,grid1,counter,snake_s,orientation):
#    print orientation
    global static
    #staticgrid = grid1
    global shut
    C.delete(Tkinter.ALL)

    global step, paused, QUIT
    if QUIT: #Simulation Loop
        print("Final size of snake : %s ... quitting"%snake_s)
        top.destroy()



    #drawGrid()
    if orientation == 3: #R
        a=1
        b=0
        c=1
        d=0
        shut = 360
    elif orientation == 2: #D
        a=0
        b=1
        c=0
        d=1
        shut = 270
    elif orientation == 1 : #L
        a=-1
        b=0
        c=-1
        d=0
        shut = 180
    elif orientation == 0 : #U
        a=0
        b=-1
        c=0
        d=-1
        shut = 90

    if not paused:
        coord=coord[0]+1*a,coord[1]+1*b,coord[2]+1*c,coord[3]+1*d
        snake_coord.append(coord)

    if angle >0 and close ==1:
        angle=angle-5
        if angle ==0:
            close =0
    elif angle<45 and close==0:
        angle =angle+5
        if angle ==45:
            close=1

    #if not paused

    tail = 1
    while tail<=snake_s and len(snake_coord)>=tail*int(e):
        if tail ==1:
           arc = C.create_arc(snake_coord[-1],outline="black",start=shut + angle,extent= (359-2*angle),fill="red")
           #arc = C.create_oval(snake_coord[-1][0],snake_coord[-1][1]+2,snake_coord[-1][0]+20,snake_coord[-1][1]+, width = 0, fill ="black")
        else:
            if len(snake_coord)>(tail-1)*e - int(e/2):
                arc = C.create_oval(snake_coord[-(tail-1)*e + int(e/2)],outline="black",width=0,fill="red")
            if len(snake_coord)>(tail-1)*e:
                arc = C.create_oval(snake_coord[-(tail-1)*e],outline="black",width=0,fill="red")

        tail = tail+1

    #ggoal = [snake_coord[e*(snake_s-1)][0]/e,snake_coord[e*(snake_s-1)][1]/e]
    if len(snake_coord) > e*(snake_s-1):
        ggoal = [snake_coord[-e*(snake_s-1)][0]/e,snake_coord[-e*(snake_s-1)][1]/e]
    else:
        ggoal = [snake_coord[-1][0]/e,snake_coord[-1][1]/e]
    #ggoal = [15,20]
    #writing call for ghost function and setting the goal point as snake head
    #print("obsgh = %s" %obsgh)
    #print("ggoal = %s" %ggoal)
    global ghcoord
    gstart = ghcoord
    if not paused:
        ghcoord,rgoal = ghostPlan(gstart,ggoal,obsgh)
    #ghcoord = [int(round(ghcoord[0])),int(round(ghcoord[1]))]
        if rgoal and snake_s!=2:
            snake_s=snake_s-1
            ghosteatssnake.play()

    createGridVisible(l1,objs1,objs_h1)

    createVisibleObstacles(grid1)
    drawGhost(ghcoord)
    regenerateApple()

    if coord[0]/e==goal_position[1] and coord[1]/e==goal_position[0]:
        print "Reached apple"
        snake_s = snake_s+1
        song.play()

        pathtotake=-1

        while pathtotake==-1:
            goal_position[1],goal_position[0]=generateApple()
            pathtotake = astar_v2(initial_position,grid.tolist(),goal_position,ghcoord)
            #quit()
        #print goal_position

    if (coord[0]%e==0 and coord[1]%e==0):
            #grid1[int(snake_coord[-12][1]/e),int(snake_coord[-12][0]/e)]=0

            if len(snake_coord)>e*(snake_s):

                grid1[int(snake_coord[-e*(snake_s)-1][1]/e),int(snake_coord[-e*(snake_s)-1][0]/e)]=0

            grid1[ceil(snake_coord[-1][1]/e),ceil(snake_coord[-1][0]/e)]=2
            #print grid1

            pathtotake = astar_v2([coord[1]/e,coord[0]/e,orientation],grid1.tolist(),goal_position,ghcoord)

            top.after(10,lambda: snake(coord,angle,close,flag12,l1,objs1,objs_h1,grid1,counter,snake_s,pathtotake[1][2]))
    else:
        top.after(10,lambda: snake(coord,angle,close,flag12,l1,objs1,objs_h1,grid1,counter,snake_s,orientation))


C.pack()
#snake(coordinate,angle,close,flag1,l,objs,objs_h,grid)
# the main loop of the program

#print grid.tolist()

pathtotake=-1

while pathtotake==-1:
    goal_position[1],goal_position[0]=generateApple()
    pathtotake = astar_v2(initial_position,grid.tolist(),goal_position,ghcoord)
print goal_position
top.after(10,lambda: snake(coordinate,angle,close,flag1,l,objs,objs_h,grid,counter,snake_size,pathtotake[1][2]))
'''
while(flag1):
    #snake(coordinate,angle,close,flag1,l,objs,objs_h,grid)
    pass
'''
top.mainloop()
