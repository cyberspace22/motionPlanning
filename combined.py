import numpy as np
from math import sqrt
from Tkinter import *
import time
import functools


#Drawing parameters
pixelsize = 1024
framedelay = 30
drawVels = True
QUIT = False
paused = False
step = False
circles = []
velLines = []
gvLines = []



#Initalize parameters to run a simulation
# the simulation time step
dt = 0.05
scenarioFile='snake_agent.csv'
# export the simulation?
doExport = True
# the simulated agents
agents = []
# keep track of the agents' traces
trajectories = []
# keep track of simulation iterations
ittr = 0
#how many time steps we want to simulate
maxIttr = 500
# simuation time
globalTime = 0
# is the agent close to its goal?
goalRadiusSq = 1
# have all agents reached their goals
reachedGoals = False
# the goal force scale
xi = 0.5
#num agets
num = 0

angle=30
close=1

grid = [[0 for x in range(20)] for y in range(20)]
obs = [[5,5,2,2]] #[x,y,r,c]
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
setobs(grid,obs)
nmap = np.array(grid)

def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def astar(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    while oheap:

        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))

    return False


def readScenario(fileName, scalex=1., scaley=1.):

    if fileName=='allway_agents.csv':
        scalex = 0.75
        scaley = 2

    # it may be better to define an Agent class, here I'm using a lazy approach
    fp = open(fileName, 'r')
    lines = fp.readlines()
    fp.close()
    for line in lines:
        tokens = line.split(',')
        id = int(tokens[0]) # the id of the agent
        gid = int(tokens[1]) # the group id of the agent
        if gid==1:
            pos = np.array([float(tokens[2]), float(tokens[3])])
            vel = np.zeros(2) # the velocity of the agent
            goal = np.array([float(tokens[2]), float(tokens[3])]) # the goal of the agent
            prefspeed = float(0) # the preferred speed of the agent
            gvel = goal-pos # the goal velocity of the agent
            #gvel = gvel/(sqrt(gvel.dot(gvel)))*prefspeed
            maxspeed = float(0) # the maximum sped of the agent
            radius = float(tokens[4]) # the radius of the agent
        else:
            pos = np.array([float(tokens[2]), float(tokens[3])]) # the position of the agent
            vel = np.zeros(2) # the velocity of the agent
            goal = np.array([float(tokens[4]), float(tokens[5])]) # the goal of the agent
            prefspeed = float(tokens[6]) # the preferred speed of the agent
            gvel = goal-pos # the goal velocity of the agent
            gvel = gvel/(sqrt(gvel.dot(gvel)))*prefspeed
            maxspeed = float(tokens[7]) # the maximum sped of the agent
            radius = float(tokens[8]) # the radius of the agent
        agents.append([id, gid, pos, vel, gvel, goal, radius, prefspeed, maxspeed, False])

    # define the boundaries of the environment
    positions = [row[2] for row in agents]
    goals = [row[5] for row in agents]
    x_min =	min(np.amin(np.array(positions)[:,0]), np.amin(np.array(goals)[:,0]))*scalex - 2.
    y_min =	min(np.amin(np.array(positions)[:,1]), np.amin(np.array(goals)[:,1]))*scaley - 2.
    x_max =	max(np.amax(np.array(positions)[:,0]), np.amax(np.array(goals)[:,0]))*scalex + 2.
    y_max =	max(np.amax(np.array(positions)[:,1]), np.amax(np.array(goals)[:,1]))*scaley + 2.

    num = len(agents);

    return x_min, x_max, y_min, y_max

def initWorld(canvas):
    print ("")
    print ("Simulation of Agents on a flat 2D torus.")
    print ("Agents do not avoid collisions")
    print ("Green Arrow is Goal Velocity, Red Arrow is Current Velocity")
    print ("SPACE to pause, 'S' to step frame-by-frame, 'V' to turn the velocity display on/off.")
    print ("")

    colors = ["white","blue","yellow", "#FAA"]
    for agent in agents:
        if agent[1]!=1:
            circles.append(canvas.create_arc(0, 0, agent[6], agent[6],start=30,extent=300, fill=colors[agent[1]%4])) # color the disc of an agent based on its group id
        else:
            circles.append(canvas.create_rectangle(0,0,agent[6],agent[6], fill=colors[agent[1]%4]))
        #circles.append(agent[6])
        velLines.append(canvas.create_line(0,0,10,10,fill="red"))
        gvLines.append(canvas.create_line(0,0,10,10,fill="green"))

