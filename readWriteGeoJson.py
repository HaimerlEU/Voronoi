# set up the Argument Parser
import argparse


def init_ArgsParser ():
    parser = argparse.ArgumentParser(
        prog='readWriteGeoJson',
        description='This are tests to read from a geoJson file into a geoDataFrame and write this back to file',
        epilog='Autor: Edgar@haimerl.eu')
    parser.add_argument('inFilename', nargs=1, type=str,
                help="geoJson file to read; has locations with location=[OrtNr] and one MultiPolygon as border")
    parser.add_argument('outFilename', nargs=1, type=str,
                        help='create and write to this file')
    return parser

parser = init_ArgsParser()
args = parser.parse_args()

# very simple write geoJson with 2 points
if 0:
    data = {'geometry': [g.Point(0, 0), g.Point(1,1)],
        'OrtNr': ['1', '2']
    }
    df = geopandas.GeoDataFrame(data)
    df.to_file(args.outFilename[0], driver='GeoJSON')

# https://geopandas.org/en/latest/gallery/create_geopandas_from_pandas.html
if 0:
    import pandas
    import geopandas

    df = pandas.DataFrame(
        {
            "City": ["Buenos Aires", "Brasilia", "Santiago", "Bogota", "Caracas"],
            "Country": ["Argentina", "Brazil", "Chile", "Colombia", "Venezuela"],
            "Latitude": [-34.58, -15.78, -33.45, 4.60, 10.48],
            "Longitude": [-58.66, -47.91, -70.66, -74.08, -66.86],
        }
    )

    gdf = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude)
    )
    print(gdf.head())
    gdf.to_file(args.outFilename[0], driver='GeoJSON')


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

# read from geojson
if 1:
    import fiona
    import pandas
    import geopandas

    geoFileData = fiona.open(args.inFilename[0])
    print("read from {0} {1} features".format(args.inFilename, len(geoFileData)))

    # all features that have a locations properties entry
    geoDataLoc = [loc for loc in geoFileData if loc["properties"]["location"] != None]
    # parallel list with location Numbers
    geoDataLocNr = [locNr["properties"]["location"] for locNr in geoDataLoc]

    # manualy create dataFrame
    df = pandas.DataFrame()
    df['OrtNr'] = geoDataLocNr
    df['coord'] = [geo["geometry"]["coordinates"] for geo in geoDataLoc]
    xCoords = [x[0] for x in  df.coord.array ]
    yCoords = [y[1] for y in df.coord.array ]
    gdf = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(xCoords, yCoords)
    )
    print(gdf.head())
    gdf.to_file(args.outFilename[0], driver='GeoJSON')
    '''
    FAILS 
    Traceback (most recent call last):
  File "C:\Users\Edgar\PycharmProjects\Voronoi\venv\lib\site-packages\geopandas\io\file.py", line 575, in _to_file_fiona
    colxn.writerecords(df.iterfeatures())
  File "C:\Users\Edgar\PycharmProjects\Voronoi\venv\lib\site-packages\fiona\collection.py", line 361, in writerecords
    self.session.writerecs(records, self)
  File "fiona\ogrext.pyx", line 1291, in fiona.ogrext.WritingSession.writerecs
  File "fiona\ogrext.pyx", line 466, in fiona.ogrext.OGRFeatureBuilder.build
ValueError: Invalid field type <class 'tuple'>
    '''