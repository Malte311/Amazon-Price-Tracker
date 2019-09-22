import datetime
import hashlib 
import json
import os
import re
import requests
import smtplib
import subprocess
import time
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
MAIL_USER = ''
MAIL_PW = ''
MAIL_RECEIVE = ''

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
	file_name = './data/' + str(hashlib.sha256(url.encode()).hexdigest()) + '.json'
	today = f'{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}'

	with open(file_name, 'w+') as out_file:
		if os.stat(file_name).st_size == 0:
			data = {}
			data['title'] = title
			data['url'] = url
			data[today] = {}
		else:
			with open(file_name, 'r') as in_file:
				data = json.load(in_file)
		
		data[today]['price'] = price
	
		json.dump(data, out_file, indent=4, sort_keys=True)


def send_notification(url, title, price):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(MAIL_USER, MAIL_PW)
	msg = f'Subject: Amazon price fell down\n\nYou can buy {title} for {price}€ now on {url}.'.encode('utf-8')
	server.sendmail(MAIL_USER, MAIL_RECEIVE, msg)
	server.quit()


def run():
	global MAIL_USER
	global MAIL_PW
	global MAIL_RECEIVE

	with open('./config.json') as config_file:
		data = json.load(config_file)
		MAIL_USER = data['mail-user']
		MAIL_PW = data['mail-pw']
		MAIL_RECEIVE = data['mail-receive']

	with open('./data/urls.json') as json_file:
		data = json.load(json_file)
		for d in data['urls']:
			check_price(d['url'], d['thresh'])


run()