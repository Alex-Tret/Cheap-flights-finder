import requests
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
APIKEY = "2hlqBPbmYKQPHuo2eo4s-XuQS_arXKY1"

class FlightSearch:
    def __init__(self):
        self.search = None
        self.city = ""

    def iata_search(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city",
            "limit": 1,

        }
        header = {
            "apikey": APIKEY
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query",
                                params=params,
                                headers=header)
        data = response.json()
        city_code = data['locations'][0]['code']

        return city_code
