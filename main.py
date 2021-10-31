import math
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pynput import keyboard
import threading
import time
from sympy import *  # See https://docs.sympy.org/latest/index.html for documentation


# Orbital object class (i.e. planet, satellite, moon, etc.
# Has some general info
from sympy.utilities.lambdify import implemented_function


class OrbitObj:
    # Instantiated with mass.
    def __init__(self, mass):
        self.mass = mass


G = 6.67430 * pow(10, -11)  # Newtonian constant of gravitation

t = 0  # TIME (increments every second)

# Declaring the objects for the moon and the satellite in orbit.
moon = OrbitObj(mass=7.34767309 * pow(10, 22))
sat = OrbitObj(mass=1916)  # Mass: (National Aeronautics and Space Administration, 2009)

mu = G * moon.mass
thrust = 44037.39       # Thrust variable
amount_change = 10      # How much thrust changes for each button press
window_width = 1500     # For rendering the canvas & map.

a = 0
e = 0
inclin = 0
omega = 0
w = 0


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
    global t, a, e, inclin, omega, w
    while True:
        t += 1
        time.sleep(1)
        t_string.set(str(t))
        root.update_idletasks()

        if int(t_string.get()) != 0:
            # Finding eccentricity anomaly using method on this website: http://orbitsimulator.com/sheela/kepler.htm
            to_radians = math.pi / 180
            mean_anomaly = 4.105 * to_radians  # Placeholder value. TODO: Implement math for mean anomaly and convert to radians
            # TODO: Find out what diff and epsilon are?
            diff = 100
            epsilon = 0.0001

            e_anom_old = mean_anomaly + e // 2
            while diff > epsilon:
                e_anom_new = e_anom_old - (e_anom_old * (math.sin(e_anom_old)) - mean_anomaly) // (1 - e * (math.cos(e_anom_old)))
                diff = abs(e_anom_old - e_anom_new)
                e_anom_old = e_anom_new

            e_anom_new = e_anom_new // to_radians
            print("Eccentricity anomaly: "+str(e_anom_new))



            # Cartesian coordinates
            x = a * ((math.cos(e_anom_new) - e) *
                     (math.cos(w) * math.cos(omega) - math.sin(w) * math.sin(omega) * math.cos(inclin)) +
                     ((1-(e**2))**0.5) * (math.sin(e_anom_new) *
                                          (-math.sin(w) * math.cos(omega) -
                                           math.cos(w) * math.sin(omega) * math.cos(inclin)))
                     )
            y = a * ((math.cos(e_anom_new) - e) *
                     (math.cos(w) * math.cos(omega) - math.sin(w) * math.sin(omega) * math.cos(inclin)) +
                     ((1-e**2)**0.5) *
                     (math.sin(e_anom_new) * (-math.sin(w) * math.cos(omega) - math.cos(w) * math.sin(omega) *
                                              math.cos(inclin)))
                     )
            z = a * ((math.cos(e_anom_new) - e) *
                     (math.sin(w) * math.sin(inclin)) +
                     ((1-e**2)**0.5) * (math.sin(e_anom_new) * (math.cos(w) * math.sin(inclin)))
                     )
            print(str(x) + ", " + str(y) + ", " +  str(z))


t1 = threading.Thread(target=incremenet)
t_string = StringVar(root, '0')


label = Label(root, text="Keplerian Elements:")
label.pack()

semimajor_entry = Entry(root, width=25)
semimajor_entry.insert(0, "Semi-major axis")
semimajor_entry.pack()

eccentricity_entry = Entry(root, width=25)
eccentricity_entry.insert(0, "Eccentricity")
eccentricity_entry.pack()

inclination_entry = Entry(root, width=25)
inclination_entry.insert(0, "Inclination")
inclination_entry.pack()

ascension_entry = Entry(root, width=25)
ascension_entry.insert(0, "Right ascension of ascending node")
ascension_entry.pack()

perigee_entry = Entry(root, width=25)
perigee_entry.insert(0, "Argument of perigee")
perigee_entry.pack()


def submit():
    global a, e, inclin, omega, w, t, t_string
    # print(semimajor_entry.get())
    # print(eccentricity_entry.get())
    # print(inclination_entry.get())
    # print(perigee_entry.get())

    try:
        a = float(semimajor_entry.get())
        e = float(eccentricity_entry.get())
        inclin = float(inclination_entry.get())
        omega = float(ascension_entry.get())
        w = float(perigee_entry.get())
    except ValueError:
        # TODO: Make better exception handling for invalid input.
        # Currently, the program terminates if an integer is not entered.
        messagebox.showerror(title="ERROR", message="INVALID INPUT FOR ENTRY")
        root.destroy()

    frame = Frame(root, height=20, width=100).pack()
    l1 = Label(frame, text="Semi-major axis: "+str(a)).pack()
    l2 = Label(frame, text="Eccentricity: "+str(e)).pack()
    l3 = Label(frame, text="Inclination: "+str(inclin)).pack()
    l3 = Label(frame, text="Right ascension of ascending node: " + str(omega)).pack()
    l4 = Label(frame, text="Argument of perigee: "+str(w)).pack()

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
