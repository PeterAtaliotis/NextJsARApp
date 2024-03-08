import json
from pyproj import Transformer, CRS

# Define the transformer - Irish Grid to WGS84
transformer = Transformer.from_crs(CRS('epsg:29902'), CRS('epsg:4326'), always_xy=True)

# Function to convert coordinates
def convert_coordinates(features):
    for feature in features:
        if feature['geometry'] and feature['geometry']['coordinates']:
            easting, northing = feature['geometry']['coordinates']
            lon, lat = transformer.transform(easting, northing)
            feature['geometry']['coordinates'] = [lon, lat]
    return features

# Load the JSON data
with open(r'server\old_locations.geojson', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert the coordinates
data['features'] = convert_coordinates(data['features'])

# Save the updated data back to a new JSON file
with open(r'server\converted_locations.geojson', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
