import Tkinter
import tkMessageBox
from obstacle import *
from astar import astar_v2
from random import randint
from math import ceil
from powerlaw import ghostPlan
import pygame


import time
start_time = time.time()

pygame.init()

QUIT = False
paused = False
step = False

initial_position=[0,0,3]
goal_position=[11,11]
#print('\n\n')
gridsize=40
grid=backEndGrid(gridsize)
#print(grid)

A4x4 = []

for i in range(300,3800,800):
    for j in range(300,3800,800):
        A4x4.append([i,j,i+200,j+200])
for i in range(700,3800,800):
    for j in range(700,3800,800):
        A4x4.append([i,j,i+200,j+200])

rect=[]
list_line=[]
obstacle_coord=[]
snake_coord = []

#initial size of snake
snake_size=2

#sound effects
song = pygame.mixer.Sound('snakeeatsapple.wav')
ghosteatssnake = pygame.mixer.Sound('ghost.wav')

#details for ghost
gstart = [10,20]
ggoal = []
obsgh = []
ghcoord = [10,20]

#e is length of a square in the grid
e=30

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
grid_coord=[]

# Grids for the map
def createGridVisible(l,objs,objs_h):
    in2=0
    for in2 in range(0,l):
        grid_coord.append(C.create_line(objs[in2].a,objs[in2].b,objs[in2].c,objs[in2].d,fill="wheat"))
        grid_coord.append(C.create_line(objs_h[in2].a,objs_h[in2].b,objs_h[in2].c,objs_h[in2].d,fill="wheat"))

    pass

def drawGrid():
    for grid in grid_coord:
        C.itemconfig(grid,fill="red")

# Draw static obstacles
def createVisibleObstacles(grid):
    lina=len(grid)
    m=0
    n=0
    for any31 in range(0,lina):#say xcord=n
        m=0
        for any32 in range(0,lina):#y coord=m
            if(grid[n][m]==1):

                coordinate2=m*e,n*e,(m+1)*e,(n+1)*e
                #id = C.create_rectangle(coordinate2,fill="#000fff000" )
                obstacle_coord.append(C.create_rectangle(coordinate2,fill="peru" ))
            m=m+1
        n=n+1
    pass

# Redraw obstacles
def drawObstacles():
    for coordinate2 in obstacle_coord:
        C.itemconfig(coordinate2)


for any21 in obstacle_list:
    obj_obs11=any21
    rect=Obstacle_from_pixel_to_grid(obj_obs11,rect)
    grid=update_grid_with_obs(grid,rect)
    global obsgh
    obsgh = rect


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
applenum = 0

top = Tkinter.Tk()
top.title("SnakeMan")
# keyboard interaction
top.bind("<space>",on_key_press)
top.bind("s",on_key_press)
top.bind("<Escape>",on_key_press)
top.bind("v",on_key_press)

# images for apple and ghost
appleimage = Tkinter.PhotoImage(file = 'apple.png')
ghostimage = Tkinter.PhotoImage(file = 'ghost.png')

# Randomly generating apple on the map
def generateApple():
    for i in range(1,100):
        x,y=-1,-1
        while (x==-1 and y==-1) or grid[x][y]!=0 or gstart == [x,y]:
            x= randint(0,gridsize-1)
            y= randint(0,gridsize-1)
        apple.append([x,y])
        #print i

    #apple.append([x,y])
    #C.create_image(x*e+e/2, y*e+e/2, image=appleimage)
    #return x,y

# Redrawing geerated apple

def regenerateApple(i):
    #global obsgh
    [x,y]=apple[i]
    #obsgh.append([x,y])
    C.create_image(x*e+e/2, y*e+e/2, image=appleimage)

# Draw the ghost
def drawGhost(gcoord):
    C.create_image(gcoord[0]*e+e/2,gcoord[1]*e+e/2, image = ghostimage)

counter=0
coordinate=initial_position[0],initial_position[1],e,e

C = Tkinter.Canvas(top, bg="ivory", height=1200, width =1200)
arc=C.create_arc(coordinate,start=30,extent=300,fill="crimson")
angle=45
close =1
shut = 360
flag1=True
createVisibleObstacles(grid)
snake_coord.append(coordinate)

staticgrid=grid
snakespeed = 1.5
snakecolour = 0
colours = [ "crimson", "royalblue", "teal" , "goldenrod" ]

