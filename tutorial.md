# Road Construction Visualizer

This tutorial will be an introduction to using Geopandas and Matplotlib to automate data download, data cleaning, basic analysis and map making. A basic understanding of Python, Python interpreters and Python module download will be assumed in this tutorial. 

The data for this tutorial is hosted on 
Open Ottawa and can be found here: https://open.ottawa.ca/datasets/construction-road-resurfacing-watermain-sewer-multi-use-pathways-bike-lanes/data?geometry=-76.197%2C45.274%2C-75.675%2C45.359&page=9. It has an application programming interface (API) which will also us to make requests to download data. Additionally, we will be using this geojson as a reference layer for our maps: https://open.ottawa.ca/datasets/wards-2010

***

## Setting up Your Environment

The first step of this tutorial is going to be how to set up your Python environment in order to complete this tutorial. 


- You will need to download Anaconda: https://docs.anaconda.com/anaconda/install/windows/

- Search for and open the Anaconda Prompt  

- Create your environment and when prompted, type y to accept:
`$ conda create --name geo_env`

* Activate your Anaconda virtual environment by typing: 
`$ conda activate geo_env`

- Install the first required packaged called geopandas: 
`$ conda install geopandas`

- Install the second package called matplotlib: 
`$ conda install matplotlib`

- Install the third package called contextily: 
`$ conda install contextily`

- Install the last and final package from Anaconda which allows you to map polygons using Geopandas: `$ conda install -c conda-forge descartes`

- Next you will need an integrated development environment (IDE). This tutorial used Visual Studio Code (VS Code) as it is free and accessible. However, other IDEs such as Pycharm can be used. 
  - The link to install Visual Studio Code can be found here: https://code.visualstudio.com/download

- You will now need to open VS Code and set your interpreter to the virtual geo_env environment you created. 
  - You can follow this tutorial: https://code.visualstudio.com/docs/python/environments#:~:text=To%20do%20so%2C%20open%20the,Settings%2C%20with%20the%20appropriate%20interpreter.


We finally have our entire Python environment set up! 

***

## Beginning to Code

The first step to begin coding is to import all of our modules:
```python
import geopandas # For automation and data cleaning of our geojson files
import os # Allow us to manipulate where we save our files and move around our folders
import matplotlib.pyplot as plt # Allow us to create maps
import requests # Allow us to download our data from the City of Ottawa using their API
from datetime import date # Allow us to generate current dates 
import contextily as ctx # Allow us to add base maps
```
The next step is to create our main function, call it and then set up our file structure:
```python
def main():
if __name__ == "__main__":

main()
```

In our main function we want to use the datetime module to generate a date object:
`date_today = str(date.today())`


Next we want to use the OS module to create our file structure and point towards our reference data. All the blow code will go in our main funcion unless otherwise specified.
```python
working_directory = os.getcwd() # Find our current working directory in order to build other directories off of this
reference_file = os.path.join(working_directory, "ottawa_boundaries", "ottawa_boundaries.geojson") # Use OS path.join function to point to our reference file
reference_folder = os.path.join(working_directory, "ottawa_boundaries" ) # Create a path for our reference folder 
maps_folder = os.path.join(working_directory, "Maps") # Create a maps folder path
maps_day_folder = os.path.join(maps_folder, date_today) # Create a specific day path in our general maps path
````

We will now use the paths we made and test if they exist within where we are running our program. If they are not, we will create them. We test if the directory already exists in order to prevent us from duplicating folders or from creating complications in our script. 
```python
# Check if the overarching maps folder exists and if not, create it
if not os.path.isdir(maps_folder):
 	os.mkdir(maps_folder)

# Check if the specific day directory exists and if not, create it
if not os.path.isdir(maps_day_folder):
        os.mkdir(maps_day_folder)

# Create GeoJSON folder and add it to repository
if not os.path.isdir("./geojson"):
	os.mkdir("./geojson")
````

We will now check to see if our reference layer folder exists, if it does not (ie the first time we run this), we will create it and download the layer file from the City of Ottawa. You will notice I use the word datafram in the comments below. a dataframe is the primary type of data structure used to store information in GeoPandas. 
```python
# If the reference basemap does not exist, create it, download it and write it into a dataframe
if not os.path.isfile(reference_file):
	os.mkdir(reference_folder)
	geojson_call = requests.get('https://opendata.arcgis.com/datasets/845bbfdb73944694b3b81c5636be46b5_0.geojson') # Send the get request and assign it to a variable
	geojson_file = open(reference_file, "w") # Open a new file based on a previous path we have created
	geojson_file.write(geojson_call.text) # Write the text from the geojson to our newly created geojson_file variable.
	geojson_file.close() # Close the file
# Incase we have run our script from this directory before, we create an option to skip this step
else:
	pass
	
reference_layer_read = open(reference_file) # We now read in our reference file
reference_layer_df = geopandas.read_file(reference_layer_read) # We then create our geopandas dataframe by reading in our previously read in reference file
````

Voila! We now have our file structure created and our reference file stored in a geopandas dataframe! The next step will be to create another get call to download the newest road construction data from the City of Ottawa. After that, we will also write this geojson to a GeoPandas dataframe.
```python
# Perform a GET call to pull the GeoJSON construction data from the City of Ottawa's webpage
# Write our geojson get call to a local geojson file with todays date within the geojson directory
print("Downloading road construction data....") # Create an update to inform the user what is happening
geojson_call = requests.get('https://opendata.arcgis.com/datasets/d2fe8f7e3cf24615b62dfc954b5c26b9_0.geojson') # Send the get request
geojson_file = open("./geojson/" + "{date}_rd_construction.geojson".format(date=date_today), "w") # Open a new geojson file with the download date of the geojson
geojson_file.write(geojson_call.text) # Write to our new file
geojson_file.close() # Close the file

