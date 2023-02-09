# from https://towardsdatascience.com/how-to-create-voronoi-regions-with-geospatial-data-in-python-adbb6c5f2134
import numpy as np
import geopandas as gpd
# import contextily as ctx
import matplotlib.pyplot as plt


from shapely.ops import cascaded_union
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from geovoronoi import voronoi_regions_from_coords, points_to_coords

gdf = gpd.read_file("data/preschools.shp")
gdf.head()

# plot the points data. Just to give some context,
# we also read the boundary of the county and plot the points on top of it.
boundary = gpd.read_file('data/uppsala.shp')
fig, ax = plt.subplots(figsize=(12, 10))
boundary.plot(ax=ax, color='gray')
gdf.plot(ax=ax, markersize=3.5, color='black')
ax.axis('off')
plt.axis('equal')
plt.show() # The output is a map showing all preschools (black dots) in Uppsala county, Sweden.

# Mercator projection
boundary = boundary.to_crs(epsg=3395)
gdf_proj = gdf.to_crs(boundary.crs)

# convert the boundary geometry into a union of the polygon.
# convert the Geopandas GeoSeries of Point objects to NumPy array of coordinates.
boundary_shape = cascaded_union(boundary.geometry)
coords = points_to_coords(gdf_proj.geometry)

# Calculate Voronoi Regions, The output holds the shapes,
# the points and identification link between the two.
poly_shapes, pts, poly_to_pt_assignments = \
    voronoi_regions_from_coords(coords, boundary_shape, return_unassigned_points=True)

fig, ax = subplot_for_map()
plot_voronoi_polys_with_points_in_area(ax, boundary_shape, poly_shapes, pts, poly_to_pt_assignments)
ax.set_title('Voronoi regions of Schools in Uppsala')
plt.tight_layout()
plt.show()