
# DataBase

## Geography

### Singapore Postcode Dataset
**Data Source**: [OneMap API](https://www.onemap.gov.sg/docs/)  
Contains postal addresses with building details, postal codes, and geographic coordinates.

[🔍🗃️VIEW DATA SIMPLE](#table-singapore_postcode)

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

[🔍🗃️VIEW DATA SIMPLE](#table-postcode_subzone)

**Fields**:
- `PostCode`: 6-digit postal code
- `subzone`: Subzone name (e.g., "LORONG 8 TOA PAYOH")
- `planarea`: Planning area (e.g., "TOA PAYOH")

---

## Housing (HDB)

### HDB Resale Flat Prices Dataset
**Data Source**: [Data.gov.sg](https://data.gov.sg/datasets?query=HDB+resale+transactions)  
Historical resale transaction records.

[🔍🗃️VIEW DATA SIMPLE](#table-resale_flat_prices)

**Key Fields**:
- `month`: Transaction date (YYYY-MM)
- `town`: Planning area
- `flat_type`: Size classification (2-5 ROOM, EXECUTIVE)
- `blk_no`, `street`: Location details
- `resale_price`: Transaction price (SGD)


### HDB Postcode Mapping Dataset
**Data Source**: [OneMap](https://www.onemap.gov.sg/)  
Maps HDB blocks to postal codes and coordinates.

[🔍🗃️VIEW DATA SIMPLE](#table-hdb)

**Fields**: `blk_no`, `street`, `PostCode`, `LATITUDE`, `LONGITUDE`

---

## Transportation

### MRT/LRT Station Exits Dataset
**Data Source**: [Data.gov.sg](https://data.gov.sg/datasets?query=MRT+location)  
Station exit locations with coordinates.

[🔍🗃️VIEW DATA SIMPLE](#table-mrt_lrt_station)

**Fields**:
- `station_name`: Station name
- `exit_code`: Exit identifier (e.g., "Exit A")
- `latitude`, `longitude`: WGS84 coordinates

### Bus Stop Locations Dataset
**Data Source**: [LTA DataMall](https://datamall.lta.gov.sg/)  
All bus stop locations in Singapore.

[🔍🗃️VIEW DATA SIMPLE](#table-bus_stop)

**Fields**:
- `bus_stop_n`: Unique stop code
- `loc_desc`: Nearby landmark
- `latitude`, `longitude`: Coordinates

---

## Education

### School Information Dataset
**Data Source**: [Data.gov.sg](https://data.gov.sg/dataset/school-directory)  
Comprehensive school details.

[🔍🗃️VIEW DATA SIMPLE](#table-school)

**Key Fields**:
- `school_name`, `address`, `postal_code`
- `mrt_desc`, `bus_desc`: Nearby transport
- `mainlevel_code`: PRIMARY/SECONDARY
- Mother tongue offerings (`mothertongue1_code`)

### Preschool Location Dataset
**Data Source**: [Data.gov.sg](https://data.gov.sg/dataset/child-care-centres)  
Child care center locations.

[🔍🗃️VIEW DATA SIMPLE](#table-preschool_location)

**Fields**: `centre_name`, `centre_code`, `latitude`, `longitude`

### School CCAs Dataset
**Data Source**: [Data.gov.sg](https://data.gov.sg/collections/457/view)  
Co-curricular activities by school.

[🔍🗃️VIEW DATA SIMPLE](#table-school_ccas)

**Fields**:
- `cca_grouping`: Category (e.g., "PHYSICAL SPORTS")
- `cca_customized_name`: School-specific CCA name

---
