from twilio.rest import Client
import data
import smtplib

MY_EMAIL = data.MY_EMAIL
MY_PASSWORD = data.MY_PASSWORD

ACCOUNT_SID = data.ACCOUNT_SID
TOKEN = data.TOKEN


class NotificationManager:
	def __init__(self):
		self.from_number = "+14155295686"
		self.to_number = "+380504142724"

	def send_notification(self, message_body):
		account_sid = ACCOUNT_SID
		auth_token = TOKEN
		client = Client(account_sid, auth_token)

		message = client.messages \
			.create(
			body=message_body,
			from_=self.from_number,
			to=self.to_number
		)

		print(message.status)

	def send_mails(self, email_to, message_body, link):
		message_tosend = message_body.encode('utf-8')
		with smtplib.SMTP("smtp.gmail.com") as connection:
			connection.starttls()
			connection.login(user=MY_EMAIL, password=MY_PASSWORD)
			connection.sendmail(from_addr=MY_EMAIL,
								to_addrs=email_to,
								msg=f"Subject: Low price for flight alert\n\n{message_body}\n{link} ".encode('utf-8'))
