import math
from tkinter import *
from PIL import Image, ImageTk
from pynput import keyboard
import threading
import time


# Orbital object class (i.e. planet, satellite, moon, etc.
# Has some general info
class OrbitObj:
    # Instantiated with mass, position (automatically origin), and velocity (automatically no velocity)
    def __init__(self, mass, pos=[0, 0, 0], vel=[0, 0, 0]):
        self.mass = mass
        # 0 --> x
        # 1 --> y
        # 2 --> z
        self.pos = pos
        self.vel = vel

    def update(self, acc):
        global t
        for j in range(len(self.vel)):
            new_vel = self.vel[j] + (acc[j] * t)
            diff_pos = ((self.vel[j] + new_vel) / 2) * t
            self.vel[j] = new_vel
            self.pos[j] += diff_pos


G = 6.67430 * pow(10, -11)  # Newtonian constant of gravitation

t = 0  # TIME

# Declaring the objects for the moon and the satellite in orbit.
# TODO: Use Keplerian element conversion to find position and velocity for satellite
moon = OrbitObj(mass=7.34767309 * pow(10, 22))
sat = OrbitObj(mass=1916)  # Mass: (National Aeronautics and Space Administration, 2009)

mu = G * moon.mass
thrust = 44037.39
amount_change = 10
window_width = 1500


# ---------------THRUST CODE---------------
def on_press(key):
    global thrust
    if key == keyboard.Key.up or key == keyboard.KeyCode.from_char('w'):
        thrust += amount_change
    elif key == keyboard.Key.down or key == keyboard.KeyCode.from_char('s'):
        thrust -= amount_change


def on_release(key):
    global thrust
    k = key
    # print(k)
    print(thrust)


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# ---------------MAP CODE---------------
root = Tk()
canvas = Canvas(root, width=window_width, height=window_width // 2)
img = ImageTk.PhotoImage(Image.open(r"A:\Python Projects\ScienceProj2122Python\map.tiff")
                         .resize((window_width, window_width // 2)))
canvas.create_image(20, 20, anchor=NW, image=img)
canvas.pack()

# ---------------UI CODE---------------
label = Label(root, text="Keplerian Elements:")
label.pack()

a = 0
semimajor_entry = Entry(root, width=25)
semimajor_entry.insert(0, "Semi-major axis")
semimajor_entry.pack()

e = 0
eccentricity_entry = Entry(root, width=25)
eccentricity_entry.insert(0, "Eccentricity")
eccentricity_entry.pack()

inclin = 0
inclination_entry = Entry(root, width=25)
inclination_entry.insert(0, "Inclination")
inclination_entry.pack()

omega = 0
ascension_entry = Entry(root, width=25)
ascension_entry.insert(0, "Right ascension of ascending node")
ascension_entry.pack()

w = 0
perigee_entry = Entry(root, width=25)
perigee_entry.insert(0, "Argument of perigee")
perigee_entry.pack()


def submit():
    global a, e, inclin, omega, w
    # print(semimajor_entry.get())
    # print(eccentricity_entry.get())
    # print(inclination_entry.get())
    # print(perigee_entry.get())

    a = semimajor_entry.get()
    e = eccentricity_entry.get()
    inclin = inclination_entry.get()
    omega = ascension_entry.get()
    w = perigee_entry.get()

    frame = Frame(root, height=20, width=100).pack()
    l1 = Label(frame, text="Semimajor axis: "+a).pack()
    l2 = Label(frame, text="Eccentricity: "+e).pack()
    l3 = Label(frame, text="Inclination: "+inclin).pack()
    l3 = Label(frame, text="Right ascension of ascending node: " + omega).pack()
    l4 = Label(frame, text="Argument of perigee: "+w).pack()

    semimajor_entry.pack_forget()
    eccentricity_entry.pack_forget()
    inclination_entry.pack_forget()
    ascension_entry.pack_forget()
    perigee_entry.pack_forget()
    button.pack_forget()


button = Button(root, text="Submit", command=submit)
button.pack()


root.mainloop()
