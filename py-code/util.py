import datetime
import os

LOGFILE = 'log.txt'

def log_exception(e):
	ts = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

	if not os.path.isfile(LOGFILE):
		with open(LOGFILE, 'w+') as file:
			file.write(ts + '\r\n' + str(e) + '\r\n')
	else:
		with open(LOGFILE, 'a') as file:
			file.write(ts + '\r\n' + str(e) + '\r\n')