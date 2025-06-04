


# Functions

These functions collectively support tasks ranging from geospatial visualization to database interaction and data plotting.

## Map-Related Functions

These functions handle map data and generate map visualizations.

### `get_minimap(lat_lng_list, postcode_list)`

- **Purpose**: Generates an HTML iframe for an embedded minimap with optional markers.
- **Parameters**:
    - `lat_lng_list`: Optional list of (latitude, longitude) tuples to mark locations.
    - `postcode_list`: Optional list of postal codes to mark locations.
- **Returns**: An HTML iframe string for embedding the map.

### `get_api_result(url)`

- **Purpose**: Fetches data (e.g., demographic statistics) from a predefined API.
- **Parameters**:
    - `url`: The relative URL path of the API endpoint (not the full URL).
- **Returns**: The API response as a JSON dictionary or list.

## Database & Data Processing Functions

These functions query databases and process/visualize data.

### `query_database(question, df_cols)`

- **Purpose**: Executes a natural-language query on a connected database.
- **Parameters**:
    - `question`: A natural-language question (e.g., "Select grades for Jane Smith").
    - `df_cols`: Optional column names (string or list) to structure the output DataFrame.
- **Returns**: A pandas DataFrame containing query results.

### `draw_graph(question, data)`

- **Purpose**: Generates a graph based on natural-language instructions and input data.
- **Parameters**:
    - `question`: A natural-language graph description (e.g., "Plot a line chart").
    - `data`: Input data as a pandas DataFrame.
- **Returns**: A URL string pointing to the generated graph image.

