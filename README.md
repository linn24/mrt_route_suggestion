# MRT Route Suggestion
This application suggests the shortest route from source to destination at a given start time for the journey.

## Pre-requisites
Install the necessary packages in *requirements.txt* using the command:  
`pip install -r requirements.txt`

## Setup
1) Download the source codes.
2) Open command prompt.
3) Change the directory to *mrt_route_suggestion* in the location you saved the downloaded source codes.
4) To setup the database, run *models.py* using the command:  
`python mrt_app/models.py`
5) To import data in .csv file into database, run *initialize_data.py* using the command:  
`python mrt_app/initialize_data.py`
6) Start the application by running the command:  
`python mrt_app/route_manager.py`
7) Once the application is up, APIs can be tested using the URL:  
[http://localhost:8000/api/docs](http://localhost:8000/api/docs)

## Unit Tests
1) Install mrt_app:  
`pip install -e .`
2) Run tests:  
`pytest`

## APIs
### Get All MRT Lines
#### Result - MRT Line Information
- List of lines
    - ID of each line
    - Name of each line
    - List of stations
        - ID of each station
        - Name of each station
        - Code number of each station
        - Opening date of each station

### Get Shortest Route - V1 (Without Consideration for Distance)
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

### Get Shortest Route - V2 (With Consideration for Distance)
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
    - Distance of self-linked edges for interchanges is considered as 0.
    - Distance between two stations is considered as 1.
3) Shortest route from source to destination station is generated.
4) Each step in the shortest route is translated into a detailed instruction.

### Get Fastest Route (With Consideration for Delay)
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
    - Weight of each edge is the travel time or delay between two stations.
3) Shortest route from source to destination station is generated.
4) Each step in the shortest route is translated into a detailed instruction.