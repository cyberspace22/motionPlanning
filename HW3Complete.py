print('A star support file')

Initial_theta=0
current_theta=Initial_theta

theta_log=[]
theta_log.append(current_theta)

goal_Theta=1
goal = [2, 0]

initial_position=[4,3]
pos=initial_position

Intial_cost=0
CurCost=Intial_cost

OptimumPath=[]
OptimumPath.append(pos)
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]


#THETA 0=0 degree right , 1=90 degree up, 2=180 degree left , 3=270 degree down
print('THETA 0=0 degree right , 1=90 degree up, 2=180 degree left , 3=270 degree down')
## code for THETA

posOld=[0,0]
posNew=[-1,0]

def thetaCorrect(current_theta,posOld,posNew,CurCost):
    print('process for theta correction started')
    Correct=False

    O=posOld
    N=posNew


    required_theta=5
    abs_theta=5
    mDelta=N[0]-O[0]
    nDelta=N[1]-O[1]


    if(Correct==False):

        print('Calculating absolute theta based on motion plan')
        if(mDelta==1):
            print('in 3')
            abs_theta=3
            #down
            pass
        if(mDelta==-1):
            print('in 1')
            abs_theta=1
            #up
            pass
        if(nDelta==1):
            abs_theta=0
            print('in 0')
            #right
            pass
        if(nDelta==-1):
            print('in 2')
            abs_theta=2
            #left
            pass
        print('absolute theta calculated')
        print(abs_theta)
        print('current_theta is : ')
        print(current_theta)
        temo=current_theta-abs_theta
        print('current_theta-abs_theta = '+str(temo))

        if(temo<0):
            temo=temo*-1
        CurCost=CurCost+(temo)
        current_theta=abs_theta


    return current_theta,CurCost
    pass














#########################

 #print(str(grid[:][2]))





def ManhatanCost(pos,goal):
    a=goal[0]-pos[0]
    if(a<0):
        a=a*(-1)

    b=goal[1]-pos[1]
    if(b<0):
        b=b*(-1)

    ManhatanCost1=a+b

    return ManhatanCost1;






def newLocations(pos,results):
    print('available location search started')
    locations=[]
    m=pos[0]
    n=pos[1]
    p=[-1,-1]
    print('from this position')
    print(str(pos)+'\n')
    #m+1,n...m,n+1...M-1,n.....M.n-1...
    if(results[0]==0):
         #print('in 1')
        p=[m+1,n]
        locations.append(p)
        pass
    if(results[1]==0):
         #print('in 2')
        p=[m,n+1]
        locations.append(p)
        pass
    if(results[2]==0):
         #print('in 3')
        p=[m-1,n]
        locations.append(p)
        pass
    if(results[3]==0):
         #print('in 4')
        p=[m,n-1]
        locations.append(p)
        pass

    print('resulting locaions')
    print(locations)
    print('available location search ended')
    return locations


def scanGrid(grid,pos):
    print('Scan started ')
    #pos =(m,n)
    #grid has values. and we need 0/1 values of nearby tiles
    m=pos[0]
    n=pos[1]
     #print('check input position ')
     #print(pos)
    ScanResult=[1,1,1,1]

    try:
        if(grid[m+1][n]==0):
             #print(str(m+1)+' : '+str(n))
            ScanResult[0]=0
    except IndexError:
        pass

    try:
        if(grid[m][n+1]==0):
             #print(str(m)+' : '+str(n+1))
            ScanResult[1]=0

    except IndexError:
        pass

    try:
        if(grid[m-1][n]==0):
             #print(str(m-1)+' : '+str(n))
            ScanResult[2]=0
    except IndexError:
        pass

    try:
        if(grid[m][n-1]==0):
             #print(str(m)+' : '+str(n-1))
            ScanResult[3]=0
    except IndexError:
        pass
    print('\nScan results \ndown,right,up,left\n')
    print(ScanResult)
    print('scanning complete\n')
    return ScanResult;

def motionByAstar(pos,goal,grid,CurCost1,OptimumPathMat,current_theta):
    count = 0
    reached = False


    while (reached== False):
         #count=count+1
         #if(count>10):
            #break
        MaxCost=1000000
        CompeteCost=1000001

        results=scanGrid(grid,pos)
        Locations = newLocations(pos,results)
        #this can give me problems in future.
        CurCost1=CurCost1+1

        for an in Locations:
            posnew=an
            print('Manhatten Cost for current position: '+str(posnew)+' goal : '+str(goal))
            cc=ManhatanCost(posnew,goal)
            print(cc)
            print('curent cost : '+str(CurCost1))

            CompeteCost=cc+CurCost1

            print('CompeteCost : '+str(CompeteCost)+'  max cost : '+str(MaxCost))
            if(MaxCost>CompeteCost):
                MaxCost=CompeteCost
                nextpos=an

             #print(cc)

        posNew=nextpos
        posOld=pos

        CurCost1=CurCost1
        current_theta=current_theta
        current_theta,CurCost1=thetaCorrect(current_theta,posOld,posNew,CurCost1)

        theta_log.append(current_theta)

        pos=nextpos
        print('\n new position')
        OptimumPathMat.append(pos)
        print(pos)
        print('\n')
        l=len(grid)
        for a in range (0,l):
            print(grid[a])

        if(pos==goal):
            print "optimum actions found!"

            reached=True
            last_work=goal_Theta-current_theta
            if(last_work<0):
                last_work=last_work*-1
            current_theta=goal_Theta
            CurCost1=CurCost1+last_work
            theta_log.append(current_theta)
            return OptimumPathMat,theta_log,CurCost1






    pass

OptimumPathFinal,theta_log,CurCost=motionByAstar(pos,goal,grid,CurCost,OptimumPath,current_theta)

 #results=scanGrid(grid,pos)
print('######FINAL ANSWER########')
print('grid in question')
l=len(grid)
for a in range (0,l):
    print(grid[a])

print('start point')
print(initial_position)

print('Initial_theta')
print(Initial_theta)

print('goal position')
print(goal)

print('goal theta')
print(goal_Theta)


print('optimal path')
print(OptimumPathFinal)
print('theta log')
print(theta_log)
print('Current Cost')
print(CurCost)

print('Its a durable and scalable version of A star')
