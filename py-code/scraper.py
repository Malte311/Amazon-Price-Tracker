import datetime
import hashlib 
import json
import os
import random
import re
import requests
import smtplib
import sys
import time
import traceback
from bs4 import BeautifulSoup
from util import log_exception


CONFIG_FILE = './config.json'
UA_FILE = './user-agents.json'
DATA_PATH = '../php-code/data/'
DATA_URLS = DATA_PATH + 'urls.json'
DATA_PAUSE =  DATA_PATH + 'pause.json'

MAIL_USER = ''
MAIL_PW = ''
MAIL_RECEIVER = ''

USER_AGENTS = []
FALLBACK_USER_AGENTS = []

PAUSE_DURATION = 1209600 # = 14 days in seconds

def check_price(url, threshold, errCount = -1):
	if errCount < 0:
		user_agent = random.choice(USER_AGENTS)
	elif errCount < len(FALLBACK_USER_AGENTS):
		user_agent = FALLBACK_USER_AGENTS[errCount]
	else:
		write_price(url, '', -1) # Mark article as not available
		raise Exception(f'No success for url "{url}".')
	
	page = requests.get(url, headers={'User-Agent': user_agent})
	soup = BeautifulSoup(page.content, 'html.parser')
	html = str(soup)
	title = ''
	price = None

	try:
		title = soup.find(id='productTitle').get_text().strip()

		try:
			queue = [soup.find(text='Preis:').find_next(class_='a-color-price')]
		except Exception:
			queue = []
		finally:
			queue.extend(soup.find_all(class_='a-color-price'))
		
		for p in queue:
			if p is None:
				continue

			p = p.get_text().strip()
			if 'Derzeit nicht verfügbar' in p: # 'Currently not available'
				write_price(url, title, -1) # Mark article as not available
				return

			if html.index(title) < html.index(p) and '€' in p and 'Preis' not in p:
				price = p
				break
		
		if price is not None:
			price = price.replace('€', '').replace('.', '').replace(',', '.').strip()
			price = float(re.sub(r'[^0-9.]', '', price).strip())
			write_price(url, title, price)
		else:
			write_price(url, title, -1) # Mark article as not available

		if price <= threshold:
			send_notification(url, title, price)
	except Exception:
		errCount += 1
		time.sleep(random.randint(30, 90)) # wait 30-90 seconds
		check_price(url, threshold, errCount)


def write_price(url, title, price):
	if title == '' and price == -1:
		return

	file_name = DATA_PATH + str(hashlib.sha256(url.encode()).hexdigest()) + '.json'
	today = create_date()

	if not os.path.isfile(file_name):
		create_file(file_name, title, url)

	with open(file_name, 'r') as in_file:
		data = json.load(in_file)
		data[today] = {}
		data['lastupdate'] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

		if price != -1:
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

def create_date():
	now = datetime.datetime.now()
	today = f'{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}'
	return today

def is_already_done(url):
	file_name = DATA_PATH + str(hashlib.sha256(url.encode()).hexdigest()) + '.json'
	
	if not os.path.isfile(file_name):
		return False

	with open(file_name, 'r') as in_file:
		data = json.load(in_file)
		today = create_date()
		return today in data

def pause_execution(url):
	if not os.path.isfile(DATA_PAUSE):
		with open(DATA_PAUSE, 'w+') as file:
			data = {}
			json.dump(data, file, indent=4, sort_keys=True)

	with open(DATA_PAUSE, 'r') as file:
		data = json.load(file)
		data[url] = int(time.time()) + PAUSE_DURATION

	with open(DATA_PAUSE, 'w') as file:
		json.dump(data, file, indent=4, sort_keys=True)

def is_paused(url):
	with open(DATA_PAUSE, 'r') as file:
		data = json.load(file)
		today = int(time.time())
		return url in data and data[url] >= today

def run():
	if len(sys.argv) < 2:
		exit()

	setGlobals()
	session_count = 0

	with open(DATA_URLS) as json_file:
		data = json.load(json_file)
		for d in data['urls']:
			if session_count >= int(sys.argv[1]):
				break
			try:
				if not is_already_done(d['url']) and not is_paused(d['url']):
					check_price(d['url'], d['thresh'])
					session_count += 1
					time.sleep(random.randint(30, 90)) # wait 30-90 seconds
			except Exception:
				log_exception('Exception for url "' + str(d['url']) + '":\r\n' + str(traceback.format_exc()))
				pause_execution(d['url']) # Skip this url for some time


def setGlobals():
	global MAIL_USER
	global MAIL_PW
	global MAIL_RECEIVER

	global USER_AGENTS
	global FALLBACK_USER_AGENTS

	with open(CONFIG_FILE) as config_file:
		data = json.load(config_file)
		MAIL_USER = data['mail-user']
		MAIL_PW = data['mail-pw']
		MAIL_RECEIVER = data['mail-receiver']

	with open(UA_FILE) as ua_file:
		data = json.load(ua_file)
		USER_AGENTS = data['USER_AGENTS']
		FALLBACK_USER_AGENTS = data['FALLBACK_USER_AGENTS']


if __name__ == '__main__':
	run()