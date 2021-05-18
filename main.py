from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

data_manager = DataManager()
flightsearch = FlightSearch()
flightdata = FlightData()
notif_manager = NotificationManager()

sheet_data = data_manager.receive_data()

for element in sheet_data:
	if element[1] == "":
		iata_code = flightsearch.iata_search(element[0])
		element[1] = iata_code
	else:
		pass

mail_list = data_manager.send_list()

data_manager.update_iatacodes()


for city in sheet_data:
	flight_info = flightdata.search_deals(city[1])
	print(flight_info)

	if flight_info[0] < int(city[2])*2:
		# notif_manager.send_notification(flight_info[1])
		for email in mail_list:
			notif_manager.send_mails(email_to=email, message_body=flight_info[1], link=flight_info[2])


