from SiddhavCode import *
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
#obs = [[2,2,2,3],[7,9,3,2],[4,4,3,3],[18,7,2,1]] #[x,y,r,c]
obs=[]
gstart = [1,1]#ghpst start,mxn n for x movement
start = [0, 0, 2] #[grid row, grid col, direction]

goal = [4, 0] #[grid row, grid col] initial goal


plan =[['-' for row in range(len(grid[0]))] for col in range(len(grid))]
setobs(grid,obs)
setobs(plan,obs)
buildheuristics(grid,goal,heuristic)
updategheuristic(gstart,heuristic)
plan = compute_plan(grid, start, goal, cost,heuristic,action,dir_name,plan)
for pr in range(len(plan)):
    print(plan[pr])
