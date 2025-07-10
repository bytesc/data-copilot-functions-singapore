import sqlalchemy


def query_resale_flats(engine, month=None, plan_area=None, flat_type=None, blk_no=None,
                       street=None, storey_range=None, floor_area_sqm_from=None, floor_area_sqm_to=None,
                       flat_model=None, lease_commence_date_from=None, lease_commence_date_to=None, resale_price=None):
    conn = engine.connect()
    try:
        # Base query
        query = "SELECT * FROM resale_flat_prices WHERE 1=1"
        params = {}

        # Add conditions for each parameter if provided
        if month is not None:
            query += " AND month = :month"
            params['month'] = month
        if plan_area is not None:
            query += " AND planarea = :planarea"
            params['planarea'] = plan_area
        if flat_type is not None:
            query += " AND flat_type = :flat_type"
            params['flat_type'] = flat_type
        if blk_no is not None:
            query += " AND blk_no = :blk_no"
            params['blk_no'] = blk_no
        if street is not None:
            query += " AND street = :street"
            params['street'] = street
        if storey_range is not None:
            query += " AND storey_range = :storey_range"
            params['storey_range'] = storey_range

        # Handle floor area range
        if floor_area_sqm_from is not None and floor_area_sqm_to is not None:
            query += " AND floor_area_sqm BETWEEN :floor_area_from AND :floor_area_to"
            params['floor_area_from'] = floor_area_sqm_from
            params['floor_area_to'] = floor_area_sqm_to
        elif floor_area_sqm_from is not None:
            query += " AND floor_area_sqm >= :floor_area_from"
            params['floor_area_from'] = floor_area_sqm_from
        elif floor_area_sqm_to is not None:
            query += " AND floor_area_sqm <= :floor_area_to"
            params['floor_area_to'] = floor_area_sqm_to

        if flat_model is not None:
            query += " AND flat_model = :flat_model"
            params['flat_model'] = flat_model

        # Handle lease commence date range
        if lease_commence_date_from is not None and lease_commence_date_to is not None:
            query += " AND lease_commence_date BETWEEN :lease_commence_date_from AND :lease_commence_date_to"
            params['lease_commence_date_from'] = lease_commence_date_from
            params['lease_commence_date_to'] = lease_commence_date_to
        elif lease_commence_date_from is not None:
            query += " AND lease_commence_date >= :lease_commence_date_from"
            params['lease_commence_date_from'] = lease_commence_date_from
        elif lease_commence_date_to is not None:
            query += " AND lease_commence_date <= :lease_commence_date_to"
            params['lease_commence_date_to'] = lease_commence_date_to

        if resale_price is not None:
            query += " AND resale_price = :resale_price"
            params['resale_price'] = resale_price

        result = conn.execute(sqlalchemy.text(query), params)

        # Return all rows as a list of dictionaries
        return [dict(row) for row in result]

    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()


def get_llm_predict_hdb_info(engine, plan_area=None, flat_type=None, blk_no=None,
                             street=None, storey_range=None, floor_area_sqm_from=None, floor_area_sqm_to=None,
                             flat_model=None, lease_commence_date_from=None, lease_commence_date_to=None):
    hdb_price_history = query_resale_flats(
        engine,
        plan_area=plan_area,
        flat_type=flat_type,
        blk_no=blk_no,
        street=street,
        storey_range=storey_range,
        floor_area_sqm_from=floor_area_sqm_from,
        floor_area_sqm_to=floor_area_sqm_to,
        flat_model=flat_model,
        lease_commence_date_from=lease_commence_date_from,
        lease_commence_date_to=lease_commence_date_to
    )

    search_conditions = {
        'plan_area': plan_area,
        'blk_no': blk_no,
        'street': street,
        'flat_model': flat_model,
        'flat_type': flat_type,
        'storey_range': storey_range,
        'floor_area_sqm_from': floor_area_sqm_from,
        'floor_area_sqm_to': floor_area_sqm_to,
        'lease_commence_date_from': lease_commence_date_from,
        'lease_commence_date_to': lease_commence_date_to,
    }
    search_conditions = {k: v for k, v in search_conditions.items() if v is not None}

    if len(hdb_price_history) > 50:
        monthly_data = {}
        for record in hdb_price_history:
            month = record['month']
            price = record['resale_price']
            if month not in monthly_data:
                monthly_data[month] = {
                    'total_price': 0,
                    'count': 0,
                    'records': []
                }
            monthly_data[month]['total_price'] += price
            monthly_data[month]['count'] += 1
            monthly_data[month]['records'].append(record)
        averaged_data = []
        for month, data in monthly_data.items():
            avg_price = data['total_price'] / data['count']
            result_record = {
                'month': month,
                'avg_resale_price': avg_price,
                'original_count': data['count']
            }
            averaged_data.append(result_record)

        return search_conditions, averaged_data

    else:
        return search_conditions, hdb_price_history


from .utils.call_llm_test import call_llm


def get_llm_predict_hdb_prompt(from_date, to_date, search_conditions, hdb_price_history):
    pre_prompt = """
You are a real estate expert specializing in Singapore HDB flat prices. 
Based on the historical price data and search conditions provided, predict the resale prices for each month between the specified date range.
"""

    search_prompt = """
### Search Conditions:
""" + str(search_conditions)

    history_prompt = """
### Historical Price Data:
""" + str(hdb_price_history)

    date_prompt = """
### You should predict the result in the month range:
""" + "from date:\n"+str(from_date)+"\nto date:\n"+str(to_date)

    end_prompt = """
### Instructions:
1. Analyze the historical price trends considering factors like location, flat type, size, etc.
2. Predict the resale price for each month in the specified date range.
3. Consider typical market trends, seasonality, and any relevant economic factors.
4. Return your predictions in JSON format with an array of objects, each containing:
   - "month": in "yyyy-mm" format
   - "predicted_price": as a float value
5. Only return the result json without any explanation or comments!!!

### Output Format Example:
[
    {"month": "2023-01", "predicted_price": 450000.0},
    {"month": "2023-02", "predicted_price": 452000.0},
    ...
]

Now provide your predictions in the exact JSON format specified above.
"""
    prompt = pre_prompt+date_prompt+search_prompt+history_prompt+end_prompt
    return prompt


def llm_predict_hdb_func(engine, llm, from_date: str, to_date: str, plan_area=None, blk_no=None, street=None,
                         flat_model=None, flat_type=None, storey_range=None,
                         floor_area_sqm_from=None, floor_area_sqm_to=None,
                         lease_commence_date_from=None, lease_commence_date_to=None):
    # First get the historical data and search conditions
    search_conditions, hdb_price_history = get_llm_predict_hdb_info(
        engine,
        plan_area=plan_area,
        flat_type=flat_type,
        blk_no=blk_no,
        street=street,
        storey_range=storey_range,
        floor_area_sqm_from=floor_area_sqm_from,
        floor_area_sqm_to=floor_area_sqm_to,
        flat_model=flat_model,
        lease_commence_date_from=lease_commence_date_from,
        lease_commence_date_to=lease_commence_date_to
    )

    prompt = get_llm_predict_hdb_prompt(from_date, to_date, search_conditions, hdb_price_history)

    ans = call_llm(prompt, llm)
    ans = ans.content

    try:
        import json
        import pandas as pd
        predictions = json.loads(ans)
        df = pd.DataFrame(predictions)
        df = df.sort_values('month')

        return df

    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        print(f"LLM response was: {ans}")
        raise ValueError("Failed to parse LLM prediction response")
