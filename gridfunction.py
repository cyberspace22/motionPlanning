'''print('grid creation start here')
grid=[]
a12=[]
for a in range(0,10):
    a12.append(0)
for b in range(0,10):
    grid.append(a12)

l=len(grid)
for a in range (0,l):
    print(grid[a])
'''
#this is probably a shorter way to do it
grid = [[0 for x in range(10)] for y in range(10)]
print(grid)
