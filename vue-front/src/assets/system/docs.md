
# DataBase

## Geography

### Singapore Postcode Dataset
**Data Source**: [OneMap API](https://www.onemap.gov.sg/docs/)  
Contains postal addresses with building details, postal codes, and geographic coordinates.

**Fields**:
- `blk_no`: Building block number (e.g., "101A")
- `street`: Road name (e.g., "LORONG 7 TOA PAYOH")
- `building`: Building name (e.g., "KIM KEAT COURT")
- `address`: Full postal address
- `PostCode`: 6-digit postal code (e.g., "310001")
- `X`, `Y`: SVY21 coordinates
- `latitude`, `longitude`: WGS84 coordinates

### Postcode to Subzone Mapping Dataset
**Data Source**: [URA API](https://www.ura.gov.sg/maps/api/)  
Maps postal codes to subzones and planning areas.

**Fields**:
- `PostCode`: 6-digit postal code
- `subzone`: Subzone name (e.g., "LORONG 8 TOA PAYOH")
- `planarea`: Planning area (e.g., "TOA PAYOH")

---

## Housing (HDB)

### HDB Resale Flat Prices Dataset
**Data Source**: [Data.gov.sg](https://data.gov.sg/datasets?query=HDB+resale+transactions)  
Historical resale transaction records.

**Key Fields**:
- `month`: Transaction date (YYYY-MM)
- `town`: Planning area
- `flat_type`: Size classification (2-5 ROOM, EXECUTIVE)
- `blk_no`, `street`: Location details
- `resale_price`: Transaction price (SGD)

### HDB Property Information Dataset
**Data Source**: [Data.gov.sg](https://data.gov.sg/dataset/hdb-property-information)  
Building details including facilities and unit composition.

**Key Fields**:
- `year_completed`: Construction completion year
- `residential/commercial`: Unit types (Y/N)
- `total_dwelling_units`: Total residential units
- Room type counts (e.g., `3room_sold`, `4room_sold`)

### HDB Postcode Mapping Dataset
**Data Source**: [OneMap](https://www.onemap.gov.sg/)  
Maps HDB blocks to postal codes and coordinates.

**Fields**: `blk_no`, `street`, `PostCode`, `LATITUDE`, `LONGITUDE`

---

## Transportation

### MRT/LRT Station Exits Dataset
**Data Source**: [Data.gov.sg](https://data.gov.sg/datasets?query=MRT+location)  
Station exit locations with coordinates.

**Fields**:
- `station_name`: Station name
- `exit_code`: Exit identifier (e.g., "Exit A")
- `latitude`, `longitude`: WGS84 coordinates

### Bus Stop Locations Dataset
**Data Source**: [LTA DataMall](https://datamall.lta.gov.sg/)  
All bus stop locations in Singapore.

**Fields**:
- `bus_stop_n`: Unique stop code
- `loc_desc`: Nearby landmark
- `latitude`, `longitude`: Coordinates

---

## Education

### School Information Dataset
**Data Source**: [Data.gov.sg](https://data.gov.sg/dataset/school-directory)  
Comprehensive school details.

**Key Fields**:
- `school_name`, `address`, `postal_code`
- `mrt_desc`, `bus_desc`: Nearby transport
- `mainlevel_code`: PRIMARY/SECONDARY
- Mother tongue offerings (`mothertongue1_code`)

### Preschool Location Dataset
**Data Source**: [Data.gov.sg](https://data.gov.sg/dataset/child-care-centres)  
Child care center locations.

**Fields**: `centre_name`, `centre_code`, `latitude`, `longitude`

### School CCAs Dataset
**Data Source**: [Data.gov.sg](https://data.gov.sg/collections/457/view)  
Co-curricular activities by school.

**Fields**:
- `cca_grouping`: Category (e.g., "PHYSICAL SPORTS")
- `cca_customized_name`: School-specific CCA name

---

# OneMap API

## Advanced Minimap
This Advanced Mini-Map Creator tool enables users to create a mini-map on the fly with multiple markers and selectable icons. The created min-map can be embedded to websites as an iframe or served out as a hyperlink/URL.

## Search
This API enables users to obtain address information for roads and buildings, etc. This API is great for web forms or application that can benefit from instant address verification or solutions that want localized POI.

**Parameters:**
- Takes a text input which can be:
    - Building name
    - Road name
    - Bus stop number
    - Postal code
      *(e.g. "Revenue House" or "307987")*

**Returns:**
- Address information including:
    - Latitude/longitude
    - X/Y coordinates
- Results sorted by estimated relevance

## Routing

### Public Transport
Retrieves travel paths involving public transports.

**Requirements:**
- Set `routeType` parameter to `pt`
- Choose between 3 modes of public transport
- Additional required parameters:
    - Date
    - Time
    - Mode

### Walk/Drive/Cycle
Retrieves walking, driving or cycling path options.

**Requirements:**
- Provide start and end latitudes/longitudes
- Set `routeType` to:
    - `walk`
    - `drive`
    - `cycle`

## Population Query
Provides population data sets by the Department of Statistics. Data available by planning area or subzone.

**Available Data Types:**
- Age group
- Economic status
- Education status
- Household size
- etc.

### Economic Status Data
Retrieves economic status data for given planning area name and year.

**Note:** If gender is not specified, returns figures for both genders.

### Education Status Data
Retrieves education status data for given planning area name and year.

### Ethnic Distribution
Retrieves ethnic distribution data for given planning area name and year.

**Note:** If gender is not specified, returns figures for both genders.

### Work Income For Household (Monthly)
Retrieves monthly household income data for given planning area name and year.

### Household Size Data
Retrieves household size data for given planning area name and year.

### Household Structure Data
Retrieves household structure data for given planning area name and year.

### Income From Work Data
Retrieves income from work data for given planning area name and year.

### Industry of population Data
Retrieves industry of population data for given planning area name and year.

### Language Literacy Data
Retrieves language literacy data for given planning area name and year.

### Mode of transport to school
Retrieves mode of transport to school data for given planning area name and year.

### Mode of transport to work
Retrieves mode of transport to work data for given planning area name and year.

### Age Data
Retrieves age data for given planning area name and year.

### Religion Data
Retrieves religion data for given planning area name and year.

### Spoken Language Data
Retrieves spoken language data for given planning area name and year.

### Tenancy Data
Retrieves tenancy data for given planning area name and year.

### Dwelling Type Household Data
Retrieves dwelling type household data for given planning area name and year.

### Dwelling Type Population Data
Retrieves dwelling type population data for given planning area name and year.

---

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

