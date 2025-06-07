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
                # "latitude": row[7],
                # "longitude": row[8],
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
            LIMIT 50
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
