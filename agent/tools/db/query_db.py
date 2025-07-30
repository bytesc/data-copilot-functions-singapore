import datetime

import sqlalchemy


def find_schools_near_postcode_func(postcode: str, engine, radius_km: float = 2.0):
    """
    Find schools near a given postal code within a specified radius.

    Args:
        postcode (str): The postal code to search around
        engine: SQLAlchemy engine for database connection
        radius_km (float): Search radius in kilometers (default 2km)

    Returns:
        List of dictionaries containing school information within the radius
    """
    conn = engine.connect()
    try:
        # Calculate approximate degrees for the radius (1km ~ 0.009 degrees)
        radius_deg = radius_km * 0.009

        result = conn.execute(sqlalchemy.text("""
            WITH postcode_location AS (
                SELECT latitude, longitude 
                FROM singapore_postcode 
                WHERE postcode = :postcode
                LIMIT 1
            )
            SELECT 
                s.school_name, 
                s.address, 
                s.postcode, 
                s.telephone_no, 
                s.email_address,
                s.mrt_desc,
                s.bus_desc,
                sp.latitude,
                sp.longitude,
                (6371 * ACOS(
                    COS(RADIANS(pl.latitude)) * COS(RADIANS(sp.latitude)) * 
                    COS(RADIANS(sp.longitude) - RADIANS(pl.longitude)) + 
                    SIN(RADIANS(pl.latitude)) * SIN(RADIANS(sp.latitude))
                )) AS distance_km
            FROM school s
            JOIN singapore_postcode sp ON s.postcode = sp.PostCode
            CROSS JOIN postcode_location pl
            WHERE 
                sp.latitude BETWEEN pl.latitude - :radius_deg AND pl.latitude + :radius_deg
                AND sp.longitude BETWEEN pl.longitude - :radius_deg AND pl.longitude + :radius_deg
            HAVING distance_km <= :radius_km
            ORDER BY distance_km
            LIMIT 50
        """), {
            "postcode": postcode,
            "radius_deg": radius_deg,
            "radius_km": radius_km
        })

        schools = []
        for row in result:
            schools.append({
                "school_name": row[0],
                "address": row[1],
                "postcode": row[2],
                "telephone": row[3],
                "email": row[4],
                # "mrt": row[5],
                # "bus": row[6],
                "latitude": row[7],
                "longitude": row[8],
                "distance_km": row[9]
            })

        return schools

    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()


def find_preschools_near_postcode_func(postcode: str, engine, radius_km: float = 2.0):
    conn = engine.connect()
    try:
        radius_deg = radius_km * 0.009

        result = conn.execute(sqlalchemy.text("""
            WITH postcode_location AS (
                SELECT latitude, longitude 
                FROM singapore_postcode 
                WHERE postcode = :postcode
                LIMIT 1
            )
            SELECT 
                pl.centre_name,
                pl.centre_code,
                pl.latitude,
                pl.longitude,
                SQRT(POW(:radius_deg * (pl.latitude - pc.latitude), 2) + POW(:radius_deg * (pl.longitude - pc.longitude), 2)) AS distance_km
            FROM preschool_location pl
            CROSS JOIN postcode_location pc
            WHERE 
                pl.latitude BETWEEN pc.latitude - :radius_deg AND pc.latitude + :radius_deg
                AND pl.longitude BETWEEN pc.longitude - :radius_deg AND pc.longitude + :radius_deg
            ORDER BY distance_km
            LIMIT 20
        """), {
            'postcode': postcode,
            'radius_deg': radius_deg,
            'radius_km': radius_km
        })

        preschools = []
        for row in result:
            preschools.append({
                'centre_name': row[0],
                'centre_code': row[1],
                'latitude': row[2],
                'longitude': row[3],
                'distance_km': row[4]
            })

        return preschools

    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()


def postcode_to_location(postcode: str, engine):
    conn = engine.connect()
    try:
        result = conn.execute(sqlalchemy.text("""
            SELECT latitude,longitude FROM singapore_postcode where postcode=:postcode
        """), {
            'postcode': postcode,
        })

        for row in result:
            return float(row[0]), float(row[1])

    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()


