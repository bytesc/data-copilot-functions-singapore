from agent.tools.copilot.utils.read_db import execute_sql, execute_select
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, Integer, Date
from datetime import datetime

engine=create_engine("mysql+pymysql://root:123456@localhost:3306/singapore_land")

full_word_mapping = {
    'RD': 'ROAD',
    'AVE': 'AVENUE',
    'BT': 'BUKIT',
    'BLVD': 'BOULEVARD',
    'CL': 'CLOSE',
    'CTRL': 'CENTRAL',
    'CRES': 'CRESCENT',
    'DR': 'DRIVE',
    'JLN': 'JALAN',
    'KG': 'KAMPONG',
    'LN': 'LANE',
    'LOR': 'LORONG',
    'UPP': 'UPPER',
    'PL': 'PLACE',
    'ST': 'STREET',
    'TG': 'TANJONG',
    'NTH': 'NORTH',
    'STH': 'SOUTH',
    'CTR': 'CENTRE'
}


def process_street_name(street):
    if not isinstance(street, str):
        return street
    parts = street.split()
    updated_parts = []
    for part in parts:
        upper_part = part.upper()
        if upper_part in full_word_mapping:
            full_word = full_word_mapping[upper_part]
            if part == upper_part:
                updated_parts.append(full_word)
            else:
                updated_parts.append(full_word.capitalize())
        else:
            updated_parts.append(part)
    return ' '.join(updated_parts)


csv_file_path = 'D:\IDLE\projects\singapore-land\data-source\Resale flat prices based on registration date from Jan-2017 onwards.csv'

df = pd.read_csv(csv_file_path)

table_name = 'Resale_Flat_Prices'

metadata = MetaData()
table = Table(
    table_name, metadata,
    Column('month', Date),
    Column('town', String(255)),
    Column('flat_type', String(255)),
    Column('blk_no', String(255)),
    Column('street', String(255)),
    Column('storey_range', String(255)),
    Column('floor_area_sqm', Float()),
    Column('flat_model', String(255)),
    Column('lease_commence_date', Integer()),
    Column('resale_price', Integer()),
)

# Create table (if not exists)
metadata.create_all(engine)

# Prepare check and insert SQLs
check_query = f"""
SELECT 1 FROM {table_name} 
WHERE month = '%s' 
AND planarea = '%s' 
AND flat_type = '%s' 
AND blk_no = '%s' 
AND street = '%s' 
AND storey_range = '%s' 
AND floor_area_sqm = %s 
AND flat_model = '%s' 
AND lease_commence_date = %s 
AND resale_price = %s
LIMIT 1
"""

insert_query = f"""
INSERT INTO {table_name} 
(month, planarea, flat_type, blk_no, street, storey_range, floor_area_sqm, flat_model, lease_commence_date, resale_price) 
VALUES ('%s', '%s', '%s', '%s', "%s", '%s', %s, '%s', %s, %s)
"""

i=0
# Insert data
for index, row in df.iterrows():
    try:
        month_date = datetime.strptime(row['month'], '%Y-%m').date()
        processed_street = process_street_name(row['street_name'])

        # Check if row exists
        sql_check = check_query % (
            month_date,
            row['town'],
            row['flat_type'],
            row['block'],
            processed_street,
            row['storey_range'],
            int(row['floor_area_sqm']),
            row['flat_model'],
            int(row['lease_commence_date']),
            int(row['resale_price'])
        )

        result = execute_select(engine, sql_check)

        if not result.empty:
            # Row doesn't exist, insert it
            sql_insert = insert_query % (
                month_date,
                row['town'],
                row['flat_type'],
                row['block'],
                processed_street,
                row['storey_range'],
                int(row['floor_area_sqm']),
                row['flat_model'],
                int(row['lease_commence_date']),
                int(row['resale_price'])
            )
            execute_sql(engine, sql_insert)
            print(i)
            i+=1

    except Exception as e:
        print(f"Error processing row {index}: {e}")
        continue

print("Data has been written to the database.")