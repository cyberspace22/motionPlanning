from math import sqrt
from math import exp
import time
import functools

inf = float("inf")

ghost = []
obstacles = []
dt = 0.1
#sensing distance
sens = 4
#Parameters for force
kpar = 1.5
mpar = 2
t0par = 3
epspar = 0.2
radius = 0.5
prefspeed = 0.35
maxspeed = 0.4
reachedgoal = False
#acceptable distance
adist = 1
#initial velocity
vel = [0,0]
#ghost object
ghost = [[],vel,[],[],radius,prefspeed,maxspeed,reachedgoal]

#dot product
def dotp(x,y):
    z = x[0]*y[0] + x[1]*y[1]
    return z

#check if within sensing radius
def sensrad(ghost,obstacles):
    obsvar = []
    for ob in obstacles:
        dist = (ghost[0][0]-ob[1]-0.5)**2 + (ghost[0][1]-ob[0]-0.5)**2
        if(dist < sens**2):
            obsvar.append(ob)
    #print("nearest obstacles = %s"%obsvar)
    return obsvar

#find isotropic time to collision
def ttciso(x,agent):
    tr = agent[4] * 3
    tw = [-0.5-x[1] + agent[0][0],-0.5-x[0] + agent[0][1]]
    c = dotp(tw,tw) - tr*tr
    if (c < 0):
        return(0)
    tv = [agent[1][0],agent[1][1]]
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

#find magnitude
def mgn(a):
    return sqrt(a[0]*a[0] + a[1]*a[1])

#compute isotropic force
def computeisoforce(ob,nagent,tc):
    disc = 0
    fce = []
    disp = [nagent[0][0] - ob[1]-0.5,nagent[0][1]-ob[0]-0.5]
    relvel = [nagent[3][0],nagent[3][1]]
    r = mgn([disp[0]+relvel[0]*tc,disp[1]+relvel[1]*tc])
    disc = (dotp(disp,relvel) - r*epspar)**2 - ((mgn(relvel)**2) - epspar**2)*(mgn(disp)**2 - r**2)
    fce = [(disp[0] + relvel[0]*tc)/sqrt(disc),(disp[1] + relvel[1]*tc)/sqrt(disc)]
    cal = ((kpar*exp(-tc/t0par))/tc**(mpar+1))*(mpar + tc/t0par)
    fce[0] = fce[0]*cal
    fce[1] = fce[1]*cal
    return fce

def updatePos(dt):
    fg = [(ghost[2][0] - ghost[1][0]),(ghost[2][1] - ghost[1][1])]
    #find obstacles within a sensing radius
    obs = sensrad(ghost,obstacles)
    #if ghost has not reached goal
    if not ghost[-1]:
        for o in obs:
            tc = ttciso(o,ghost)
            if tc > 0 and tc < inf:
                fce = computeisoforce(o,ghost,tc)
                fg = [fg[0]+fce[0],fg[1]+fce[1]]
        #net force
        force = fg
        par = 1
        #capping it to a max force
        if (mgn(force) > 2):
            par = 2/mgn(force)
        force = [force[0]*par,force[1]*par]
        global reachedgoal
        reachedgoal = True #this is to find if ghost has caught snake
        ghost[1] = [ghost[1][0]+force[0]*dt,ghost[1][1]+force[1]*dt]
        #cap it to max speed
        mg = sqrt(dotp(ghost[1],ghost[1]))
        if mg > ghost[6]:
            ghost[1] = [ghost[6]*ghost[1][0]/mg,ghost[6]*ghost[1][1]/mg]
        #update position
        ghost[0] = [ghost[0][0]+ghost[1][0]*dt,ghost[0][1]+ghost[1][1]*dt]
        #find goal vel for next step
        gv = [ghost[3][0]-ghost[0][0],ghost[3][1]-ghost[0][1]]
        distToGoal = dotp(gv,gv)
        if(distToGoal < adist):
            ghost[-1] = True
            print("ghost reached goal!")
        else:
            gv = [ghost[5]*gv[0]/sqrt(distToGoal),ghost[5]*gv[1]/sqrt(distToGoal)]
            ghost[2] = gv
            reachedgoal = False
#call function for planning
def ghostPlan(gstart,goal,obs):
    if not (gstart == goal):
        ghost[-1] = False
    global obstacles
    obstacles = obs
    #this will be the current position of the snake
    pos = gstart
    #compute goal velocity
    gvel = [goal[0]-pos[0],goal[1]-pos[1]]
    gvel = [gvel[0]/(sqrt(dotp(gvel,gvel)))*prefspeed,gvel[1]/(sqrt(dotp(gvel,gvel)))*prefspeed]
    #initialize ghost
    global ghost
    ghost[0] = pos
    ghost[2] = gvel
    ghost[3] = goal
    #update its position according to goal
    updatePos(dt)
    #return new location and status of path to goal
    return ghost[0],reachedgoal
