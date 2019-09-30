import json
import requests
import sys
from bs4 import BeautifulSoup


BASE_URL = 'https://developers.whatismybrowser.com/useragents/explore/software_name/'
BROWSERS = [
	'chrome/',
	'firefox/',
	'internet-explorer/',
	'opera/',
	'safari/'
]
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
FILE = './user-agents.json'


def run():
	if len(sys.argv) > 1:
		switch(str(sys.argv[1]))
	else:
		run_all()


def run_all():
	for browser in BROWSERS:
		get_user_agents(BASE_URL + browser)


def switch(arg):
	browser = ''
	if arg == '--chrome':
		browser = BROWSERS[0]
	elif arg == '--firefox':
		browser = BROWSERS[1]
	elif arg == '--ie':
		browser = BROWSERS[2]
	elif arg == '--opera':
		browser = BROWSERS[3]
	elif arg == '--safari':
		browser = BROWSERS[4]

	if browser != '':
		get_user_agents(BASE_URL + browser)


def get_user_agents(url):
	page = requests.get(url, headers=HEADERS)
	soup = BeautifulSoup(page.content, 'html.parser')

	table = soup.find_all(class_='useragent')
	table = filter(is_not_none, table)

	agents = []
	for agent in table:
		if agent.get_text().strip().lower() != 'user agent':
			agents.append(agent.get_text().strip())
	
	update_user_agents(FILE, agents)


def is_not_none(element):
	return not (element is None)


def update_user_agents(file, agents):
	with open(file, 'r') as in_file:
		data = json.load(in_file)
		for agent in agents:
			if agent not in data['USER_AGENTS']:
				data['USER_AGENTS'].append(agent)

	with open(file, 'w') as out_file:
		json.dump(data, out_file, indent=4, sort_keys=True)


run()