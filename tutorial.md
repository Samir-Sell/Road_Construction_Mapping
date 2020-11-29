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
```
import geopandas # For automation and data cleaning of our geojson files
import os # Allow us to manipulate where we save our files and move around our folders
import matplotlib.pyplot as plt # Allow us to create maps
import requests # Allow us to download our data from the City of Ottawa using their API
from datetime import date # Allow us to generate current dates 
import contextily as ctx # Allow us to add base maps
```
The next step is to create our main function, call it and then set up our file structure:
````
def main():
if __name__ == "__main__":

main()
````

In our main function we want to use the datetime module to generate a date object:
`date_today = str(date.today())`


Next we want to use the OS module to create our file structure and point towards our reference data. All the blow code will go in our main funcion unless otherwise specified.
````
working_directory = os.getcwd() # Find our current working directory in order to build other directories off of this
reference_file = os.path.join(working_directory, "ottawa_boundaries", "ottawa_boundaries.geojson") # Use OS path.join function to point to our reference file
reference_folder = os.path.join(working_directory, "ottawa_boundaries" ) # Create a path for our reference folder 
maps_folder = os.path.join(working_directory, "Maps") # Create a maps folder path
maps_day_folder = os.path.join(maps_folder, date_today) # Create a specific day path in our general maps path
````

We will now use the paths we made and test if they exist within where we are running our program. If they are not, we will create them. We test if the directory already exists in order to prevent us from duplicating folders or from creating complications in our script. 
````
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
````
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

Voila! We now have our file structure created and our reference file stored in a geopandas dataframe! The next step will be to create another get call to download the newest road construction data from the City of Ottawa.
````
# Perform a GET call to pull the GeoJSON construction data from the City of Ottawa's webpage
# Write our geojson get call to a local geojson file with todays date within the geojson directory
print("Downloading road construction data....") # Create an update to inform the user what is happening
geojson_call = requests.get('https://opendata.arcgis.com/datasets/d2fe8f7e3cf24615b62dfc954b5c26b9_0.geojson') # Send the get request
geojson_file = open("./geojson/" + "{date}_rd_construction.geojson".format(date=date_today), "w") # Open a new geojson file with the download date of the geojson
geojson_file.write(geojson_call.text) # Write to our new file
geojson_file.close() # Close the file
````


		
