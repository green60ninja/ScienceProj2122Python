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

from plot_test import plot_lro_orbit


window_width = 1500     # For rendering the canvas & map.

a = 0  # semimajor axis
e = 0  # eccentricity
inclin = 0  # inclination
omega = 0  # right ascension of ascending node
w = 0  # argument of perigee
t = 0  # true anomaly

a_2 = 0
e_2 = 0
inclin_2 = 0
omega_2 = 0
w_2 = 0

# ---------------MAP CODE---------------
root = Tk()
canvas = Canvas(root, width=window_width // 2, height=window_width // 4)
img = ImageTk.PhotoImage(Image.open(r"map.tiff")
                         .resize((window_width // 2, window_width // 4)))
canvas.create_image(20, 20, anchor=NW, image=img)
canvas.pack()

# ---------------CALCULATIONS---------------
# Function to convert the Classical Keplerian elements into cartesian coordinates
# Input  - N/A
# Output - Array of Cartesian coordinates
def cartesian_from_elements(a, e, inclin, omega, w, t):
    a_quant = Quantity(value=a, unit='km')  # Semimajor axis (kilometers)
    e_quant = Quantity(value=e)  # Eccentricity
    inclin_quant = Quantity(value=inclin, unit='deg')  # Inclination (degrees)
    omega_quant = Quantity(value=omega, unit='deg')  # Longitude of Ascending Node (degrees)
    w_quant = Quantity(value=w, unit='deg')  # Argument of Perigee (degrees)
    t_quant = Quantity(value=t, unit='deg')  # True anomaly (degrees)
    
    # Creating an Orbit object
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

    # Taking individual x, y, and z values from position vector 'r'
    x = lro_orbit.r[0] / u.km
    y = lro_orbit.r[1] / u.km
    z = lro_orbit.r[2] / u.km
    return [x, y, z]

# Function to convert from Cartesian coordinates (x, y, z) to geographic coordinates (long, lat)
# Input  - Cartesian coordinates
# Output - Array of latitude and longitude
def cart_to_spherical(x, y, z):
    r = math.sqrt(x*x + y*y + z*z) # Getting the magnitude of the position vector
    
    lat = math.acos(z / r) # Inverse cosine of the z-component divided by the magnitude
    # Piecewise function where the tangent of the longitude is equal to the y-component 
    # divded by the x-component
    if x > 0:
        long = math.atan(y / x)
    elif x < 0:
        long = math.atan(y / x) + math.pi
    else:
        long = math.pi / 2 

    lat = lat * (180 / math.pi)   # Converting to decimal degrees from radians
    long = long * (180 / math.pi) # Converting to decimal degrees from radians

    print("[Long, Lat]: "+str([long, lat]))
    return [lat, long, r]

# Function to compare two orbits' Cartesian coordinates to find a collision
# Input  - (x1, y1, z1) and (x2, y2, z2) to compare
# Output - Orbits have collided at true anomaly 't' (bool)
def compare(x1, y1, z1, x2, y2, z2):
    is_collision = False # Automatically assumes no collision
    
    # Rounding values to the nearest hundred to allow for more accurate collision detection
    rounded_x1 = round(x1, -2)
    rounded_y1 = round(y1, -2)
    rounded_z1 = round(z1, -2)
    
    rounded_x2 = round(x2, -2)
    rounded_y2 = round(y2, -2)
    rounded_z2 = round(z2, -2)

    # Comparing rounded coordinates
    if (rounded_x1, rounded_y1, rounded_z1) == (rounded_x2, rounded_y2, rounded_z2):
        is_collision = True

    return is_collision

# Function to plot the longitude and latitude of an orbit's groundtrack on a map
# Input  - (lat, long), color of orbit (identifier)
# Output - N/A
def plot_lat_long(lat, long, color):
    # Finding the pixel coordinates on the map
    map_w = float(canvas["width"])
    map_h = float(canvas["height"])
    x_p = (((map_w / 2)) + long * (map_w / map_h)) - 170
    y_p = (((map_h / 2)) + lat) - 50

    # Plotting the point
    canvas.create_oval(x_p, y_p, x_p, y_p, outline=color, width=5)

# ---------------UI CODE---------------
def incremenet():
    global t, a, e, inclin, omega, w, canvas, lat_long_stringvar_1, lat_long_stringvar_2
    while t1.is_alive():
        try:
            t += 0.1
            if t >= 360:
                break
            # time.sleep(1)
            t_string.set("True anomaly: "+str(t))
            root.update_idletasks()
            
            if float(t_string.get()) != 0:
                # Cartesian coordinates
                result = cartesian_from_elements(a, e, inclin, omega, w, t)
                x = float(result[0])
                y = float(result[1])
                z = float(result[2])

                result2 = cartesian_from_elements(a=a_2, e=e_2, inclin=inclin_2, omega=omega_2, w=w_2, t=t)
                x2 = float(result2[0])
                y2 = float(result2[1])
                z2 = float(result2[2])

                collide = compare(x, y, z, x2, y2, z2)  # To check if two orbits collide
                
                # Latitude and Longitude Coordinates
                lat_long = cart_to_spherical(x, y, z)
                lat = lat_long[0]
                long = lat_long[1]
                r = lat_long[2]

                lat_long_2 = cart_to_spherical(x2, y2, z2)
                lat2 = lat_long_2[0]
                long2 = lat_long_2[1]
                r2 = lat_long_2[2]
                with open('values.csv', 'a', newline='') as file:
                    fwriter = csv.writer(file)
                    fwriter.writerow([long2, lat2])

                lat_long_stringvar_1.set(f'Latitude: {lat}\nLongitude: {long}\nAltitude: {r}')
                lat_long_stringvar_2.set(f'Latitude: {lat2}\nLongitude: {long2}\nAltitude: {r2}')
                
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

label = Label(root, text="Orbit 1:")
label.pack()

# Entry for keplerian elements of orbit(s??)
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

label_2 = Label(root, text="Orbit 2:")
label_2.pack()

semimajor_entry_2 = Entry(root, width=25)
semimajor_entry_2.insert(0, "Semi-major axis (2)")
semimajor_entry_2.pack()

eccentricity_entry_2 = Entry(root, width=25)
eccentricity_entry_2.insert(0, "Eccentricity (2)")
eccentricity_entry_2.pack()

inclination_entry_2 = Entry(root, width=25)
inclination_entry_2.insert(0, "Inclination (2)")
inclination_entry_2.pack()

ascension_entry_2 = Entry(root, width=25)
ascension_entry_2.insert(0, "Right ascension of ascending node (2)")
ascension_entry_2.pack()

perigee_entry_2 = Entry(root, width=25)
perigee_entry_2.insert(0, "Argument of perigee (2)")
perigee_entry_2.pack()

# For spherical coordinate readouts
lat_long_stringvar_1 = StringVar(root, '')
lat_long_label_1 = Label(root, textvariable=lat_long_stringvar_1)
lat_long_label_1.pack(side=LEFT)

lat_long_stringvar_2 = StringVar(root, '')
lat_long_label_2 = Label(root, textvariable=lat_long_stringvar_2)
lat_long_label_2.pack(side=RIGHT)


def submit():
    global a, e, inclin, omega, w, t, t_string, a_2, e_2, inclin_2, omega_2, w_2
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

        a_2 = float(semimajor_entry_2.get())
        e_2 = float(eccentricity_entry_2.get())
        inclin_2 = float(inclination_entry_2.get())
        omega_2 = float(ascension_entry_2.get())
        w_2 = float(perigee_entry_2.get())
    except ValueError:
        # Program lets user know if element values are invalid. (i.e. not a float)
        messagebox.showerror(title="ERROR", message="INVALID INPUT FOR ENTRY")
        return

    frame = Frame(root, height=20, width=100)
    frame.pack()
    l1 = Label(frame, text="Semi-major axis: "+str(a))
    l1.pack()
    l2 = Label(frame, text="Eccentricity: "+str(e))
    l2.pack()
    l3 = Label(frame, text="Inclination: "+str(inclin))
    l3.pack()
    l3 = Label(frame, text="Right ascension of ascending node: " + str(omega))
    l3.pack()
    l4 = Label(frame, text="Argument of perigee: "+str(w))
    l4.pack()

    l5 = Label(frame, text="Semi-major axis (2): "+str(a_2))
    l5.pack()
    l6 = Label(frame, text="Eccentricity (2): "+str(e_2))
    l6.pack()
    l7 = Label(frame, text="Inclination (2): "+str(inclin_2))
    l7.pack()
    l8 = Label(frame, text="Right ascension of ascending node (2): " + str(omega_2))
    l8.pack()
    l9 = Label(frame, text="Argument of perigee (2): "+str(w_2))
    l9.pack()

    t1.start()
    # t2.start()
    l5 = Label(frame, textvariable=t_string).pack()

    semimajor_entry.pack_forget()
    eccentricity_entry.pack_forget()
    inclination_entry.pack_forget()
    ascension_entry.pack_forget()
    perigee_entry.pack_forget()
    button.pack_forget()

    semimajor_entry_2.pack_forget()
    eccentricity_entry_2.pack_forget()
    inclination_entry_2.pack_forget()
    ascension_entry_2.pack_forget()
    perigee_entry_2.pack_forget()
    label.pack_forget()
    label_2.pack_forget()


button = Button(root, text="Submit", command=submit)
button.pack()

root.mainloop()
