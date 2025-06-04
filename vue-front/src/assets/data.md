
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
