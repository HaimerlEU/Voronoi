# https://www.daniweb.com/programming/computer-science/tutorials/520314/how-to-make-quality-voronoi-diagrams
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import numpy as np


# plot the voronoi and save as png
def simple_voronoi(p_vor, saveas=None, lim=None):
    # Make Voronoi Diagram
    fig = voronoi_plot_2d(p_vor, show_points=True, show_vertices=True, s=4)

    # Configure figure
    fig.set_size_inches(5, 5)
    plt.axis("equal")

    if lim:
        plt.xlim(*lim)
        plt.ylim(*lim)

    if not saveas is None:
        plt.savefig("%s.png"%saveas)
    plt.show()

# Calculate Voronoi Polygons
square = [(0, 0), (0, 1), (1, 1), (1, 0)]
vor = Voronoi(square)
simple_voronoi(vor, lim=(-0.25,1.25))

# use random seeds
#n_randoms = 5
#for i in range(4):
#    randos = five + np.random.rand(n_randoms, 2).tolist()
#    vor = Voronoi(randos)
#    simple_voronoi(vor, lim=(-1.5,2.5), saveas="rand%s"%i)