import argparse
import sys

import matplotlib.pyplot as plt
# open geojson
import fiona

from shapely import MultiPolygon, Point, LineString
from shapely.geometry import shape, Polygon
from shapely.geometry.base import GeometrySequence
from shapely.ops import polygonize

from geovoronoi.plotting import subplot_for_map
from geovoronoi._voronoi import voronoi_regions_from_coords

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

def init_ArgsParser ():
    parser = argparse.ArgumentParser(
        prog='OSMConverter',
        description='This program reads locations & one border from a geoJson file, generate polygons and export them in VDM format',
        epilog='Autor: Edgar@haimerl.eu')
    parser.add_argument('filename', nargs=1, type=str,
                help="geoJson file to read; has locations with location=[OrtNr] and one MultiPolygon as border")  # positional argument - automatically required
    parser.add_argument('-i', '--imageExport', help="the polygons are exported as png file")
    parser.add_argument('-o', '--osmExport', help="the polygons are exported as a geoJson file")
    parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', help='Suppress Output' )
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Output' )
    return parser

# handle command line params
parser = init_ArgsParser()
args = parser.parse_args()

# read OSM file Dees locations
# !!!!!!!!!!!!!!! voronoi_region_from_coords did not work with gdf data format, only with Shapely (below)
#locations = gpd.read_file("Dees_loc.geojson")
geoFileData = fiona.open(args.filename[0])
# find locations (have properties.location != 'None') into shapes

# all features that have a locations properties entry
geoDataLoc =  [loc for loc in geoFileData if loc["properties"]["location"] != None]
# parallel list with location Numbers
geoDataLocNr = [locNr["properties"]["location"] for locNr in geoDataLoc]

# only use the one area that's called "clip area"
geoDataArea = [area for area in geoFileData if area["properties"]["type"] == 'multipolygon']

# convert to list of Shapely points
locations = [shape(loc["geometry"]) for loc in geoDataLoc]
# convert to list of shapely Mulipolyon - just one entry
borders = [shape(area["geometry"]) for area in geoDataArea]
# use the first border that has  area=clip area
if len(borders) != 1:
    print("could not find exactly ONE MuliPolygon in " + args.filename[0])
    exit(-1)
# use geovoronoi to create the polygons within the border
region_polys, region_pts = voronoi_regions_from_coords(locations, borders[0])
print ("generated " + str(len(region_polys)) + " polygons")

# plot
# plt.clf()
fig, ax = subplot_for_map()
plot_polys(region_polys)

if args.imageExport is not None:
    plt.savefig(args.imageExport[0])
plt.show()

# convert to VDM polygons

