from shapely import LineString, MultiPoint, normalize, Point, voronoi_polygons
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from shapely.plotting import plot_line, plot_points


# ===========================   examples for voronoi_polygons =======================
# https://shapely.readthedocs.io/en/stable/reference/shapely.voronoi_polygons.html
if 0:
    points = MultiPoint([(2, 2), (4, 2)])

    normalize(voronoi_polygons(points))
    # GEOMETRYCOLLECTION (POLYGON ((3 0, 3 4, 6 4, 6 0, 3 0)), POLYGON ((0 0, 0 4...>


    polygons1 = voronoi_polygons(points, only_edges=True)
    # <LINESTRING (3 4, 3 0)>

    polygons2 = voronoi_polygons(MultiPoint([(2, 2), (4, 2), (4.2, 2)]), 0.5, only_edges=True)
    # <LINESTRING (3 4.2, 3 -0.2)>

    polygons3 = voronoi_polygons(points, extend_to=LineString([(0, 0), (10, 10)]), only_edges=True)
    # <LINESTRING (3 10, 3 0)>

    polygons4 = voronoi_polygons(LineString([(2, 2), (4, 2)]), only_edges=True)
    # <LINESTRING (3 4, 3 0)>

    polygons6 = voronoi_polygons(Point(2, 2))
    # <GEOMETRYCOLLECTION EMPTY>


# ================================= lines & plotting
#from https://shapely.readthedocs.io/en/stable/manual.html#linestrings
if 1:
    SIZE = (8,8)
    BLUE = 'b'
    BLACK = '0'
    GRAY = '0.7'
    YELLOW = "y"

    fig = plt.figure(1, figsize=SIZE, dpi=90)

    # 1: simple line
    ax = fig.add_subplot(121)
    line = LineString([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])

    plot_line(line, ax=ax, add_points=False, color=BLUE, alpha=0.7)
    plot_points(line, ax=ax, color=GRAY, alpha=0.7)
    plot_points(line.boundary, ax=ax, color=BLACK)

    ax.set_title('a) simple')

    # set_limits(ax, -1, 4, -1, 3)

    # 2: complex line
    ax = fig.add_subplot(122)
    line2 = LineString([(0, 0), (1, 1), (0, 2), (2, 2), (-1, 1), (1, 0)])

    plot_line(line2, ax=ax, add_points=False, color=YELLOW, alpha=0.7)
    plot_points(line2, ax=ax, color=GRAY, alpha=0.7)
    plot_points(line2.boundary, ax=ax, color=BLACK)

    ax.set_title('b) complex')

#    set_limits(ax, -2, 3, -1, 3)

    plt.show()