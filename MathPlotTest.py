import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

if 0:
       x = np.linspace(0, 2 * np.pi, 200)
       y = np.sin(x)

       fig, ax = plt.subplots()
       ax.plot(x, y)
       plt.show()


       # from https://matplotlib.org/stable/plot_types/3D/surface3d_simple.html#sphx-glr-plot-types-3d-surface3d-simple-py
       plt.style.use('_mpl-gallery')

       # Make data
       X = np.arange(-5, 5, 0.25)
       Y = np.arange(-5, 5, 0.25)
       X, Y = np.meshgrid(X, Y)
       R = np.sqrt(X**2 + Y**2)
       Z = np.sin(R)

       # Plot the surface
       fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
       ax.plot_surface(X, Y, Z, vmin=Z.min() * 2, cmap=cm.Blues)

       ax.set(xticklabels=[],
              yticklabels=[],
              zticklabels=[])
       plt.show()

if 1:
       # from https://matplotlib.org/stable/tutorials/introductory/quick_start.html#sphx-glr-tutorials-introductory-quick-start-py
       x = np.linspace(0, 2, 100)  # Sample data.

       # Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
       fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
       ax.plot(x, x, label='linear')  # Plot some data on the axes.
       ax.plot(x, x**2, label='quadratic')  # Plot more data on the axes...
       ax.plot(x, x**3, label='cubic')  # ... and some more.
       ax.set_xlabel('x label')  # Add an x-label to the axes.
       ax.set_ylabel('y label')  # Add a y-label to the axes.
       ax.set_title("Simple Plot")  # Add a title to the axes.
       ax.legend();  # Add a legend.
       plt.show()