def snake(coord,angle,close,flag12,l1,objs1,objs_h1,grid1,counter,snake_s,orientation):

    global static
    global applenum
    global shut
    global snakespeed
    global snakecolour
    C.delete(Tkinter.ALL)

    global step, paused, QUIT
    if QUIT: #Simulation Loop
        #print("Final size of snake : %s ... quitting"%snake_s)
        top.destroy()

    # Orientation of Snake
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
        coord=coord[0]+snakespeed*a,coord[1]+snakespeed*b,coord[2]+snakespeed*c,coord[3]+snakespeed*d
        snake_coord.append(coord)

    # Mouth movement of snake
    if angle >0 and close ==1:
        angle=angle-5
        if angle ==0:
            close =0
    elif angle<45 and close==0:
        angle =angle+5
        if angle ==45:
            close=1
    # Drawing the grid
    createGridVisible(l1,objs1,objs_h1)
    createVisibleObstacles(grid1)

    # Drawing the snake
    tail = 1
    while tail<=snake_s and len(snake_coord)>=tail*int(e):
        if tail ==1:
           arc = C.create_arc(snake_coord[-1],outline="black",start=shut + angle,extent= (359-2*angle),fill=colours[snakecolour])
        else:
            if len(snake_coord)>(tail-1)*int(e/snakespeed) + int(e/(snakespeed*2)):
                arc = C.create_oval(snake_coord[-(tail-1)*int(e/snakespeed) + int(e/(snakespeed*2))],outline="black",width=0,fill=colours[snakecolour])
            if len(snake_coord)>(tail-1)*int(e/snakespeed):
                arc = C.create_oval(snake_coord[-(tail-1)*int(e/snakespeed)],outline="black",width=0,fill=colours[snakecolour])
        tail = tail+1


    if len(snake_coord) > ceil(e/snakespeed)*(snake_s-1):
        ggoal = [ceil(snake_coord[-int(ceil(e/snakespeed))*(snake_s-1)][0]/e),ceil(snake_coord[-int(ceil(e/snakespeed))*(snake_s-1)][1]/e)]
    else:
        ggoal = [ceil(snake_coord[-1][0]/e),ceil(snake_coord[-1][1]/e)]

    global ghcoord
    gstart = ghcoord
    if not paused:
        ghcoord,rgoal = ghostPlan(gstart,ggoal,obsgh)
        if rgoal and snake_s!=2:
            snake_s=snake_s-1
            #snakespeed = snakespeed - 0.1
            if snake_s<5:
                snakecolour= 0
            elif snake_s<10:
                snakecolour= 1
            if snake_s<15:
                snakecolour= 2
            ghosteatssnake.play()


    drawGhost(ghcoord)
    regenerateApple(applenum)

    if ceil(coord[0]/e)==goal_position[1] and ceil(coord[1]/e)==goal_position[0]:
        print "Reached apple"
        snake_s = snake_s+1
        #snakespeed = snakespeed + 0.1
        if snake_s>5:
            snakecolour= 1
        elif snake_s>10:
            snakecolour= 2
        if snake_s>15:
            snakecolour= 3
        song.play()
        pathtotake=-1
        applenum = applenum +1


        #while pathtotake==-1:
    goal_position[1],goal_position[0]=apple[applenum]
        #    pathtotake = astar_v2(initial_position,grid.tolist(),goal_position,ghcoord)

    if (coord[0]%e==0 and coord[1]%e==0):
        if len(snake_coord)>int(ceil(e/snakespeed))*(snake_s)-1:
            grid1[int(ceil(snake_coord[-int(ceil(e/snakespeed))*(snake_s)-1][1]/e)),int(ceil(snake_coord[-int(ceil(e/snakespeed))*(snake_s)-1][0]/e))]=0
        grid1[int(ceil(snake_coord[-1][1]/e)),int(ceil(snake_coord[-1][0]/e))]=2
        pathtotake = astar_v2([int(ceil(coord[1]/e)),int(ceil(coord[0]/e)),orientation],grid1.tolist(),goal_position,ghcoord)
        top.after(10,lambda: snake(coord,angle,close,flag12,l1,objs1,objs_h1,grid1,counter,snake_s,pathtotake[1][2]))
    else:
        top.after(10,lambda: snake(coord,angle,close,flag12,l1,objs1,objs_h1,grid1,counter,snake_s,orientation))

C.pack()

pathtotake=-1
generateApple()

#while pathtotake==-1:
goal_position[1],goal_position[0]=apple[applenum]
regenerateApple(applenum)

pathtotake = astar_v2(initial_position,grid.tolist(),goal_position,ghcoord)

#print goal_position
top.after(10,lambda: snake(coordinate,angle,close,flag1,l,objs,objs_h,grid,counter,snake_size,pathtotake[1][2]))

top.mainloop()

print("--- %s seconds ---" % float(time.time() - start_time)/60)