# Load the GeoJSON into a Geopandas dataframe
working_file = os.path.join(working_directory , "geojson" , "{date}_rd_construction.geojson".format(date=date_today)) # Create a working file variable path with the current date
gp_read = open(working_file) # Open the current geojson road contruction file (The working file)
gp_df = geopandas.read_file(gp_read) # Write the opened file to a Geopandas dataframe.
````

## Data Cleaning
It is important to be able to automate the processing and cleaning of data. Especially when you receive large amounts of data on a regular basis. In the following steps, we will learn how to extract only the desired data from this relatively large road construction dataset. We have our road construction dataset as a geodataframe which will allow us full access to all of the useful functions and methods within geopandas. 

The first functions we wil use is the .drop method that can be called on a geodataframe (gdf). It takes a parameter of a list of labels where we can specify which columns of our gdf we want dropped. In this case, we are removing the French columns and some other columns that are not required in our analysis. The axis parameter tell geopandas which row we want to search for the labels in. We entered 1, as these are our column headings. Lastly, we used the method .dropna which removed all rows where there is missing data (N/A or NaN). 

```python
# Remove uneeded columns and drop rows with no values
print("Cleaning and processing data....") # Provide the user with an update
clean_df = gp_df.drop(labels=[
	'FEATURE_TYPE_FR', 'STATUS_FR', 'TARGETED_START_FR', 'PROJECT_MANAGER', 'PROJECTWEBPAGE', 'PROJECTWEBPAGE_FR'
        ], axis=1).dropna()
````

We are basing our series of maps on the "STATUS" column of the data. From look at the data earlier, you may have noticed some of the values were NOTAVAIL which is not good for our analysis. Therefore, we will remove these rows from our data. We use a geopandas filter again to pull only the STATUS column from our geodataframe. We then cast it into a set in order to get rid of duplicate values. We then loop through the set to check if there are "NOTAVAIL" values in our data. If there is, we perform another filter that only selects for data where the STATUS column value is NOT "NOTAVAIL". This new filter then becomes a new geodataframe called status_removed. 

```python
# Check for NOTAVAIL and if these rows exist, then remove them
not_avail_check = set(clean_df['STATUS']) # Create filter to select all values in the STATUS column
    for value in not_avail_check: # Loop through the set to check for NOTAVAIL values
        if value == 'NOTAVAIL':
            status_removed = clean_df[clean_df.STATUS != 'NOTAVAIL'] # Create filter to only select rows where the STATUS column value does not equal NOTAVAIL
        else:
            pass
````

Since we will be putting this data on a map, we want to make sure we remove any data that does not have an actual location / geometry attached to it. Geopandas has a handy feature / filter we can use to check this called .is_empty. If a geometry is missing, the cell will return a value of true. We want to use this as a filter in order to only select data that does not have missing geometry. We also use a tilda (~) to invert the data from false to true. Therefore, a row with no geometry will return true, and we will invert that to false. 

```python
 # Drop empty geometries 
 clean_df = status_removed[~status_removed.is_empty]
 ````
 
 The filter we just created will now be further filtered in order to pull only road data from the whole dataset. We will create another filter to only select data from "FEATURE_TYPE". We will then convert these rows to strings and then use the string method called .startswith() to select only road construction features. The road_filter is then used to filter our clean_df dataframe and create a new final geodataframe called road_df. 
 
 ```python
# Filter for road resurfacing attributes by creating a filter
road_filter = clean_df["FEATURE_TYPE"].str.startswith("RD") # Create filter
road_df = clean_df[road_filter] # Apply Filter
````
 
 ## Making the Maps
 
We now have our final cleaned data that has no missing values, no missing geometries, no undeeded columns and only construction relating to roads. The next step is to turn this data into a consumable map using matplotlib. This tutorial intends to create a series of maps that will differ based on the targeted start of the construction project. The next snippet of code will generate all the data we are going to need to send to a function we will write called save_map(). 
 
First, we want to write a string that will let us identify which map we are working on. We will then create a new filter based on the "TARGETED_START" column and convert the data to string and then select cells that start with "This". Based on our manual data examination at the beginning of this tutorial, you may have noticed that in progress construction projects start with "This". We will then apply this filter to our road_df to create a new geodataframe for this map. Lastly, we will send our reference layer we created from before, the gdf we just created, our identification string, todays date and the directory we created to our save maps. These will be sent to a function we are going to create called save_map. 
 
 ```python
# Filter for road construction and send layers to be processed into a map
layer_title = "This_Year_" # Create an identification name for this map
in_progress_filter = road_df["TARGETED_START"].str.startswith("This") # Create filter
in_progress_df = road_df[in_progress_filter] # Apply filter
save_map(reference_layer_df, in_progress_df, layer_title, date_today, maps_day_folder) # Send layers
 ```
 
 ## Creating the save_map function
 
