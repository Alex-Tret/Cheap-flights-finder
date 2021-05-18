import requests
import datetime
from pprint import pprint

data = [{'city': 'Paris', 'iataCode': 'PAR', 'id': 2, 'lowestPrice': 54},
 {'city': 'Berlin', 'iataCode': 'BER', 'id': 3, 'lowestPrice': 42},
 {'city': 'Tokyo', 'iataCode': 'TYO', 'id': 4, 'lowestPrice': 485},
 {'city': 'Sydney', 'iataCode': 'SYD', 'id': 5, 'lowestPrice': 551},
 {'city': 'Istanbul', 'iataCode': 'IST', 'id': 6, 'lowestPrice': 95},
 {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'id': 7, 'lowestPrice': 414},
 {'city': 'New York', 'iataCode': 'NYC', 'id': 8, 'lowestPrice': 240},
 {'city': 'San Francisco', 'iataCode': 'SFO', 'id': 9, 'lowestPrice': 260},
 {'city': 'Cape Town', 'iataCode': 'CPT', 'id': 10, 'lowestPrice': 378}]

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
APIKEY = "2hlqBPbmYKQPHuo2eo4s-XuQS_arXKY1"

class FlightData:


	def __init__(self):
		self.fly_from = "LON"
		self.fly_to = ''
		self.date_from = ''
		self.date_to = ''
		self.nights_in_dst_from = 7
		self.nights_in_dst_to = 28
		self.flight_type = "round"
		self.adults = 1
		self.infants = 0
		self.curr = "GBP"
		self.max_stopovers = "0"
		self.vehicle_type = "aircraft"


	def search_deals(self, destination):
		tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
		max_return = tomorrow + datetime.timedelta(days=180)
		self.date_from = tomorrow.strftime("%d/%m/%Y")
		self.date_to = max_return.strftime("%d/%m/%Y")

		params = {
			"fly_from": self.fly_from,
			"fly_to": destination,
			"date_from": self.date_from,
			"date_to": self.date_to,
			"nights_in_dst_from": self.nights_in_dst_from,
			"nights_in_dst_to": self.nights_in_dst_to,
			"flight_type": self.flight_type,
			"adults": self.adults,
			"infants": self.infants,
			"curr": self.curr,
			 "one_for_city": 1,
			"max_stopovers": self.max_stopovers,
		}
		header = {
			"apikey": APIKEY,
			"accept": "application/json"
		}

		response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=params, headers=header)

		try:
			data = response.json()['data'][0]
			# print(data)
		except IndexError:

			params["max_stopovers"] = "2"
			# print(params)
			response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=params, headers=header)
			data = response.json()['data'][0]
			# pprint(data)
			message = f"Low price alert! Only £{data['price']} to fly from {data['cityFrom']}-{data['flyFrom']} to {data['cityTo']}-{data['flyTo']} " \
					  f"from {data['local_arrival'][:10]} to {data['route'][1]['local_arrival'][:10]}. Flight has stopover, via {data['route'][1]['cityFrom']} "
			link = f"https://www.google.co.uk/flights?hl=en#flt={data['flyFrom']}.{data['flyTo']}.{data['local_arrival'][:10]}*" \
					   f"{data['flyTo']}.{data['flyFrom']}.{data['route'][1]['local_arrival'][:10]}"
			flight_data = (data['price'], message, link)
			return flight_data
		else:
			message = f"Low price alert! Only £{data['price']} to fly from {data['cityFrom']}-{data['flyFrom']} to {data['cityTo']}-{data['flyTo']} " \
					  f"from {data['local_arrival'][:10]} to {data['route'][1]['local_arrival'][:10]}."
			link = f"https://www.google.co.uk/flights?hl=en#flt={data['flyFrom']}.{data['flyTo']}.{data['local_arrival'][:10]}*" \
					   f"{data['flyTo']}.{data['flyFrom']}.{data['route'][1]['local_arrival'][:10]}"
			flight_data = (data['price'], message, link)
			return flight_data




