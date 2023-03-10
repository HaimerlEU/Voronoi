import geopandas

# load example data
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

# Check original projection
# (it's Plate Carrée! x-y are long and lat)
print(world.crs)

# Visualize
ax = world.plot()

ax.set_title("WGS84 (lat/lon)");

# Reproject to Mercator (after dropping Antartica)
world = world[(world.name != "Antarctica") & (world.name != "Fr. S. Antarctic Lands")]

world = world.to_crs("EPSG:3395") # world.to_crs(epsg=3395) would also work

ax = world.plot()

ax.set_title("Mercator");