import Tkinter
import tkMessageBox

top = Tkinter.Tk()

coordinate=50,50,100,100
C = Tkinter.Canvas(top, bg="gray", height=500, width =500)
arc=C.create_arc(coordinate,start=30,extent=300,fill="red")
angle=30
close =1

def snake(coord,angle,close):

    if coord[0]>300:
        return
    arc = C.create_arc(coord,outline="gray",start=angle,extent=(360-2*angle),fill="gray")
    coord=coord[0]+1,50,coord[2]+1,100
    if angle >0 and close ==1:
        angle=angle-1
        if angle ==0:
            close =0
    elif angle<30 and close==0:
        angle =angle+1
        if angle ==30:
            close=1
    arc = C.create_arc(coord,start=angle,extent=360-2*angle,fill="red")
    top.after(30,lambda: snake(coord,angle,close))


C.pack()
# the main loop of the program
top.after(30,lambda: snake(coordinate,angle,close))

top.mainloop()
