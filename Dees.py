# https://pypi.org/project/geovoronoi/

import fiona
from shapely import MultiPolygon
from shapely.geometry import shape, Polygon
from shapely.geometry.base import GeometrySequence
from shapely.ops import polygonize

from geovoronoi.plotting import plot_voronoi_polys_with_points_in_area
from geovoronoi.plotting import subplot_for_map
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
import numpy as np

import geopandas as gpd
# don't use geovoronoi (not maintained) - use shapely instead
from geovoronoi import voronoi_regions_from_coords
# from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area



def plot_coords(coords):
    pts = list(coords)
    x,y = zip(*pts)
    plt.plot(x,y)

# plot array of polygons or MultiPolygone array is in geoms
def plot_polys(polys):
    print ("plot_polys draws obj of type " + str(type(polys)))

    if type(polys) == MultiPolygon:
        for poly in polys.geoms:
            if (not getattr(poly, "exterior", None)):
                print("no attr exterior in " + str(type(poly)))
            else:
                plot_coords(poly.exterior.coords)

            for hole in poly.interiors:
                plot_coords(hole.coords)

    elif type(polys) == Polygon:
        plot_coords(polys.exterior.coords)

    elif type(polys) == list:
        for poly in polys:
            if (not getattr(poly, "exterior", None)):
                print("no attr exterior in " + str(type(poly)))
            else:
                plot_coords(poly.exterior.coords)

            for hole in poly.interiors:
                plot_coords(hole.coords)
    elif type(polys) == GeometrySequence:
        for poly in polys:
            if (not getattr(poly, "exterior", None)):
                print("no attr exterior in " + str(type(poly)))
            else:
                plot_coords(poly.exterior.coords)

            for hole in poly.interiors:
                plot_coords(hole.coords)

    elif type(polys) == dict:
        for  poly in polys.values():
            if type(poly) == Polygon:
                plot_coords(poly.exterior.coords)
            else:
                print ("ERROR: cannot plot dict element " + str(type(poly)))
    else:
        print ("ERROR: cannot plot type " + str(type(polys)))


# read OSM file Dees locations
# !!!!!!!!!!!!!!! voronoi_region_from_coords did not work with gdf data format, only with Shapely (below)
#locations = gpd.read_file("Dees_loc.geojson")

# read Dees points as shapely list of points
path = 'Dees_loc.geojson'
points = fiona.open(path)
#convert in shapes
DeesPoints = [ shape(feat["geometry"]) for feat in points ]

# make sure the way is defined as a multipolygon in JOSM
path = 'Dees_bounds.geojson'
bounds = fiona.open(path)
# why does it only work when I create it as list with one entry, not as Multipolygon directly
DeesBounds =  [ shape(bound["geometry"]) for bound in bounds ]
region_polys, region_pts = voronoi_regions_from_coords(DeesPoints, DeesBounds[0])
print ("generated " + str(len(region_polys)) + " polygons")

# plot
plt.clf()
fig, ax = subplot_for_map()
plot_polys(polygonize(DeesBounds))
plot_polys(region_polys)
plt.show()

