import Tkinter as tk

self.title = Label(root, text="Brnr", font=("Helvetica", 50), anchor = W, pady = 40, padx = 50)

self.title.pack (anchor = NW)
#creates title widget for title

self.frame = Frame(screen, bd =1)
self.frame.pack(fill = BOTH)
#Creates frame widget under which all other widgets will be kept

self.canvas = Canvas(self.frame,  bd=1,scrollregion=(0,0, 1000, 1000), height = 600)
#creates canvas so that screen can be scrollable

self.scrollbar = Scrollbar(self.frame, command=self.canvas.yview)
#creates scrollbar

self.canvas.config(yscrollcommand=self.scrollbar.set)
#connects the scrollbar to the canvas

self.scrollbar.pack(side=RIGHT, fill=Y)
self.canvas.pack(expand=YES, fill=BOTH)
#packs the scrollbar and canvas so that they fill the remainder of the screen


self.frameC = Frame(bg = "red")
self.canvas.create_window(0,0, anchor = NW, window = self.frameC, width = 200, height = 200)
#creates window on the scrollable area to add other widgets

self.frameC.pack()
self.groupRec = LabelFrame(self.frameC, text ="Recommendations:", font=("Helvetica", 20))
self.groupRec.pack()
self.signupButton = Button(self.groupRec, text="Sign Up", width=10)
self.signupButton.pack(side=RIGHT)
