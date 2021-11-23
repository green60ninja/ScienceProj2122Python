from astropy.units.quantity import Quantity
from poliastro.bodies import Moon
from poliastro.constants.general import J2000
from poliastro.plotting.static import StaticOrbitPlotter
from poliastro.twobody.orbit import Orbit
import matplotlib.pyplot as plt

def plot_lro_orbit():
    lro = Orbit.from_classical(
        attractor=Moon,
        a=Quantity(value=2011.343, unit='km'),
        ecc=Quantity(value=0.635485),
        inc=Quantity(value=90.016, unit='deg'),
        raan=Quantity(value=88.74, unit='deg'),
        argp=Quantity(value=336.655, unit='deg'),
        nu=Quantity(value=0, unit='deg')
    )
    
    frame = StaticOrbitPlotter()
    # frame.plot_body_orbit(Moon, J2000)
    frame.plot(lro, label='LRO')
    plt.show()