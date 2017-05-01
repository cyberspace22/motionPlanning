print('A star support file')
# the (x,y,theta) model is used you can't move without having a proper orientation

pos=[4,3,0]
#facing to right on 2d world.

goal = [2, 0, 0]
#facing to right on 2d world.

CurCost=0;
path_action_storage=[]


grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
 #path_action_storage=[] (x,y,theta)
#data in this can be like [p1,p2,...]  and symbol printed like this > v A <
def thetaCorrection():
    #location is about to be changed then we check if theta is correct.. if not change it
    #and add 1 movement cost to previous CurCost
    delta=newpos-pos
    #delta will look like this
    #(0,-1) for left movement (0,1) for right movement
    #(-1,0) for up movement (1,0) fo down movement