def drawWorld():
    global angle,close
    for i in range(len(agents)):
        agent = agents[i]
        '''
        if not agent[-1]:
            if angle >0 and close ==1:
                angle=angle-1
                if angle ==0:
                    close =0
            elif angle<30 and close==0:
                angle =angle+1
                if angle ==30:
                    close=1
        colors = ["white","blue","yellow", "#FAA"]
        #arc = canvas.create_arc(0, 0, circles[i], circles[i],outline="gray",start=angle,extent=(360-2*angle),fill="gray")
        circ= canvas.create_arc(0, 0, circles[i], circles[i],start=angle,extent=360-2*angle, fill=colors[agent[1]%4])
        '''
        canvas.coords(circles[i],world_scale*(agent[2][0]- agent[6] - world_xmin), world_scale*(agent[2][1] - agent[6] - world_ymin), world_scale*(agent[2][0] + agent[6] - world_xmin), world_scale*(agent[2][1] + agent[6] - world_ymin))
        canvas.coords(velLines[i],world_scale*(agent[2][0] - world_xmin), world_scale*(agent[2][1] - world_ymin), world_scale*(agent[2][0]+ agent[6]*agent[3][0] - world_xmin), world_scale*(agent[2][1] + agent[6]*agent[3][1] - world_ymin))
        canvas.coords(gvLines[i],world_scale*(agent[2][0] - world_xmin), world_scale*(agent[2][1] - world_ymin), world_scale*(agent[2][0]+ agent[6]*agent[4][0] - world_xmin), world_scale*(agent[2][1] + agent[6]*agent[4][1] - world_ymin))
        if drawVels:
            canvas.itemconfigure(velLines[i], state="normal")
            canvas.itemconfigure(gvLines[i], state="normal")
        else:
            canvas.itemconfigure(velLines[i], state="hidden")
            canvas.itemconfigure(gvLines[i], state="hidden")

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

def nextpoint(currpos,goalpos):
    #print(grid)
    #print(str(grid[:][2]))
    path = astar(nmap, currpos, goalpos)
    if path != False:
        path = list (reversed(path))
        print path
        return (path[0])
    else:
        return 0

def updateSim(dt):
    global reachedGoals

    F = [] #force

    for i in range(len(agents)):
        F.append(np.zeros(2))

    for i in range(len(agents)):
        agent = agents[i]
        if not agent[-1]:
            nextt=nextpoint(agent[2],agent[5])
            if nextt!=0:
                gvel = nextt-pos # the goal velocity of the agent
                gvel = gvel/(sqrt(gvel.dot(gvel)))*agent[7]
                F[i] += (gvel-agent[3])/xi
            else:
                F[i] += (agent[4]-agent[3])/xi

    reachedGoals = True
    for i in range(len(agents)):
        agent = agents[i]
        if not agent[-1]:
            agent[3] += F[i]*dt       # update the velocity
            mag = np.sqrt(agent[3].dot(agent[3])) # cap the velocity to max speed
            if (mag > agent[8]): agent[3] = agent[8]*agent[3]/mag

            agent[2] += agent[3]*dt   #update the position

            gvel = agent[5] - agent[2]
            distGoalSq = gvel.dot(gvel)
            # goal has been reached
            if distGoalSq < goalRadiusSq:
                agent[-1] = True
            else:
                #compute the goal velocity for the next time step
                gvel = gvel/sqrt(distGoalSq)*agent[7]
                agent[4] = gvel
                reachedGoals = False

def drawFrame(dt):
    global start_time,step,paused,ittr,globalTime

    if reachedGoals or ittr > maxIttr or QUIT: #Simulation Loop
        print("%s itterations ran ... quitting"%ittr)
        win.destroy()
    else:
        elapsed_time = time.time() - start_time
        start_time = time.time()
        if not paused:
            updateSim(dt)
            ittr += 1
            globalTime += dt
            for agent in agents:
                if not agent[-1]:
                    trajectories.append([agent[0], agent[1], agent[2][0], agent[2][1], agent[3][0], agent[3][1], agent[6], globalTime])

        drawWorld()
        if step == True:
            step = False
            paused = True

        win.title('Snake')
        win.after(framedelay,lambda: drawFrame(dt))

world_xmin, world_xmax, world_ymin, world_ymax = readScenario(scenarioFile)
world_width = world_xmax - world_xmin
world_height = world_ymax - world_ymin
world_scale = pixelsize/world_width

# set the visualizer
win = Tk()
# keyboard interaction
win.bind("<space>",on_key_press)
win.bind("s",on_key_press)
win.bind("<Escape>",on_key_press)
win.bind("v",on_key_press)
# the drawing canvas
canvas = Canvas(win, width=pixelsize, height=pixelsize*world_height/world_width, background="#666")
canvas.pack()
initWorld(canvas)
start_time = time.time()


# the main loop of the program
win.after(framedelay, lambda: drawFrame(dt))
mainloop()
if doExport:
    header = "id,gid,x,y,v_x,v_y,radius,time"
    exportFile = scenarioFile.split('.csv')[0] +"_sim.csv"
    np.savetxt(exportFile, trajectories, delimiter=",", fmt='%d,%d,%f,%f,%f,%f,%f,%f', header=header, comments='')
