# from https://www.daniweb.com/programming/computer-science/tutorials/520314/how-to-make-quality-voronoi-diagrams
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import colorized_voronoi as colorVor

# Calculate Voronoi Polygons
square = [(0, 0), (0, 1), (1, 1), (1, 0)]
vor = Voronoi(square)


# generates a simple polygon - square with four seeds
def simple_voronoi(vor, saveas=None, lim=None):
    # Make Voronoi Diagram
    fig = voronoi_plot_2d(vor, show_points=True, show_vertices=True, s=4)

    # Configure figure
    fig.set_size_inches(5, 5)
    plt.axis("equal")

    if lim:
        plt.xlim(*lim)
        plt.ylim(*lim)

    if not saveas is None:
        plt.savefig("%s.png" % saveas)

    plt.show()


# simple_voronoi(vor, saveas="square", lim=(-0.25, 1.25))

