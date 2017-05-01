from Tkinter import *

##
w=0
h=0
##
class AllTkinterWidgets2:
    a=00
    b=00
    def __init__(self, master,a,b):


        c = Frame(master, bg='red',width=a+200, height=b+200, bd=1)
        c.pack()

        iframe5 = Frame(c, bd=2, relief=RAISED)
        iframe5.pack(expand=1, fill=X, pady=10, padx=5)
        c = Canvas(iframe5, bg='green', width=a, height=b)
        c.pack()
        for i in range(25):
            c.create_oval(200,200,300,300, fill='blue')
        c.create_text(260, 80, text='Snake_man Vs Ghost', font=('verdana', 10, 'bold'))
        iframe5.pack(expand=1, fill=X, pady=20, padx=20)




toot=Tk()

w = 1100 # width for the Tk root
h = 400 # height for the Tk root

a1=AllTkinterWidgets2(toot,w,h)
toot.title('Test yp')
a1=a1.a
print(a1)

# get screen width and height
ws = toot.winfo_screenwidth() # width of the screen
hs = toot.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
toot.geometry('%dx%d+%d+%d' % (w, h, x, y))



toot.mainloop()
