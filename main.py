import math
import threading
import time
from tkinter import *
from tkinter import messagebox

import poliastro.bodies
from astropy.units.quantity import Quantity
from PIL import Image, ImageTk
from poliastro.frames.enums import Planes
from poliastro.twobody.orbit import Orbit
from pynput import keyboard
from astropy.coordinates import SkyCoord


# Orbital object class (i.e. planet, satellite, moon, etc.
# Has some general info
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

# hi #

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
    # print(thrust)


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# ---------------MAP CODE---------------
root = Tk()
canvas = Canvas(root, width=window_width // 2, height=window_width // 4)
img = ImageTk.PhotoImage(Image.open(r"map.tiff")
                         .resize((window_width // 2, window_width // 4)))
canvas.create_image(20, 20, anchor=NW, image=img)
canvas.pack()

# ---------------CALCULATIONS---------------
# Input  - N/A
# Output - Array of Cartesian coordinates
def cartesian_from_elements():
    a_quant = Quantity(value=a, unit='km')
    e_quant = Quantity(value=e)
    inclin_quant = Quantity(value=inclin, unit='deg')
    omega_quant = Quantity(value=omega, unit='deg')
    w_quant = Quantity(value=w, unit='deg')
    t_quant = Quantity(value=t, unit='deg')
                
    lro_orbit = Orbit.from_classical(
        attractor=poliastro.bodies.Moon,
        a=a_quant,
        ecc=e_quant,
        inc=inclin_quant,
        raan=omega_quant,
        argp=w_quant,
        nu=t_quant,
        plane=Planes.BODY_FIXED
        )

    x = lro_orbit.r[0]
    y = lro_orbit.r[1]
    z = lro_orbit.r[2]
    return [x, y, z]
    # print(str(x.to_value()) + ", " + str(y.to_value()) + ", " + str(z.to_value()))

# Input  - Cartesian coordinates
# Output - Array of latitude and longitude
def cart_to_spherical(x, y, z):
    lro_orbit_astro = SkyCoord(representation_type='cartesian', x=x, y=y, z=z)
    lat = float(lro_orbit_astro.to_string().split()[0])
    long = float(lro_orbit_astro.to_string().split()[1])
    print("[Lat, Long]: "+str([lat, long]))
    return [lat, long]

# ---------------UI CODE---------------
def incremenet():
    global t, a, e, inclin, omega, w, canvas
    while True:
        try:
            t += 1
            if t >= 360:
                t = 0
            # time.sleep(1)
            t_string.set(str(t))
            root.update_idletasks()

            if int(t_string.get()) != 0:
                # Cartesian coordinates
                result = cartesian_from_elements()
                x = result[0]
                y = result[1]
                z = result[2]

                # Latitude and Longitude Coordinates
                lat_long = cart_to_spherical(x, y, z)
                lat = lat_long[0]
                long = lat_long[1]

                # Plotting onto map
                # canvas.create_oval(100, 100, 105, 105, outline="#000", fill="#000", width=1)
                # The above command is to plot a point on a line with the top-left at (100, 100)
                map_w = float(canvas["width"])
                map_h = float(canvas["height"])

                x = map_w/2
                y = map_h/2
                print("[x, y]"+str([x, y]))
                canvas.create_oval(x, y, x, y, fill="#000", width=5)
        except RuntimeError:
            # When the window is closed, the thread stops
            return


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
        # Program lets user know if element values are invalid. (i.e. not a float)
        messagebox.showerror(title="ERROR", message="INVALID INPUT FOR ENTRY")
        return

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
