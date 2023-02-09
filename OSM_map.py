# my test to read OSM map with locations and boarder
import geopandas as gpd
import matplotlib.pyplot as plt

# read OSM file Dees locations
gdf_locations = gpd.read_file("Dees_loc.geojson")
# gdf_locations.sample(10)
# print(gdf_locations['OrtNr'])
fig, ax = plt.subplots(figsize=(12, 10))
gdf_locations.plot(ax=ax, color='gray')
gdf_locations.plot(ax=ax, markersize=2.5, color='black')
ax.axis('off')
plt.axis('equal')
plt.show() # The output is a map showing locations in DEES.

# read borders from OSM file - but this is not a polygon but single points??