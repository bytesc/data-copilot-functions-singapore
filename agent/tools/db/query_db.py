import sqlalchemy


def from_username_to_uid_func(username: str, engine):
    conn = engine.connect()
    try:
        result = conn.execute(sqlalchemy.text("""
                        SELECT uid FROM user_info WHERE username=:username
                                            """),
                              {"username": username})
        conn.commit()
        user_result = result.fetchone()
        if user_result:
            return user_result[0]
        return None
    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()


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
                WHERE PostCode = :postcode
                LIMIT 1
            )
            SELECT 
                s.school_name, 
                s.address, 
                s.postal_code, 
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
            JOIN singapore_postcode sp ON s.postal_code = sp.PostCode
            CROSS JOIN postcode_location pl
            WHERE 
                sp.latitude BETWEEN pl.latitude - :radius_deg AND pl.latitude + :radius_deg
                AND sp.longitude BETWEEN pl.longitude - :radius_deg AND pl.longitude + :radius_deg
            HAVING distance_km <= :radius_km
            ORDER BY distance_km
            LIMIT 20
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
                "postal_code": row[2],
                "telephone": row[3],
                "email": row[4],
                "mrt": row[5],
                "bus": row[6],
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
