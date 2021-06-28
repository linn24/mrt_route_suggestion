# MRT Route Suggestion
This application suggests the shortest route from source to destination at a given start time for the journey.

## Pre-requisites
Install the necessary packages in *requirements.txt* using the command:  
`pip install -r requirements.txt`

## Setup
1) Download the source codes.
2) Open command prompt.
3) Change the directory to the location you saved the downloaded source codes.
4) To setup the database, run *models.py* using the command:  
`python models.py`
5) To import data in .csv file into database, run *initialize_data.py* using the command:  
`python initialize_data.py`
6) Start the application by running the command:  
`python route_manager.py`
7) Once the application is up, APIs can be tested using the URL:  
[http://localhost:8000/api/docs](http://localhost:8000/api/docs)

## APIs
### Get Route
#### Search Parameters
- Source station
- Destination station
- Start time of journey

#### Result - Route Information
- Number of stations travelled
- List of stations along the route
- Detailed instructions

#### How Implementation Works
1) The list of stations is retrieved from database.
    - filtered by start time of journey
    - ordered by ascending order of line ID and station code number
2) The list of edges is populated in memory.
3) Shortest route from source to destination station is generated.
4) Each step in the shortest route is translated into a detailed instruction.