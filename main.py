import csv
import math
import threading
import time
from tkinter import *
from tkinter import messagebox

import astropy.units as u
import poliastro.bodies
from astropy.units.quantity import Quantity
from matplotlib.pyplot import plot
from PIL import Image, ImageTk
from poliastro.frames.enums import Planes
from poliastro.twobody.orbit import Orbit
from pynput import keyboard

from plot_test import plot_lro_orbit


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
def cartesian_from_elements(a, e, inclin, omega, w, t):
    a_quant = Quantity(value=a, unit='km')  # Semimajor axis
    e_quant = Quantity(value=e)  # Eccentricity
    inclin_quant = Quantity(value=inclin, unit='deg')  # Inclination
    omega_quant = Quantity(value=omega, unit='deg')  # Longitude of Ascending Node
    w_quant = Quantity(value=w, unit='deg')  # Argument of Perigee
    t_quant = Quantity(value=t, unit='deg')  # True anomaly
                
    lro_orbit = Orbit.from_classical(
        attractor=poliastro.bodies.Moon,
        a=a_quant,
        ecc=e_quant,
        inc=inclin_quant,
        raan=omega_quant,
        argp=w_quant,
        nu=t_quant,
        plane=Planes.EARTH_EQUATOR
        )

    x = lro_orbit.r[0] / u.km
    y = lro_orbit.r[1] / u.km
    z = lro_orbit.r[2] / u.km
    return [x, y, z]
    # print(str(x.to_value()) + ", " + str(y.to_value()) + ", " + str(z.to_value()))

# Input  - Cartesian coordinates
# Output - Array of latitude and longitude
"""
# OLD FUNCTION - DO NOT TOUCH (whoops)
def cart_to_spherical(x, y, z):
    lro_orbit_astro = SkyCoord(representation_type='cartesian', x=x, y=y, z=z)
    lat = float(lro_orbit_astro.represent_as(SphericalRepresentation).lat / u.rad)
    long = float(lro_orbit_astro.represent_as(SphericalRepresentation).lon / u.rad)
    # altitude = float(lro_orbit_astro.represent_as(SphericalRepresentation).distance / u.km)  # TODO: Add in calculation accounting for distance from surface to point
    # print("[Lat, Long]: "+str([lat, long]))
    # print("("+str(long)+","+str(lat)+")")
    return [lat, long]
"""
def cart_to_spherical(x, y, z):
    r = math.sqrt(x*x + y*y + z*z)
    
    lat = math.acos(z / r)
    if x > 0:
        long = math.atan(y / x)
    elif x < 0:
        long = math.atan(y / x) + math.pi
    else:
        long = math.pi / 2 

    lat = lat * (180 / math.pi)   # Converting to degrees from radians
    long = long * (180 / math.pi) # Converting to degrees from radians

    print("[Long, Lat]: "+str([long, lat]))
    return [lat, long]

# Input  - (x1, y1, z1) and (x2, y2, z2) to compare
# Output - Orbits have collided at true anomaly 't' (bool)
def compare(x1, y1, z1, x2, y2, z2):
    is_collision = False
    
    rounded_x1 = round(x1, -2)
    rounded_y1 = round(y1, -2)
    rounded_z1 = round(z1, -2)
    
    rounded_x2 = round(x2, -2)
    rounded_y2 = round(y2, -2)
    rounded_z2 = round(z2, -2)

    if (rounded_x1, rounded_y1, rounded_z1) == (rounded_x2, rounded_y2, rounded_z2):
        is_collision = True

    return is_collision

# Input  - (lat, long), color of orbit (identifier)
# Output - N/A
def plot_lat_long(lat, long, color):
    # canvas.create_oval(100, 100, 105, 105, outline="#000", fill="#000", width=1)
    # The above command is to plot a point on a line with the top-left at (100, 100)
    map_w = float(canvas["width"])
    map_h = float(canvas["height"])
    x_p = ((map_w / 2)+20) + long  # +20 to account for padding
    y_p = ((map_h / 2)+20) + lat  # +20 to account for padding
    # print("[x_p, y_p]"+str([x_p, y_p]))
    canvas.create_oval(x_p, y_p, x_p, y_p, outline=color, width=5)

# ---------------UI CODE---------------
def incremenet():
    global t, a, e, inclin, omega, w, canvas
    while t1.is_alive():
        try:
            t += 0.1
            if t >= 360:
                break
            # time.sleep(1)
            t_string.set(str(t))
            root.update_idletasks()
            
            if float(t_string.get()) != 0:
                # Cartesian coordinates
                result = cartesian_from_elements(a, e, inclin, omega, w, t)
                x = float(result[0])
                y = float(result[1])
                z = float(result[2])

                result2 = cartesian_from_elements(a=1795.224, e=0.019296, inclin=85.780, omega=128.208, w=246.531, t=t)
                x2 = float(result2[0])
                y2 = float(result2[1])
                z2 = float(result2[2])

                collide = compare(x, y, z, x2, y2, z2)  # To check if two orbits collide
                
                # Latitude and Longitude Coordinates
                lat_long = cart_to_spherical(x, y, z)
                lat = lat_long[0]
                long = lat_long[1]

                lat_long_2 = cart_to_spherical(x2, y2, z2)
                lat2 = lat_long_2[0]
                long2 = lat_long_2[1]
                with open('values.csv', 'a', newline='') as file:
                    fwriter = csv.writer(file)
                    fwriter.writerow([long2, lat2])
                
                # Plotting onto map
                plot1_color = "yellow" if collide else "red"    # Color changes if collision (Input)
                plot2_color = "yellow" if collide else "blue"   # Color changes if collision (LRO)
                plot_lat_long(lat, long, plot1_color)
                plot_lat_long(lat2, long2, plot2_color)
        except RuntimeError:
            break
    return
        
# Declaring threads for the calculations & orbit plot
t1 = threading.Thread(target=incremenet)
t_string = StringVar(root, '0')
t2 = threading.Thread(target=plot_lro_orbit)  # Poliastro plot thread

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
    t2.start()
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
