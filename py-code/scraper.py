import datetime
import hashlib 
import json
import os
import random
import re
import requests
import smtplib
import time
from bs4 import BeautifulSoup

FALLBACK_USER_AGENTS = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
	'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'
]
USER_AGENTS = FALLBACK_USER_AGENTS
LOGFILE = 'log.txt'
MAIL_USER = ''
MAIL_PW = ''
MAIL_RECEIVER = ''

def check_price(url, threshold, errCount = -1):
	if errCount < 0:
		user_agent = random.choice(USER_AGENTS)
	elif errCount < len(FALLBACK_USER_AGENTS):
		user_agent = FALLBACK_USER_AGENTS[errCount]
	else:
		return
	
	page = requests.get(url, headers={'User-Agent': user_agent})
	soup = BeautifulSoup(page.content, 'html.parser')
	title = ''
	price = 0

	try:
		title = soup.find(id='productTitle').get_text().strip()
		price = soup.find(class_='a-color-price').get_text().replace('€', '').replace(',', '.').strip()
		price = float(re.sub(r'[^0-9.]', '', price).strip())

		write_price(url, title, price)

		if price <= threshold:
			send_notification(url, title, price)
	except Exception as e:
		errCount += 1
		check_price(url, threshold, errCount)
		raise Exception(f'Error for url "{url}" with title "{title}" and price "{price}":\r\n{e}')


def write_price(url, title, price):
	now = datetime.datetime.now()
	file_name = './data/' + str(hashlib.sha256(url.encode()).hexdigest()) + '.json'
	today = f'{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}'

	if not os.path.isfile(file_name):
		create_file(file_name, title, url)

	with open(file_name, 'r') as in_file:
		data = json.load(in_file)
		data[today] = {}
		data[today]['price'] = price

	with open(file_name, 'w') as out_file:
		json.dump(data, out_file, indent=4, sort_keys=True)


def create_file(file_name, title, url):
	with open(file_name, 'w+') as file:
		data = {}
		data['title'] = title
		data['url'] = url
		json.dump(data, file, indent=4, sort_keys=True)


def send_notification(url, title, price):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(MAIL_USER, MAIL_PW)
	msg = f'Subject: Amazon price fell down\n\nYou can buy {title} for {price}€ now on {url}.'.encode('utf-8')
	server.sendmail(MAIL_USER, MAIL_RECEIVER, msg)
	server.quit()


def run():
	global MAIL_USER
	global MAIL_PW
	global MAIL_RECEIVER
	global USER_AGENTS
	global FALLBACK_USER_AGENTS

	with open('./config.json') as config_file:
		data = json.load(config_file)
		MAIL_USER = data['mail-user']
		MAIL_PW = data['mail-pw']
		MAIL_RECEIVER = data['mail-receiver']

	with open('./user-agents.json') as ua_file:
		data = json.load(ua_file)
		if data['FALLBACK_USER_AGENTS']:
			FALLBACK_USER_AGENTS = data['FALLBACK_USER_AGENTS']
		if data['USER_AGENTS']:
			USER_AGENTS = data['USER_AGENTS']

	with open('./data/urls.json') as json_file:
		data = json.load(json_file)
		for d in data['urls']:
			try:
				check_price(d['url'], d['thresh'])
			except Exception as e:
				log_exception(e)


def log_exception(e):
	if not os.path.isfile(LOGFILE):
		with open(LOGFILE, 'w+') as file:
			file.write(str(e) + '\r\n')
	else:
		with open(LOGFILE, 'a') as file:
			file.write(str(e) + '\r\n')


run()