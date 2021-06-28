# MRT Route Suggestion

## Get Route
### Search Parameters
- Source station
- Destination station
- Start time of journey

### Result - Route Information
- Number of stations travelled
- List of stations along the route
- Detailed instructions

### How Implementation Works
1) The list of stations is retrieved from database.
    - filtered by start time of journey
    - ordered by ascending order of line ID and station code number
2) The list of edges is populated in memory.
3) Shortest route from source to destination station is generated.
4) Each step in the shortest route is translated into a detailed instruction.