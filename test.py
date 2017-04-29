from astar_siddhav import astarold
from math import sqrt
from math import exp
import time
import functools

inf = float("inf")

grid = [[0 for x in range(20)] for y in range(20)]
#heuristic = [[0 for x in range(20)] for y in range(20)]
obs = [[2,2,2,3],[7,9,3,2],[4,4,3,3],[18,7,2,1]] #[x,y,r,c]
gstart = [6,16] #there is a function to calculate this in the astar_siddhav.py code but not being used currently
#currently only a set value is  being used for ghost. Its position can also  be passed as a parameter in the function
start = [4, 3, 2] #[grid row, grid col, direction]
goal = [6, 18]
'''points,plan = astarold(start,grid,obs,goal)
print("Printing from test file")
for pr in range(len(plan)):
    print(plan[pr])
print(points)'''


#adding code for ghost
#may be moved to the master function
def dotp(x,y):
    z = x[0]*y[0] + x[1]*y[1]
    return z
#sensing distance
sens = 3
#Parameters for force
kpar = 1.5
mpar = 2
t0par = 3
epspar = 0
radius = 0.5
prefspeed = 1.2
maxspeed = 1.6
pos = gstart
vel = [0,0]
goal = [5,6] #this will be the current position of the snake
gvel = [goal[0]-pos[0],goal[1]-pos[1]]
gvel = [gvel[0]/(sqrt(dotp(gvel,gvel)))*prefspeed,gvel[1]/(sqrt(dotp(gvel,gvel)))*prefspeed]
reachedgoal = False
ghost = [pos,vel,gvel,goal,radius,prefspeed,maxspeed,reachedgoal]
obstacles = [[5,5,0,0],[5,6,0,0],[6,5,0,0],[6,6,0,0]]
def sensrad(ghost,obstacles):
    obsvar = []
    for ob in obstacles:
        dist = sqrt((ghost[0][0]-ob[0])**2 + (ghost[0][1]-ob[1])**2)
        if(dist < sens):
            obsvar.append(ob)
    return obsvar


def ttciso(x,agent):
    tr = agent[4] * 2
    tw = [x[0] - agent[0][0],x[1] - agent[0][1]]
    c = dotp(tw,tw) - tr*tr
    if (c < 0):
        return(0)
    tv = [x[2] - agent[1][0],x[3] - agent[1][1]]
    a = dotp(tv,tv) - epspar**2
    b = dotp(tw,tv) - epspar*tr
    if (b > 0):
        return(inf)
    discr = b*b - a*c
    if (discr <= 0):
        return(inf)
    tau = c/(-b + sqrt(discr))
    if(tau < 0):
        return(inf)
    return tau

def computeisoforce(ob,nagent,tc):
    #find relative displacement
    disc = 0
    fce = []
    disp = [ob[0] - nagent[0][0],ob[1] - nagent[0][1]]
    #print("displacement %s" %disp)
    relvel = [ob[2] - nagent[3][0],ob[3] - nagent[3][1]]
    #print("V = %s" %relvel)
    r = mg([disp[0]+relvel[0]*tc,disp[1]+relvel[1]*tc])
    #print("r %s" %r)
    disc = (dotp(disp,relvel) - r*epspar)**2 - ((mg(relvel)**2) - epspar**2)*(mg(disp)**2 - r**2)
    #print("discriminant %s" %disc)
    fce = [(disp[0] + relvel[0]*tc)/sqrt(disc),(disp[1] + relvel[1]*tc)/sqrt(disc)]
    cal = ((kpar*exp(-tc/t0par))/tc**(mpar+1))*(mpar + tc/t0par)
    fce[0] = fce[0]*cal
    fce[1] = fce[1]*cal
    #print(fce)
    return fce

def updatePos(dt):
    fg = [ghost[2][0] - ghost[1][0],ghost[2][1] - ghost[1][1]]/0.5
    #find obstacles within a sensing radius
    obs = sensrad(ghost,obstacles)
    if not ghost[-1]:
        for o in obs:
            tc = ttciso(o,ghost)
            if tc > 0 and tc < inf:
                fce = computeisoforce(o,ghost,tc)
                fg += fce
                print("col")
        force = fg
        global reachedgoal
        reachedgoal = True #this is to find if ghost has caught snake
        ghost[1] += [force[0]*dt,force[1]*dt]
        #cap it to max speed
        mg = sqrt(dotp(ghost[1],ghost[1]))
        if mg > ghost[6]:
            ghost[1] = [ghost[6]*x/mg for x in ghost[1]]
        #update position
        ghost[0] = [ghost[0][0]+ghost[1][0]*dt,ghost[0][1]+ghost[1][1]*dt]

        #find goal vel for next step
        gv = [ghost[3][0]-ghost[0][0],ghost[3][1]-ghost[0][1]]
        distToGoal = dotp(gv,gv)
        if(distToGoal < adist):
            ghost[-1] = True
        else:
            gv = [ghost[5]*x/sqrt(distToGoal) for x in gv]
            ghost[2] = gv
            reachedgoal = False
