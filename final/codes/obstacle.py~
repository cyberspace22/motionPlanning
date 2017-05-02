import numpy as np

#last work
def backEndGrid(ab1):
    print('grid creation start here')
    grid=[]
    a12=[]
    for a in range(0,ab1):
        a12.append(0)
    for b in range(0,ab1):
        grid.append(a12)

    l=len(grid)
    for a in range (0,l):
        print(grid[a])
    grid=np.array(grid)
    return grid

def Obstacle_from_pixel_to_grid(obj_obs1,rect1):
    print('started Obstacle_from_pixel_to_grid(obj_obs1,rect1)')
    p1=[0,0]
    p2=[0,0]

    if(obj_obs1.x1==obj_obs1.x2):
        print('invalid obstacle co-ords')
        return 0
    if(obj_obs1.y1==obj_obs1.y2):
        print('invalid obstacle co-ords')
        return 0


    if(obj_obs1.x1<obj_obs1.x2):
        #print('point worked1')
        p1[0]=obj_obs1.x1
        p2[0]=obj_obs1.x2

    if (obj_obs1.x1>obj_obs1.x2):
        #print('point worked2')
        p1[0]=obj_obs1.x2
        p2[0]=obj_obs1.x1


    if(obj_obs1.y1<obj_obs1.y2):
        #print('point worked3')
        p1[1]=obj_obs1.y1
        p2[1]=obj_obs1.y2

    if(obj_obs1.y1>obj_obs1.y2):
        #print('point worked4')
        p1[1]=obj_obs1.y2
        p2[1]=obj_obs1.y1

    print('p1 an p2 '+str(p1)+'  '+str(p2))
    a1231=1
    xp=int(int(p2[0]-p1[0])/100*a1231)
    yp=int(int(p2[1]-p1[1])/100*a1231)
    #print('x pieces and y pieces')
    #print(xp)
    #print(yp)

    # we need keep y const and increase x 3 times and orginal x
    xLL=int(p1[0]/100*a1231)
    yLL=int(p1[1]/100*a1231)

    yo=yLL
    #print('(xLL,yLL) first rect = '+str(xLL)+' , '+str(yLL))


    for any1 in range(0,xp):
        #print(xLL)
        for any2 in range(0,yp):
            #print('y shouldnt change')
            #print(yLL)
            pnew=[xLL,yLL]
            rect1.append(pnew)
            yLL=yLL+1
        yLL=yo
        xLL=xLL+1

    print(rect1)
    return rect1



def update_grid_with_obs(grid1,rects1):
    lt=len(rects1)
    for t in rects1:
        a=t[0]
        b=t[1]
        grid1[a][b]=1
    return grid1




