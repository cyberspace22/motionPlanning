print('A star')
goal = [13,13]
goal_Theta=90
pos=[0,0]
OptimumPath=[]
OptimumPath.append(pos)
'''grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]'''
grid = [[0 for x in range(20)] for y in range(20)]
obs = [[2,2,2,3],[7,9,3,2]] #[x,y,r,c]
#setobs(grid,obs)
initial_theta=0
CurCost=0;
 #print(str(grid[:][2]))
def setobs(grid,obs):
    for o in obs:
        x = o[0]
        y = o[1]
        for r in range(o[2]):
            for c in range(o[3]):
                grid[x+r][y+c] = 1
    print(grid)
setobs(grid,obs)
print(grid)
def selectNewNode():
    for loc in locations:


        pass
    pass

def costCalc(locations):



    pass




def CCupdate(CCFinal):
    CCFinal=CCFinal + 1
    return CCFinal




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

def motionByAstar(pos,goal,grid,CurCost,OptimumPathMat):
    count = 0
    reached = False


    while (reached== False):
         #count=count+1
         #if(count>10):
            #break
        MaxCost=10000
        CompeteCost=10001
        results=scanGrid(grid,pos)
        Locations = newLocations(pos,results)
        #this can give me problems in future.
        CurCost=CurCost+1

        for an in Locations:
            posnew=an
            print('Manhatten Cost for current position: '+str(posnew)+' goal : '+str(goal))
            cc=ManhatanCost(posnew,goal)
            print(cc)
            print('curent cost : '+str(CurCost))

            CompeteCost=cc+CurCost

            print('CompeteCost : '+str(CompeteCost)+'  max cost : '+str(MaxCost))
            if(MaxCost>CompeteCost):
                MaxCost=CompeteCost
                nextpos=an

             #print(cc)
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
            return OptimumPathMat
    pass

OptimumPathFinal=motionByAstar(pos,goal,grid,CurCost,OptimumPath)
print(OptimumPathFinal)
 #results=scanGrid(grid,pos)
