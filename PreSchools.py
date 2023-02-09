# from https://github.com/shakasom/voronoi/blob/master/Voronoi%20PreSchools.ipynb
# code for article  https://laptrinhx.com/how-to-create-voronoi-regions-with-geospatial-data-in-python-897661291/

import numpy as np
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from shapely.ops import cascaded_union
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from geovoronoi import voronoi_regions_from_coords, points_to_coords

# read data
gdf = gpd.read_file("data/preschools.shp")
print (gdf.head())

# read area data & plot area with locations
boundary = gpd.read_file("data/uppsala.shp")
fig, ax = plt.subplots(figsize=(12, 10))
boundary.plot(ax=ax, color="gray")
gdf.plot(ax=ax, markersize=3.5, color="black")
ax.axis("off")
plt.axis("equal")
plt.show()

# convert to Web Mercator projection
boundary = boundary.to_crs(epsg=3395)
gdf_proj = gdf.to_crs(boundary.crs)

# prepare the data to a format that Geovoronoi library can use
boundary_shape = cascaded_union(boundary.geometry)
coords = points_to_coords(gdf_proj.geometry)

# Calculate Voronoi Regions
# ERROR - wrong number of return values
# poly_shapes, pts, poly_to_pt_assignments = voronoi_regions_from_coords(coords, boundary_shape)
poly_shapes, pts = voronoi_regions_from_coords(coords, boundary_shape)
print ("generated " + str(len(poly_shapes)) + " polygons")

# plot
fig, ax = subplot_for_map()
plot_voronoi_polys_with_points_in_area(ax, boundary_shape, poly_shapes, pts)
ax.set_title('Voronoi regions of Schools in Uppsala')
plt.tight_layout()
plt.show()