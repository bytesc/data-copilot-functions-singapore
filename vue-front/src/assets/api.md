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

