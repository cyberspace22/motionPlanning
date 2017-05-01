for fuck in range(1,50):

    if(shut_x==False):
        x=x+1
        if(x>o1-1):
            counter=counter+1
            shut_x=True
            shut_y=False

            pass

        pass
    if(shut_y==False):
        y=y+1
        if(y>o1-1):
            counter=counter+1
            shut_y=True
            shut_x=False
            pass

        pass

    print('(x,y) : '+str(x)+' , '+str(y))
