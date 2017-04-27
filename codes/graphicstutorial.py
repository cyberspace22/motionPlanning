from graphics import *
import time

win = GraphWin()
pt =Point(100,50)
pt.draw(win)
cir=Circle(pt,25)
cir.draw(win)
for i in range(0,100):
    cir.setOutline('gray')
    cir=Circle(Point(100+i,50),25)
    cir.draw(win)
    cir.setOutline('black')
    time.sleep(1)
