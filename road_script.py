# Import required modules
# This must be installed first to map polygons with geopandas: $conda install -c conda-forge descartes
import geopandas
import os
import matplotlib.pyplot as plt
import requests
from datetime import date
import contextily as ctx


def save_map(reference_layer_df, in_df, layer_title, date_today, mapping_directory):
    
    '''
    Function to create map and calculate length of constructions
    '''

    #Create axis to be plotted
    fig, ax = plt.subplots(1,1,figsize=(15,15))

    # Create title
    map_title = layer_title.replace("_", " ") + "Road Construction"
    plt.title(label=map_title, fontdict={'fontsize' : 40}, pad=10)

    # Assign layers to the axis
    reference_layer_df.plot(ax=ax, color='white', alpha=0.5, edgecolor='black', linewidth=0.2, zorder=1)
    in_df.plot(ax=ax, linewidth=1.2, zorder=2, column="FEATURE_TYPE", legend=True)

    # Reproject to Canada Lambert Conformal Conic in order to correctly calculate lengths in meters and add to map
    projected_df = in_df.to_crs("ESRI:102002")
    length_of_roads = projected_df.length.sum()
    length_for_map = "{:.0f}".format(length_of_roads)
    plt.text(x=-75.4,y=44.95, s="Road Work (m): {}".format(length_for_map)) # Add text with length info to our maps

    # Assign basemap
    ctx.add_basemap(ax, crs=in_progress_df.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

    # Save map to mapping directory
    map_name = layer_title + date_today
    print("Saving map: " + map_name + "....")
    plt.savefig(os.path.join(mapping_directory, map_name))

# Create date string and assemble required strings for file names
date_today = str(date.today())
working_directory = os.getcwd()
reference_file = os.path.join(working_directory, "ottawa_boundaries", "ottawa_boundaries.geojson" )
reference_folder = os.path.join(working_directory, "ottawa_boundaries" )
maps_folder = os.path.join(working_directory, "Maps")
maps_day_folder = os.path.join(maps_folder, date_today)

# Check if the overarching maps folder exists and if not, create it
if not os.path.isdir(maps_folder):
    os.mkdir(maps_folder)

# Check if the specific day directory exists and if not, create it
if not os.path.isdir(maps_day_folder):
    os.mkdir(maps_day_folder)

# Create GeoJSON file and add it to repository
# Store our files in a geojson directory
if not os.path.isdir("./geojson"):
    os.mkdir("./geojson")


# If the reference basemap does not exist, create it and download it and write it into a DF
if not os.path.isfile(reference_file):
    os.mkdir(reference_folder)
    geojson_call = requests.get('https://opendata.arcgis.com/datasets/845bbfdb73944694b3b81c5636be46b5_0.geojson')
    geojson_file = open(reference_file, "w")
    geojson_file.write(geojson_call.text)
else:
    pass

reference_layer_read = open(reference_file)
reference_layer_df = geopandas.read_file(reference_layer_read)

# Perform a GET call to pull the GeoJSON construction data from the City of Ottawa's webpage
# Write our geojson get call to a local geojson file with todays date within a geojson directory
print("Downloading road construction data....")
geojson_call = requests.get('https://opendata.arcgis.com/datasets/d2fe8f7e3cf24615b62dfc954b5c26b9_0.geojson')
geojson_file = open("./geojson/" + "{date}_rd_construction.geojson".format(date=date_today), "w")
geojson_file.write(geojson_call.text)
geojson_file.close()

# Load the GeoJSON into a Geopandas dataframe
working_file = os.path.join(working_directory , "geojson" , "{date}_rd_construction.geojson".format(date=date_today))
gp_read = open(working_file)
gp_df = geopandas.read_file(gp_read)

# Remove uneeded columns and drop rows with no values
print("Cleaning and processing data....")
clean_df = gp_df.drop(labels=[
    'FEATURE_TYPE_FR', 'STATUS_FR', 'TARGETED_START_FR', 'PROJECT_MANAGER', 'PROJECTWEBPAGE', 'PROJECTWEBPAGE_FR'
    ], axis=1).dropna()

# Check for NOTAVAIL and if these rows exist, then remove them
not_avail_check = list(set(clean_df['STATUS']))
for value in not_avail_check:
    if value == 'NOTAVAIL':
        status_removed = clean_df[clean_df.STATUS != 'NOTAVAIL']
    else:
        pass

# Drop empty geometries 
clean_df = status_removed[~status_removed.is_empty]

# Filter for road resurfacing attributes by creating a filter
road_filter = clean_df["FEATURE_TYPE"].str.startswith("RD") # Create filter
road_df = clean_df[road_filter] # Apply Filter

# Filter for road construction and send layers to be processed into a map
layer_title = "This_Year_"
in_progress_filter = road_df["TARGETED_START"].str.startswith("This") # Create filter
in_progress_df = road_df[in_progress_filter] # Apply filter
save_map(reference_layer_df, in_progress_df, layer_title, date_today, maps_day_folder) # Send layers

# Filter for road construction starting in 1 - 2 years and send layers to be processed into a map
layer_title = "1-2_Years_"
one_to_two_filter = road_df["TARGETED_START"].str.startswith("1") # Create filter
one_to_two_df = road_df[one_to_two_filter] # Apply filter
save_map(reference_layer_df, one_to_two_df, layer_title, date_today, maps_day_folder) # Send layers

# Filter for road construction starting in 3 - 5 years and send layers to be processed into a map
layer_title = "3-5_Years_"
three_to_five_filter = road_df["TARGETED_START"].str.startswith("3") # Create filter
three_to_five_df = road_df[three_to_five_filter] # Apply filter
save_map(reference_layer_df, three_to_five_df, layer_title, date_today, maps_day_folder) # Send layers

# Filter for road construction starting in 4 - 7 years and send layers to be processed into a map
layer_title = "4-7_Years_"
four_to_seven_filter = road_df["TARGETED_START"].str.startswith("4") # Create filter
four_to_seven_df = road_df[four_to_seven_filter] # Apply filter
save_map(reference_layer_df, four_to_seven_df, layer_title, date_today, maps_day_folder) # Send layers

print("Script completed successfully")
