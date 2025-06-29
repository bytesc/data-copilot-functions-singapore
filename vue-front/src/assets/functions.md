


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


Here are the additional functions documented in the same format:

## Prediction Functions

### `house_price_prediction_model(month="", storey_range="", planarea="", flat_type="", flat_model="", street_name="", floor_area_sqm=84, lease_commence_date="", remaining_lease="")`

- **Purpose**: Predicts the price of an HDB flat based on various property features using a pre-trained machine learning model.
- **Parameters**:
  - `month`: Transaction month in "YYYY-MM" format (optional)
  - `storey_range`: Original floor range (e.g., "04 to 06") (optional)
  - `planarea`: Planarea where the flat is located (optional)
  - `flat_type`: Type of flat (e.g., "4-room") (optional)
  - `flat_model`: Model of flat (e.g., "Simplified") (optional)
  - `street_name`: Fine-grained location information (optional)
  - `floor_area_sqm`: Floor area in square meters (default: 84)
  - `lease_commence_date`: Year lease commenced (e.g., "1985") (optional)
  - `remaining_lease`: Remaining lease duration (e.g., "59 years 11 months") (optional)
- **Returns**: The predicted price as a float value.

## Information Functions

### `find_schools_near_postcode(postcode, radius_km=2.0)`

- **Purpose**: Finds schools near a given postal code within a specified radius.
- **Parameters**:
  - `postcode`: The postal code to search around (e.g., "123456")
  - `radius_km`: Search radius in kilometers (default: 2.0)
- **Returns**: A pandas DataFrame containing school information (name, address, contact details, etc.) or None if none found.

### `find_preschools_near_postcode(postcode, radius_km=2.0)`

- **Purpose**: Finds preschools within distance of a given postcode with walking distance and time calculations.
- **Parameters**:
  - `postcode`: The postal code to search around (e.g., "123456")
  - `radius_km`: Search radius in kilometers (default: 2.0)
- **Returns**: A pandas DataFrame containing preschool information (name, code, walking metrics) or None if none found.

### `get_hdb_info_with_postcode(postcode)`

- **Purpose**: Retrieves comprehensive HDB (Housing Development Board) information for a given postal code.
- **Parameters**:
  - `postcode`: The postal code to search for (e.g., "123456")
- **Returns**: A dictionary containing HDB information (planarea, flat type, model, lease details, etc.) or None if not found.
