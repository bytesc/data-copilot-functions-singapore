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

        columns = result.keys()
        return [dict(zip(columns, row)) for row in result]

    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()


def query_latest_month(engine):
    conn = engine.connect()
    try:
        # 查询最大的month值（最新日期）
        query = "SELECT MAX(month) AS latest_month FROM resale_flat_prices"
        result = conn.execute(sqlalchemy.text(query))
        latest_month = result.scalar()
        return latest_month

    except Exception as e:
        print(f"Error querying latest month: {e}")
        raise e
    finally:
        conn.close()


def get_llm_predict_hdb_info(engine, plan_area=None, flat_type=None, blk_no=None,
                             street=None, storey_range=None, floor_area_sqm_from=None,
                             floor_area_sqm_to=None, flat_model=None,
                             lease_commence_date_from=None, lease_commence_date_to=None):

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

    # Format month to YYYY-MM and sort chronologically
    for record in hdb_price_history:
        if 'month' in record and record['month']:
            if isinstance(record['month'], str):
                try:
                    from datetime import datetime
                    dt = datetime.strptime(record['month'], '%Y-%m-%d')
                    record['month'] = dt.strftime('%Y-%m')
                except ValueError:
                    pass
            else:
                record['month'] = record['month'].strftime('%Y-%m')
    hdb_price_history = sorted(hdb_price_history, key=lambda x: x['month'])
    averaged_data = []
    sampled_data = None

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

        # Create averaged data
        averaged_data = []
        for month, data in monthly_data.items():
            avg_price = data['total_price'] / data['count']
            result_record = {
                'month': month,
                'avg_resale_price': avg_price,
                'original_count': data['count']
            }
            averaged_data.append(result_record)

        if len(averaged_data) > 50:
            sampled_data = []
            for record in averaged_data:
                month = record['month']
                # Check for Q1, Q2, Q3, Q4 months (Jan, Apr, Jul, Oct)
                if month.endswith(('-01', '-04', '-07', '-10')):
                    sampled_data.append(record)

            return search_conditions, hdb_price_history, sampled_data

        return search_conditions, hdb_price_history, averaged_data  # sampled_data is None when not reduced
    else:
        return search_conditions, hdb_price_history, hdb_price_history  # No averaging or sampling needed


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
4. Please consider price fluctuations and cyclical characteristics to simulate real-market scenarios, do not predict a straight line!!!
The prediction result must have unpredictable swings and irregular fluctuations!!! 
The prediction must have obvious oscillation and erratic volatility!!!

5. Return your predictions in JSON format with an array of objects, each containing:
   - "month": in "yyyy-mm" format
   - "predicted_price": as a float value
6. Only return the result json without any explanation or comments!!!

### Output Format Example:
[
    {"month": "2023-01", "predicted_price": 450000.0},
    {"month": "2023-02", "predicted_price": 452000.0},
    ...
]
# The prediction result must have unpredictable swings and irregular fluctuations!!! 
# The prediction must have obvious oscillation and erratic volatility!!!
# Only return the result json without any explanation or comments!!!
"""
    prompt = pre_prompt+date_prompt+search_prompt+history_prompt+end_prompt
    return prompt


def llm_predict_hdb_func(engine, llm, from_date: str = None, to_date: str = None,
                         plan_area=None, blk_no=None, street=None,
                         flat_model=None, flat_type=None, storey_range=None,
                         floor_area_sqm_from=None, floor_area_sqm_to=None,
                         lease_commence_date_from=None, lease_commence_date_to=None):
    # First get the historical data and search conditions
    search_conditions, hdb_price_history, sample = get_llm_predict_hdb_info(
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

    if from_date is None:
        latest_month = query_latest_month(engine).strftime("%Y-%m")
        year, month = map(int, latest_month.split('-'))
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        from_date = f"{year}-{month:02d}"

    if to_date is None:
        year, month = map(int, from_date.split('-'))
        to_date = f"{year + 1}-{month:02d}"
    else:
        from_year, from_month = map(int, from_date.split('-'))
        to_year, to_month = map(int, to_date.split('-'))
        if (to_year < from_year) or (to_year == from_year and to_month <= from_month):
            to_date = f"{from_year + 1}-{from_month:02d}"

    prompt = get_llm_predict_hdb_prompt(from_date, to_date, search_conditions, sample)
    ans = call_llm(prompt, llm)
    ans = ans.content

    try:
        import json
        import pandas as pd
        import re

        json_str = ans.strip()
        code_block_match = re.search(r'```(?:json)?\n(.*?)\n```', json_str, re.DOTALL)
        if code_block_match:
            json_str = code_block_match.group(1)
        predictions = json.loads(json_str)
        df = pd.DataFrame(predictions)
        df = df.sort_values('month')
        return df

    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        print(f"LLM response was: {ans}")
        raise ValueError("Failed to parse LLM prediction response")
