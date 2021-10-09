from tkinter import *
from PIL import Image, ImageTk
from pynput import mouse

root = Tk()
canvas = Canvas(root, width=1920, height=1080)
canvas.pack()
img = ImageTk.PhotoImage(Image.open(r"A:\Python Projects\ScienceProj2122Python\map.tiff"))
canvas.create_image(20, 20, anchor=NW, image=img)


# Orbital object class (i.e. planet, satellite, moon, etc.
# Has some general info
class OrbitObj:
    # Instantiated with mass, position (automatically origin), and velocity (automatically no velocity)
    def __init__(self, mass, pos=[0,0,0], vel=[0,0,0]):
        self.mass = mass
        self.pos = pos
        self.vel = vel


root.mainloop()