# def get_hdb_info_by_postcode(engine, postcode: str, storey_range="",
#                              flat_type="", flat_model="",
#                              floor_area_sqm=84, lease_commence_date="",
#                              remaining_lease=""):
#     conn = engine.connect()
#     try:
#         # First get the block number and street from the hdb table
#         hdb_result = conn.execute(sqlalchemy.text("""
#             SELECT blk_no, street FROM hdb WHERE postcode = :postcode
#         """), {'postcode': postcode})
#
#         hdb_info = hdb_result.fetchone()
#         if not hdb_info:
#             return None
#
#         blk_no, street = hdb_info
#
#         # Then get additional details from resale_flat_prices
#         resale_result = conn.execute(sqlalchemy.text("""
#             SELECT
#                 planarea,
#                 flat_type,
#                 flat_model,
#                 street,
#                 floor_area_sqm,
#                 lease_commence_date
#             FROM resale_flat_prices
#             WHERE blk_no = :blk_no AND street = :street
#             ORDER BY month DESC
#             LIMIT 1
#         """), {'blk_no': blk_no, 'street': street})
#
#         resale_info = resale_result.fetchone()
#         if not resale_info:
#             # return None
#             # return {
#             #     'blk_no': blk_no,
#             #     'street_name': street,
#             #     'message': 'Basic address information found but no resale data available'
#             # }
#             return {
#                 'planarea': "",
#                 'flat_type': "",
#                 'flat_model': "",
#                 'street_name': street,
#                 'floor_area_sqm': 84,
#                 'lease_commence_date': "",
#                 'remaining_lease': "",
#                 'blk_no': blk_no,
#             }
#
#         # Unpack the result
#         (planarea, flat_type, flat_model, street_name,
#          floor_area_sqm, lease_commence_date) = resale_info
#
#         # Calculate remaining lease (HDB lease is typically 99 years)
#         current_year = datetime.datetime.now().year
#         lease_years_passed = current_year - lease_commence_date
#         remaining_lease_years = 99 - lease_years_passed
#         remaining_lease_months = 12 - datetime.datetime.now().month
#
#         # Format remaining lease string
#         if remaining_lease_months == 12:
#             remaining_lease_years += 1
#             remaining_lease_months = 0
#         remaining_lease = f"{remaining_lease_years} years {remaining_lease_months} months"
#
#         return {
#             'planarea': planarea,
#             'flat_type': flat_type,
#             'flat_model': flat_model,
#             'street_name': street_name,
#             'floor_area_sqm': floor_area_sqm,
#             'lease_commence_date': str(lease_commence_date),
#             'remaining_lease': remaining_lease,
#             'blk_no': blk_no,
#         }
#
#     except Exception as e:
#         print(f"Error retrieving HDB info: {e}")
#         raise e
#     finally:
#         conn.close()

def get_hdb_info_by_postcode(engine, postcode: str, storey_range="",
                             flat_type="", flat_model="",
                             floor_area_sqm=0, lease_commence_date=""):
    conn = engine.connect()
    try:
        # First get the block number and street from the hdb table
        hdb_result = conn.execute(sqlalchemy.text("""
            SELECT blk_no, street FROM hdb WHERE postcode = :postcode
        """), {'postcode': postcode})

        hdb_info = hdb_result.fetchone()
        if not hdb_info:
            return {
                'planarea': "",
                'flat_type': flat_type,
                'flat_model': flat_model,
                'street_name': "",
                'floor_area_sqm': 84,
                'lease_commence_date': lease_commence_date,
                'remaining_lease': "",
                'blk_no': "",
                'storey_range': storey_range,
            }

        blk_no, street = hdb_info

        # Build the base query for resale_flat_prices
        query = """
            SELECT 
                planarea, 
                flat_type, 
                flat_model, 
                street, 
                floor_area_sqm, 
                lease_commence_date,
                storey_range
            FROM resale_flat_prices
            WHERE blk_no = :blk_no AND street = :street
        """

        params = {'blk_no': blk_no, 'street': street}

        # Add optional filters based on provided parameters
        if storey_range != "":
            query += " AND storey_range = :storey_range"
            params['storey_range'] = storey_range
        if flat_type != "":
            query += " AND flat_type = :flat_type"
            params['flat_type'] = flat_type
        if flat_model != "":
            query += " AND flat_model = :flat_model"
            params['flat_model'] = flat_model
        if floor_area_sqm != 0:
            query += " AND floor_area_sqm = :floor_area_sqm"
            params['floor_area_sqm'] = floor_area_sqm
        if lease_commence_date != "":
            query += " AND lease_commence_date = :lease_commence_date"
            params['lease_commence_date'] = lease_commence_date

        # Add ordering and limit
        query += " ORDER BY month DESC LIMIT 1"

        # Execute the query
        resale_result = conn.execute(sqlalchemy.text(query), params)
        resale_info = resale_result.fetchone()

        if not resale_info:
            return {
                'planarea': "",
                'flat_type': flat_type,
                'flat_model': flat_model,
                'street_name': street,
                'floor_area_sqm': 84,
                'lease_commence_date': lease_commence_date,
                'remaining_lease': "",
                'blk_no': blk_no,
                'storey_range': storey_range,
            }

        # Unpack the result
        (planarea, flat_type, flat_model, street_name,
         floor_area_sqm, lease_commence_date, storey_range) = resale_info

        # Calculate remaining lease (HDB lease is typically 99 years)
        current_year = datetime.datetime.now().year
        lease_years_passed = current_year - lease_commence_date
        remaining_lease_years = 99 - lease_years_passed
        remaining_lease_months = 12 - datetime.datetime.now().month

        # Format remaining lease string
        if remaining_lease_months == 12:
            remaining_lease_years += 1
            remaining_lease_months = 0
        remaining_lease = f"{remaining_lease_years} years {remaining_lease_months} months"

        # Check remaining_lease filter if provided
        if remaining_lease:
            # Extract years from the remaining_lease string (assuming format like "50 years")
            try:
                required_years = int(remaining_lease.split()[0])
                actual_years = remaining_lease_years
                if actual_years < required_years:
                    return None
            except (IndexError, ValueError):
                pass  # Ignore if remaining_lease filter is malformed

        return {
            'planarea': planarea,
            'flat_type': flat_type,
            'flat_model': flat_model,
            'street_name': street_name,
            'floor_area_sqm': floor_area_sqm,
            'lease_commence_date': str(lease_commence_date),
            'remaining_lease': remaining_lease,
            'blk_no': blk_no,
            'storey_range': storey_range,
        }

    except Exception as e:
        print(f"Error retrieving HDB info: {e}")
        raise e
    finally:
        conn.close()
