from operator import itemgetter
# The car can perform 3 actions: 0: right turn, 1: no turn, 2: left turn
action = [-1, 0, 1]
#action  = [0,0,0]
action_name = ['R', 'F', 'L']
dir_name = ['U','L','D','R']
actn = 0
cost = [1, 1, 1] # corresponding cost values R F L
orientation = [0, 1, 2, 3] #U L D R
# GRID:
#     0 = navigable space
#     1 = unnavigable space
grid = [[0 for x in range(20)] for y in range(20)]
heuristic = [[0 for x in range(20)] for y in range(20)]
obs = [[2,2,2,3],[7,9,3,2],[4,4,3,3],[18,7,2,1]] #[x,y,r,c]
setobs(grid,obs)
setobs(plan,obs)

start = [4, 3, 2] #[grid row, grid col, direction]

goal = [19, 19] #[grid row, grid col] initial goal
#heuristic fn
def buildheuristics(grid,goal,heuristic):
    for r in range(len(heuristic)):
        for c in range(len(heuristic[0])):
            heuristic[r][c] = (abs(goal[0]-r) + abs(goal[1] - c))

def setobs(grid,obs):
    for o in obs:
        x = o[0]
        y = o[1]
        for r in range(o[2]):
            for c in range(o[3]):
                grid[x+r][y+c] = 1

def neighbours(curr,neigh):
    r = curr[3]
    c = curr[4]
    #assuming only up down left right neighbours
    if (r-1 >= 0):
        #there exists a up neighbor and is navigable space
        if not (grid[r-1][c]):
            neigh.append([r-1,c,0,0])
    if (r+1 < len(grid)):
        #there exists a down neighbor and is navigable space
        if not (grid[r+1][c]):
            neigh.append([r+1,c,0,0])
    if (c-1 >= 0):
        #there exists a left neighbor and is navigable space
        if not (grid[r][c-1]):
            neigh.append([r,c-1,0,0])
    if (c+1 < len(grid[0])):
        #there exists a right neighbor and is navigable space
        if not (grid[r][c+1]):
            neigh.append([r,c+1,0,0])

def movecost(curr,coord):
    r = curr[3] #store the row of current
    c = curr[4] #store the column of current
    orient = curr[5]    #store the orientation of current
    mcost = 0      #variable for movement cost
    actn = 0        #variable for action
    if r == coord[0]:
        if coord[1] == c - 1:
            #left neighbor
            if orient == 0: #if facing up
                orient = orient + action[2]
                mcost = cost[2]
                actn = 2
            elif orient == 1:   #if facing left
                orient = orient + action[1]
                mcost = cost[1]
                actn = 1
            elif orient == 2:   #if facing down
                orient = orient + action[0]
                mcost = cost[0]
                actn = 0
            elif orient == 3:
                mcost = 50
        else:
            #right neigbor
            if orient == 0: #if facing up
                orient = orient + action[0]
                mcost = cost[0]
                actn = 0
            elif orient == 2:   #if facing down
                orient = orient + action[2]
                mcost = cost[2]
                actn = 2
            elif orient == 3:   #if facing right
                orient = orient + action[1]
                mcost = cost[1]
                actn = 1
            elif orient == 1:
                mcost = 50
    elif c == coord[1]:
        if coord[0] == r - 1:
            #up
            if orient == 0: #if facing up
                orient = orient + action[1]
                mcost = cost[1]
                actn = 1
            elif orient == 1:   #if facing left
                orient = orient + action[0]
                mcost = cost[0]
                actn = 0
            elif orient == 3:   #if facing right
                orient = orient + action[2]
                mcost = cost[2]
                actn = 2
            elif orient == 2:
                mcost = 50
        else:
            #down
            if orient == 3: #if facing right
                orient = orient + action[0]
                mcost = cost[0]
                actn = 0
            elif orient == 1:   #if facing left
                orient = orient + action[2]
                mcost = cost[2]
                actn = 2
            elif orient == 2:   #if facing down
                orient = orient + action[1]
                mcost = cost[1]
                actn = 1
            elif orient == 0:
                mcost = 50
    if (orient == -1):
        orient = 3
    elif (orient == 4):
        orient = 0
    coord[2] = orient
    coord[3] = actn
    return mcost
def compute_plan(grid,start,goal,cost,heuristic):
    parent = [[[[0 for d in range(3)] for t in range(4)] for row in range(len(grid[0]))] for col in range(len(grid))]
    clsd = [] #variable for the closed spaces
    x = start[0]
    y = start[1]
    theta = start[2]
    g = 0
    h = heuristic[x][y]
    f = g+h
    openvar = [[f, g, h, x, y, theta,1]]
    parent[x][y][theta] = [500,500,500] #in order to identify the start node
    while True:
        flg = 0 #flag to check if current state is in closed or open or neither
        neigh = []#variable for neighbors
        current = openvar[0]
        del openvar[0]
        clsd.append(current)
        neighbours(current,neigh)#find neighbors
        tht = 0 #theta
        cst = 0 #cost
        for coord in neigh:#for every accessible neighbor found
            cst = current[1] + movecost(current,coord)
            #coord = [x,y,theta,action]
            tht = coord[2]
            act = coord[3]
            flg = 0
            for a in range(len(clsd)): #check if in closed
                if ((clsd[a][3] == coord[0]) and (clsd[a][4] == coord[1]) and (clsd[a][5] == coord[2])):
                    flg = 1 #set flag since found in closed
                    if cst < clsd[a][1]: #only for inadmissible heuristics
                        del clsd[a]
                        flg = 0
                    break
            if flg == 1:
                continue
            for a in range(len(openvar)):   #check if in open
                if ((openvar[a][3] == coord[0]) and (openvar[a][4] == coord[1])and (openvar[a][5] == coord[2])):
                    flg = 1
                    if cst < openvar[a][1]: #if lower cost, update and add parent
                        openvar[a][0] = cst + openvar[a][2]
                        openvar[a][1] = cst
                        openvar[a][5] = tht
                        openvar[a][6] = act
                        parent[coord[0]][coord[1]][coord[2]] = [current[3],current[4],current[5],coord[3]]
                        openvar.sort(key=lambda xa: xa[0])
                        break
            if flg == 0:    #if found in neither
                gn = cst    #set g(neighbor) = cost
                hn = heuristic[coord[0]][coord[1]]
                fn = gn + hn    #set f
                tht = coord[2]  #set theta
                act = coord[3]  #set action
                parent[coord[0]][coord[1]][coord[2]] = [current[3],current[4],current[5],coord[3]]
                op = [fn,gn,hn,coord[0],coord [1],tht,act]
                openvar.append(op)#add to open
                openvar.sort(key=lambda x: x[0]) #sort the openvariable
        if (current[3] == goal[0] and current[4] == goal[1]):
            print("goal reached!")
            break
    #get current data to trace back the path
    x = current[3]
    y = current[4]
    actn = current[6]
    ori = current[5]
    plan[x][y] = dir_name[ori] #set the action in plan for final node
    while not (parent[x][y][ori] == [500,500,500]):
        #print(x,y,ori)
        #actn = data[x][y][6]
        [x,y,ori,actn] = parent[x][y][ori] #set action in plan for all other nodes
        plan[x][y] = dir_name[ori]
    return plan

def show(p):
    for i in range(len(p)):
        print p[i]
plan =[['-' for row in range(len(grid[0]))] for col in range(len(grid))]
buildheuristics(grid,goal,heuristic)
show(compute_plan(grid, start, goal, cost,heuristic))
