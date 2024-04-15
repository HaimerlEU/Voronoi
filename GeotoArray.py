import pandas as pd
import geopandas    
# for map display gfd.explore
import matplotlib
# import mapclassify
# import folium

# from https://geopandas.org/en/stable/gallery/create_geopandas_from_pandas.html
df = pd.DataFrame(
    {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
     'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
     'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
     'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})

# We use geopandas points_from_xy() to transform Longitude and Latitude into a list of shapely.Point o
gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))
print(gdf.head())

# https://geopandas.org/en/stable/getting_started/introduction.html
# This tutorial uses the "nybb" dataset, a map of New York boroughs,
# which is part of the GeoPandas installation.
path_to_data = geopandas.datasets.get_path("nybb")
gdf = geopandas.read_file(path_to_data)
print(gdf.head())
# to make the results easier to read, set the names of the boroughs as the index:
gdf = gdf.set_index("BoroName")
gdf["area"] = gdf.area
print(gdf["area"])

# To get the boundary of each polygon (LineString), access the GeoDataFrame.boundary
gdf['boundary'] = gdf.boundary
print(gdf['boundary'])

# create new geometrie, e.g. centroids - all that is ADDED to the GeoDataFrame as new fields
gdf['centroid'] = gdf.centroid
print(gdf['centroid'])

# add distance to first location
first_point = gdf['centroid'].iloc[0]
gdf['distance'] = gdf['centroid'].distance(first_point)
print(gdf['distance'])

# show map
matplotlib.use('svg', force=True)
gdf.plot("area", legend=True)
# interactive version - enter at prompt in console?
# don't see anything on Ubuntu???
# gdf.explore("area", legend=False)

gdf = gdf.set_geometry("centroid")

df = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
df.head(2)
print("were is the map?")
