import argparse

import matplotlib.pyplot as plt
# read geojson
import fiona
from fiona.crs import from_epsg

# write geoJson
import geopandas
from geopandas import GeoDataFrame
import pandas
import shapely
from shapely import MultiPolygon
from shapely.geometry import shape, Polygon
from shapely.geometry.base import GeometrySequence

from geovoronoi.plotting import subplot_for_map
from geovoronoi._voronoi import voronoi_regions_from_coords

# draw a line between the coords - used in plot_polys
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

# set up the Argument Parser
def init_ArgsParser ():
    parser = argparse.ArgumentParser(
        prog='OSMConverter',
        description='This program reads locations & one border from a geoJson file, generate polygons and export them in VDM format',
        epilog='Autor: Edgar@haimerl.eu')
    parser.add_argument('filename', nargs=1, type=str,
                help="geoJson file to read; has locations with location=[OrtNr] and one MultiPolygon as border")  # positional argument - automatically required
    parser.add_argument('-i', '--imageExport', help="the polygons are exported as png file")
    parser.add_argument('-o', '--osmExport', help="the polygons are exported as a geoJson file")
    parser.add_argument('-s', '--show', help="show the polygons in an extra viewer Window - close the window to continue in the program")
    parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', help='Suppress Output' )
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Output' )
    return parser

def df_to_geodf(df, geom_col="geom", crs=None, wkt=True):
  """
  Transforms a pandas DataFrame into a GeoDataFrame.
  The column 'geom_col' must be a geometry column in WKB representation.
  To be used to convert df based on pd.read_sql to gdf.
  Parameters
  from https://gis.stackexchange.com/questions/174159/converting-pandas-dataframe-to-geodataframe
  ----------
  df : DataFrame
      pandas DataFrame with geometry column in WKB representation.
  geom_col : string, default 'geom'
      column name to convert to shapely geometries
  crs : pyproj.CRS, optional
      CRS to use for the returned GeoDataFrame. The value can be anything accepted
      by :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
      such as an authority string (eg "EPSG:4326") or a WKT string.
      If not set, tries to determine CRS from the SRID associated with the
      first geometry in the database, and assigns that to all geometries.
  Returns
  -------
  GeoDataFrame
  """

  if geom_col not in df:
    raise ValueError("Query missing geometry column '{}'".format(geom_col))

  geoms = df[geom_col].dropna()

  if not geoms.empty:
    if wkt == True:
      load_geom = shapely.wkt.loads
    else:
      load_geom_bytes = shapely.wkb.loads
      """Load from Python 3 binary."""

      def load_geom_buffer(x):
        """Load from Python 2 binary."""
        return shapely.wkb.loads(str(x))

      def load_geom_text(x):
        """Load from binary encoded as text."""
        return shapely.wkb.loads(str(x), hex=True)

      if isinstance(geoms.iat[0], bytes):
        load_geom = load_geom_bytes
      else:
        load_geom = load_geom_text

    df[geom_col] = geoms = geoms.apply(load_geom)
    if crs is None:
      srid = shapely.geos.lgeos.GEOSGetSRID(geoms.iat[0]._geom)
      # if no defined SRID in geodatabase, returns SRID of 0
      if srid != 0:
        crs = "epsg:{}".format(srid)

  return GeoDataFrame(df, crs=crs, geometry=geom_col)



# ================  this is where the main program begins ==========================
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
if args.show is not None:
    plt.show()

# export as image
if args.imageExport is not None:
    plt.savefig(args.imageExport[0])

# save polygons as geoJson file
if args.osmExport is not None:
    # create dict with OrtNr - Polygon
    DictPoly = dict()
    pos = 0
    for regPoint in region_pts:
        DictPoly[geoDataLocNr[regPoint]] = { 'geometry': {'type': 'Polygon', 'coordinates' : region_polys[pos]} ,
                                             'properties': {'OrtNr': geoDataLocNr[regPoint]}
                                            }
        pos += 1
# save as geoJson ===========  many tests and no success

if 0:
    # try with GeoDataFrame.to_file
    import pandas as pd
    import geopandas
    #    d = {'col1': ['name1', 'name2'], 'wkt': ['POINT (1 2)', 'POINT (2 1)']}
    df = pd.DataFrame(list(region_polys.values()))
    gs = geopandas.GeoSeries.from_wkt(df['coordinates'])
    gdf = geopandas.GeoDataFrame(df, geometry=gs, crs="EPSG:2154")

    #df_output = pd.DataFrame(data = region_polys.values())
    # output = GeoDataFrame(region_polys.values())
    # output.set_geometry(col='geometry', inplace=True)
    # Input must be valid geometry objects: {'type': 'Polygon', 'coordinates': <POLYGON ((-0.743 48.777, -1.333 47.699, -2.342 47.599, -2.225 48.61, -1.464...>}
    gdf.to_file(args.osmExport, driver='GeoJSON', mode='w')

if 0:
    # try direct with fiona
    schema = {'geometry': 'Polygon', 'properties': {'OrtNr':'str'}}
    france_crs = from_epsg(2154)
    with fiona.open(args.osmExport, 'w', driver="GeoJSON", crs = france_crs, schema= schema) as dst:
        for poly in DictPoly.values():
            dst.write ([poly])

if 0:
    #try with geojson
    import json
    geojson = {"type": "FeatureCollection",  "features": []}
    for f in DictPoly.values():
        geojson["features"].append(f)
    with open(args.osmExport, "w") as gjs:
        json.dump(geojson, gjs)

# manualy create dataFrame (for tests see readWriteGeoJson.py
df = pandas.DataFrame({'OrtNr' : '0' , 'Polygon' : []})
# list of order of the polygons relative to input: 0=43 means that point at GeoDataFile position 43 is the first polygon etc.
regionOrder = [pos[0] for pos in region_pts.values()]
df['OrtNr'] = [geoDataLocNr[pos] for pos in regionOrder]
df['Polygon'] = region_polys

# this adds colum geometry to the df -> makes it a geoDataFrame
gdf = geopandas.GeoDataFrame(df, geometry='Polygon')
print(gdf.head())
gdf.to_file(args.osmExport, driver='GeoJSON')

# convert to VDM polygons
