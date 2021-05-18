# SHETTY_ENDPOINT = "https://api.sheety.co/3f42fccabe16677986b39a272775566e/flightDeals/prices"
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'mypython.json'  # имя файла с закрытым ключом

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
															   ['https://www.googleapis.com/auth/spreadsheets',
																'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


class DataManager:
	def __init__(self):
		self.credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
															   ['https://www.googleapis.com/auth/spreadsheets',
																'https://www.googleapis.com/auth/drive'])
		self.httpAuth = credentials.authorize(httplib2.Http())
		self.service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
		self.spreadsheetId = '1DBpCp6UyPTOx2oQhc7A734u9Y9Wm8vW1VM0yuIN-dXg'
		self.sheet_update = []

	def receive_data(self):
		"""Read the data from the sheet"""
		range_name = 'prices!A1:C'
		table = service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=range_name).execute()
		self.destination_data = table['values'][1:]
		return self.destination_data


	def update_iatacodes(self):
		for element in self.destination_data:
			self.sheet_update.append(element[1])
		range_update = f'prices!B2:B{len(self.sheet_update)+1}'
		self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId,
													body={
														"valueInputOption": "USER_ENTERED",
														"data": [
															{"range": range_update,
															 "majorDimension": "COLUMNS",
															 "values": [self.sheet_update]}

														]
													}).execute()

	def send_list(self):
		range_name = 'users!A1:C'
		table = service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=range_name).execute()
		users = table['values'][1:]
		users_list = [element[2] for element in users]
		return users_list
# responce = requests.get("https://api.sheety.co/3f42fccabe16677986b39a272775566e/flightDeals/prices")
# result = responce.json()
# responce.raise_for_status()
# print(responce.text)
