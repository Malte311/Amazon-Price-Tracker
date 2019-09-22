import datetime
import json
import os
import re
import requests
import smtplib
import time
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

def check_price(url, threshold):
	page = requests.get(url, headers=HEADERS)
	soup = BeautifulSoup(page.content, 'html.parser')

	title = soup.find(id='productTitle').get_text().strip()
	price = soup.find(class_='a-color-price').get_text().replace('€', '').strip()
	price = float(price.replace(',', '.'))

	write_price(url, title, price)

	if price <= threshold:
		send_notification(url, title, price)


def write_price(url, title, price):
	now = datetime.datetime.now()
	file_name = re.sub('[^a-zA-Z0-9]', '_', title).lower() + '.json'
	today = f'{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}'

	with open(file_name, 'w+') as out_file:
		if os.stat(file_name).st_size == 0:
			data = {}
			data[today] = {}
		else:
			with open(file_name, 'r') as in_file:
				data = json.load(in_file)
		
		data[today]['url'] = url
		data[today]['title'] = title
		data[today]['price'] = price
	
		json.dump(data, out_file, indent=4, sort_keys=True)


def send_notification(url, title, price):
	print ('send notification')


def run():
	with open('urls.json') as json_file:
		data = json.load(json_file)
		for url in data['urls']:
			check_price(url)


#run()