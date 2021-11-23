from astropy.units.quantity import Quantity
from poliastro.bodies import Moon
from poliastro.constants.general import J2000
from poliastro.frames.enums import Planes
from poliastro.plotting.static import StaticOrbitPlotter
from poliastro.twobody.orbit import Orbit
import matplotlib.pyplot as plt

def plot_lro_orbit():
    lro = Orbit.from_classical(
        attractor=Moon,
        a=Quantity(value=1795.224, unit='km'),
        ecc=Quantity(value=0.019296),
        inc=Quantity(value=85.780, unit='deg'),
        raan=Quantity(value=128.208, unit='deg'),
        argp=Quantity(value=246.531, unit='deg'),
        nu=Quantity(value=0, unit='deg'),
        plane=Planes.BODY_FIXED,
        epoch=J2000
    )

    plotter = StaticOrbitPlotter(plane=Planes.BODY_FIXED)
    plotter.plot(lro, label='LRO')
    plt.show()

if __name__ == "__main__":
    plot_lro_orbit()