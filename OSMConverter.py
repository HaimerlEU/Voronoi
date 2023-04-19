import argparse

import matplotlib.pyplot as plt
import geopandas
import pandas
import scipy
import descartes
from shapely import MultiPolygon
from shapely.geometry import Polygon
from shapely.geometry.base import GeometrySequence

from geovoronoi.plotting import subplot_for_map
from geovoronoi._voronoi import voronoi_regions_from_coords


# draw a line between the coords - used in plot_polys
def plot_coords(coords):
    pts = list(coords)
    x, y = zip(*pts)
    plt.plot(x, y)


# plot array of polygons or MultiPolygone array is in geoms
def plot_polys(polys):
    print("plot_polys draws obj of type " + str(type(polys)))

    if type(polys) == MultiPolygon:
        for poly in polys.geoms:
            if not getattr(poly, "exterior", None):
                print("no attr exterior in " + str(type(poly)))
            else:
                plot_coords(poly.exterior.coords)

            for hole in poly.interiors:
                plot_coords(hole.coords)

    elif type(polys) == Polygon:
        plot_coords(polys.exterior.coords)

    elif type(polys) == list:
        for poly in polys:
            if not getattr(poly, "exterior", None):
                print("no attr exterior in " + str(type(poly)))
            else:
                plot_coords(poly.exterior.coords)

            for hole in poly.interiors:
                plot_coords(hole.coords)
    elif type(polys) == GeometrySequence:
        for poly in polys:
            if not getattr(poly, "exterior", None):
                print("no attr exterior in " + str(type(poly)))
            else:
                plot_coords(poly.exterior.coords)

            for hole in poly.interiors:
                plot_coords(hole.coords)

    elif type(polys) == dict:
        for poly in polys.values():
            if type(poly) == Polygon:
                plot_coords(poly.exterior.coords)
            else:
                print("ERROR: cannot plot dict element " + str(type(poly)))
    else:
        print("ERROR: cannot plot type " + str(type(polys)))


# set up the Argument Parser
def init_ArgsParser():
    newParser = argparse.ArgumentParser(
        prog='OSMConverter',
        description='This program reads locations & one border from a geoJson file, generate polygons and export them in VDM format',
        epilog='Autor: Edgar@haimerl.eu')
    newParser.add_argument('filename', nargs=1, type=str,
                help="geoJson file to read; has locations with location=[OrtNr] and one MultiPolygon as border")  # positional argument - automatically required
    newParser.add_argument('-c', '--crs',
                help="Projection code; outputs file [osmExport]_[crs].geojson with his projection")
    newParser.add_argument('-i', '--imageExport',
                help="the polygons are exported as png file")
    newParser.add_argument('-o', '--osmExport',
                help="the polygons are exported as a geoJson file in projection of input file")
    newParser.add_argument('-s', '--show',
                help="if show is defined the is a polygon preview in an extra viewer window - close the window to continue in the program")
    return newParser


# ================  this is where the main program begins ==========================
# handle command line params
parser = init_ArgsParser()
args = parser.parse_args()

# read OSM file, contains locations (points) and ONE area = bounding area
geoFileData = geopandas.read_file(args.filename[0])
crsOri = geoFileData.crs

# geoFileData = gdf.from_features(gdf, crs=2154)
print("read file " + args.filename[0] + "; has Projection " + str(geoFileData.crs))

# select all features that are points
locations =  [loc for loc in geoFileData['geometry'] if loc.geom_type == "Point"]
# create a parallel list with location Numbers
geoDataLocNr = [locNr for locNr in geoFileData['location'] if locNr is not None]
# looking for bounding area - select all MultiPolygons (should be only one - later only use the 1st)
borders = [area for area in geoFileData['geometry'] if area.geom_type == "MultiPolygon"]
if len(borders) != 1:
    print("could not find exactly ONE MuliPolygon in " + args.filename[0])
    exit(-1)

# use geovoronoi to create the polygons within the border
region_polys, region_pts = voronoi_regions_from_coords(locations, borders[0])
print ("generated " + str(len(region_polys)) + " polygons")

# ========================
# plot the polygons (but here without the right projection - just for basic
# ============================
if args.show is not None:
    fig, ax = subplot_for_map()
    plot_polys(region_polys)
    plt.show()

# ===============  export as image =================================
if args.imageExport is not None:
    plt.savefig(args.imageExport[0])

# ================  convert to GeoDataFrame  ===========================

# create dict with OrtNr - Polygon
DictPoly = dict()
pos = 0
for regPoint in region_pts:
    DictPoly[geoDataLocNr[regPoint]] = { 'geometry': {'type': 'Polygon', 'coordinates' : region_polys[pos]} ,
                                         'properties': {'OrtNr': geoDataLocNr[regPoint]}
                                        }
    pos += 1

# manually create dataFrame (for tests see readWriteGeoJson.py
df = pandas.DataFrame({'name' : '0' , 'Polygon' : []})
# list of order of the polygons relative to input: 0=43 means that point at GeoDataFile position 43 is the first polygon etc.
regionOrder = [pos[0] for pos in region_pts.values()]
df['name'] = [geoDataLocNr[pos] for pos in regionOrder]
df['Polygon'] = region_polys

# this adds colum geometry to the df -> makes it a geoDataFrame
gdf = geopandas.GeoDataFrame(df, geometry='Polygon')
gdf.crs = crsOri

# =========== plot polygons - no reprojection
if args.show is not None:
    gdf.plot()
    print(gdf.head())

# export in original projection
if args.osmExport is not None:
    gdf.to_file(args.osmExport, driver='GeoJSON')

# reprojection to crs
if args.crs is not None:
    fileName = args.osmExport[0: args.osmExport.find(".")] + "_" + args.crs + args.osmExport[args.osmExport.find('.'): len(args.osmExport)]
    gdfMercator = gdf.to_crs(int(args.crs))
    # transformation looses properties, copy transformed polygons to df from above
    df['Polygon'] = gdfMercator.affine_transform([1, 0, 0, -1, 0, 10000000])
    # transformation looses properties
    gdf = geopandas.GeoDataFrame(df, geometry='Polygon')
    gdf.to_file(fileName, driver='GeoJSON')

if args.show is not None:
    gdf.plot()
    print(gdf.head())
