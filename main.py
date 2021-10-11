import math
from tkinter import *
from PIL import Image, ImageTk
from pynput import keyboard
import threading
import time


# Orbital object class (i.e. planet, satellite, moon, etc.
# Has some general info
class OrbitObj:
    # Instantiated with mass.
    def __init__(self, mass):
        self.mass = mass


G = 6.67430 * pow(10, -11)  # Newtonian constant of gravitation

t = 0  # TIME (increments every second)

# Declaring the objects for the moon and the satellite in orbit.
# TODO: Use Keplerian element conversion to find position and velocity for satellite
moon = OrbitObj(mass=7.34767309 * pow(10, 22))
sat = OrbitObj(mass=1916)  # Mass: (National Aeronautics and Space Administration, 2009)

mu = G * moon.mass
thrust = 44037.39       # Thrust variable
amount_change = 10      # How much thrust changes for each button press
window_width = 1500     # For rendering the canvas & map.


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


def incremenet():
    global t
    while True:
        t += 1
        time.sleep(1)
        t_string.set(str(t))
        root.update_idletasks()


t1 = threading.Thread(target=incremenet)
t_string = StringVar(root, '0')


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
    global a, e, inclin, omega, w, t, t_string
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
    l1 = Label(frame, text="Semi-major axis: "+a).pack()
    l2 = Label(frame, text="Eccentricity: "+e).pack()
    l3 = Label(frame, text="Inclination: "+inclin).pack()
    l3 = Label(frame, text="Right ascension of ascending node: " + omega).pack()
    l4 = Label(frame, text="Argument of perigee: "+w).pack()

    t1.start()
    l5 = Label(frame, textvariable=t_string).pack()

    semimajor_entry.pack_forget()
    eccentricity_entry.pack_forget()
    inclination_entry.pack_forget()
    ascension_entry.pack_forget()
    perigee_entry.pack_forget()
    button.pack_forget()


button = Button(root, text="Submit", command=submit)
button.pack()

root.mainloop()
