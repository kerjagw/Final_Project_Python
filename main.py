import osmnx as ox
import geopandas as gpd
from shapely.wkt import loads


#1 Using a geocoder to get the extent
city = ox.geocoder.geocode_to_gdf('Wageningen, Netherlands')
ox.plot.plot_footprints(ox.project_gdf(city))

#Store Area Of Interest
AOI = ox.geocode_to_gdf('Wageningen, Netherlands',buffer_dist=5000)

# Get all network and create graph
wageningenRoadsGraph = ox.graph.graph_from_place('Wageningen, Netherlands', network_type='all')

# Plot and save
ox.plot.plot_graph(wageningenRoadsGraph, figsize=(10, 10), node_size=2)
ox.io.save_graph_shapefile(G=wageningenRoadsGraph, filepath='data/OSMnetwork_Wageningen.shp')

# Metadata
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G=wageningenRoadsGraph)
print(gdf_nodes.info())
print(gdf_edges.info())

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

#2 Get District
from owslib.wfs import WebFeatureService

# Put the WFS url in a variable
wfsUrl = 'https://geodata.nationaalgeoregister.nl/nwbwegen/wfs?'

# Create a WFS object
wfs = WebFeatureService(url=wfsUrl, version='2.0.0')

# Get the title from the object
print(wfs.identification.title)

# Check the contents of the WFS
print(list(wfs.contents))

#3 Filter Overlap
import matplotlib as plt

# Define center point and create bbox for study area
x, y = (173994.1578792833, 444133.60329471016)
xmin, xmax, ymin, ymax = x - 1000, x + 350, y - 1000, y + 350

# Get the features for the study area (using the wfs from the previous code block)
response = wfs.getfeature(typename=list(wfs.contents)[0], bbox=(xmin, ymin, xmax, ymax))

# Save them to disk
with open('data/Roads.gml', 'wb') as file:
    file.write(response.read())

# Read in again with GeoPandas
roadsGDF = gpd.read_file('data/Roads.gml')

# Create a WFS object
wfs = WebFeatureService(url=wfsUrl, version='2.0.0')

# Let's create a bit bigger bounding box for this example than last time
x, y = (173994.1578792833, 444133.60329471016)
xmin, xmax, ymin, ymax = x - 3000, x + 3000, y - 3000, y + 3000

# Get the features for the study area
response = wfs.getfeature(typename=list(wfs.contents)[0], bbox=(xmin, ymin, xmax, ymax))
roadsGDF = gpd.read_file(response)

# Select the roads within Wageningen municipality
wageningenRoadsGDF = roadsGDF.loc[roadsGDF['gme_naam'] == 'Wageningen']

# Plot
wageningenRoadsGDF.plot(edgecolor='purple')

import json

# Get the WFS of the BAG
wfsUrl = 'https://service.pdok.nl/lv/bag/wfs/v2_0'
wfs = WebFeatureService(url=wfsUrl, version='2.0.0')
layer = list(wfs.contents)[0]

# Define center point and create bbox for study area
x, y = (173994.1578792833, 444133.60329471016)
xmin, xmax, ymin, ymax = x - 500, x + 500, y - 500, y + 500

# Get the features for the study area
# notice that we now get them as json, in contrast to before
response = wfs.getfeature(typename=layer, bbox=(xmin, ymin, xmax, ymax), outputFormat='json')
data = json.loads(response.read())

# Create GeoDataFrame, without saving first
buildingsGDF = gpd.GeoDataFrame.from_features(data['features'])

# Set crs to RD New
buildingsGDF.crs = 28992

# Plot roads and buildings together
roadlayer = roadsGDF.plot(color='grey')
buildingsGDF.plot(ax=roadlayer, color='red')

# Set the limits of the x and y axis
roadlayer.set_xlim(xmin, xmax)
roadlayer.set_ylim(ymin, ymax)

# Save the figure to disk
plt.savefig('./output/BuildingsAndRoads.png')


# Define center point and create bbox for study area
x, y = (173994.1578792833, 444133.60329471016)
xmin, xmax, ymin, ymax = x - 1000, x + 350, y - 1000, y + 350

# Get the features for the study area (using the wfs from the previous code block)
response = wfs.getfeature(typename=list(wfs.contents)[0], bbox=(xmin, ymin, xmax, ymax))

# Save them to disk
with open('data/Roads.gml', 'wb') as file:
    file.write(response.read())

# Read in again with GeoPandas
roadsGDF = gpd.read_file('data/Roads.gml')

# Inspect and plot to get a quick view
print(type(roadsGDF))
roadsGDF.plot()
plt.show()

print(type(roadsGDF))
print(type(roadsGDF.geometry))
print(roadsGDF['geometry'])

# Buffer of 1.5 m on both sides
roadsPolygonGDF = gpd.GeoDataFrame(roadsGDF, geometry=roadsGDF.buffer(distance=1.5)) 

# Plot
roadsPolygonGDF.plot(color='blue', edgecolor='blue')

# Check the total coverage of buffers
print(roadsPolygonGDF.area.sum())


import folium

# Initialize the map
campusMap = folium.Map([51.98527485, 5.66370505205543], zoom_start=17)

# Re-project
buildingsGDF = buildingsGDF.to_crs(4326)
roadsPolygonGDF = roadsPolygonGDF.to_crs(4326)

# Add the buildings
folium.Choropleth(buildingsGDF, name='Building construction years',
                  data=buildingsGDF, columns=['identificatie', 'bouwjaar'],
                  key_on='feature.properties.identificatie', fill_color='RdYlGn',
                  fill_opacity=0.7, line_opacity=0.2,
                  legend_name='Construction year').add_to(campusMap)

# Add the roads
folium.GeoJson(roadsPolygonGDF).add_to(campusMap)

# Add layer control
folium.LayerControl().add_to(campusMap)

# Save (you can now open the generated .html file from the output directory)
campusMap.save('output/CandidateDistrictForVeronica.html')