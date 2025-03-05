from .get_onemap_auth import AUTH
import requests


def get_api_result_func(url: str):
    url="https://www.onemap.gov.sg"+url
    # Replace with your actual API token
    headers = {
        "Authorization": AUTH}

    # Make the request
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Convert JSON response to a dictionary
        result_dict = response.json()
        print(result_dict)
        print(type(result_dict))
        return result_dict
    else:
        # Handle the error case
        print(f"Failed to retrieve data: {response.status_code}")
        return None


if __name__ == "__main__":
    get_api_result_func("https://www.onemap.gov.sg/api/public/popapi/getEconomicStatus?planningArea=Bedok&year=2010&gender=male")
