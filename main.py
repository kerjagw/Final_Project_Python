import osmnx as ox
import geopandas as gpd

# Using a geocoder to get the extent
city = ox.geocoder.geocode_to_gdf('Wageningen, Netherlands')
ox.plot.plot_footprints(ox.project_gdf(city))

# Get all network and create graph
wageningenRoadsGraph = ox.graph.graph_from_place('Wageningen, Netherlands', network_type='all')

# Plot and save
ox.plot.plot_graph(wageningenRoadsGraph, figsize=(10, 10), node_size=2)
ox.io.save_graph_shapefile(G=wageningenRoadsGraph, filepath='data/OSMnetwork_Wageningen.shp')

# Metadata
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G=wageningenRoadsGraph)
print(gdf_nodes.info())
print(gdf_edges.info())

from shapely.wkt import loads

# Define a point
wktstring = 'POINT(173994.1578792833 444133.6032947102)'

# Convert to a GeoSeries
gs = gpd.GeoSeries([loads(wktstring)])

# Inspect the properties
print(type(gs), len(gs))

# Specify the projection
gs.crs = "EPSG:28992" 

# add a buffer of 5000 m (5km)
gs_buffer = gs.buffer(5000)

# Inspect the results
print(gs.geometry)
print(gs_buffer.geometry)