We are going to create a function to handle map creation for the 4 time periods we want to display. We will make date specific maps to represent this years projects, 1 to 2 years, 3 to 5 years, and 4 to 7 years. This function will be sent our reference layer we created from before, the gdf we just createdc(in_progess_df), our identification string, todays date and the directory we created to save our maps. 
 
 Lets declare the function and send in our data. 
 
```python
def save_map(reference_layer_df, in_df, layer_title, date_today, mapping_directory):
    
	'''
	Function to create maps and calculate length of road constructions
	'''
````
The following code, unless specified, will now be placed in our function. 

In this snippet, we create the figure and the axis object.We specify we want only 1 column and 1 row, and then we specify the figure size we want it ot output. The final title for the figure is created. Then we use a method to assign our final title string to the figure and dictate its size, as well as the pad. The pad is short for padding and dictates how far the title will hover above the figure. 


```python
# Create axis to be plotted
fig, ax = plt.subplots(1,1,figsize=(15,15)) # Generate Figure

# Create title
map_title = layer_title.replace("_", " ") + "Road Construction" # String concatenation to make final title 
plt.title(label=map_title, fontdict={'fontsize' : 30}, pad=10) # Create and format figure title
````

Now we will plot our layers to the axis of the figure. First, we have to specify which axis was want to add the layer to. Then we can assign a color and an edge color. We can also use the alpha parameter to adjust transparency. We can assign a line width and then specify the zorder. The zorder lets us organize which layers will be on top of other layers. A higher z order in one layer places it above another layer with a lower zorder. It is also important to assign which column we want to plot. Lastly, we can also specify if we want to display a legend for a specific layer.

```python
# Assign layers to the axis
reference_layer_df.plot(ax=ax, color='white', alpha=0.5, edgecolor='black', linewidth=0.2, zorder=1) # Plot the reference layers
in_df.plot(ax=ax, linewidth=1.2, zorder=2, column="FEATURE_TYPE", legend=True) # Plot the road construction layer
````

Next we want to calculate the length of the road construction for each map. Currently our data is in a geographic coordinate system. We need to project it to a projected coordinate system. We will use the Canada Lambert Conformal Conic projection in this tutorial. Geopandas has the built in functionality to reproject our data by using .to_crs method. As a parameter, we can give the method a CRS ID. 

We will then use the .length function to calculate the length of each geometry in the dataframe. Then we will sum the lengths to get the total length and then divide by 1000 to convert to kilometers. The unit was in meters as that is the unit of the crs we used. We will then format the string to two decimal places. Then we call a method to add the road construction length to our figure. We specify where we want it as x and y coordinates and then feed it the actual text itself. 
.

```python
# Reproject to Canada Lambert Conformal Conic in order to correctly calculate lengths in meters and add to map as kilometers
projected_df = in_df.to_crs("ESRI:102002")
length_of_roads = (projected_df.length.sum())/1000
length_for_map = "{:.0f}".format(length_of_roads)
plt.text(x=-75.4,y=44.95, s="Road Work (km): {}".format(length_for_map)) # Add text with length info to our maps
````

A basemap is always useful in order to give context to a map. We are going to use a python library called Contextily that will allow us to access Open Street Map and utilize it as a basemap. We will using its .add_basemap method to add a basemap to our axis. First we specify which axis we want to add it to, then we specify which crs we want to display the basemap in. It has to be the same crs as our data. In order to ensure this, we call the .crs method of our geodataframe and then we convert the value to a string in order to be an acceptable parameter. Then we specify the source of the basemap by acessing contextilys providers and then specifiing open street map and then mapnik. 

```python
# Assign basemap
ctx.add_basemap(ax, crs=in_df.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)
````

Finally, we will save our finished map.The first step will be to create a file name for the map. The we will use the path.join method of the OS module to allow us to join our mapping directory and the mape_name file name in order to create a new file path. We will then use that full file path to save our figure using our figures .savefig method. This will be the end of our fully completed function.

```python
# Save map to mapping directory
map_name = layer_title + date_today
print("Saving map: " + map_name + "....")
plt.savefig(os.path.join(mapping_directory, map_name))
````

## Finishing Touches 

We now have our function created and everything else layed out. We now need to call the function three more times in order to create the rest of our maps for the different expected construction time periods. We will repeat the code snippet that was used in the "Making the Map" subheader of this tutorial. However, we will alter the layer title and what values we are filtering for in order to create a map for projects started in the next 1 to 2 years, 3 to 5 years and then 4 to 7 years. The code explanation is the same and the 3 other maps are posted below and are in our main function under the in progress snippet we created earlier. 

```python
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
````

Congratulations! You have now created your map generating tool for 
