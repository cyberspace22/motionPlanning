import Tkinter

root = Tkinter.Tk()
canvas =Tkinter.Canvas(root)
canvas.grid(row = 0, column = 0)
photo = Tkinter.PhotoImage(file = 'test.gif')
canvas.create_image(0, 0, image=photo)
root.mainloop()
