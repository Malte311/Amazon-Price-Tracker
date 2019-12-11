import datetime
import os

LOGFILE = 'log.txt'

def log_exception(e):
	ts = str(datetime.datetime.now())

	if not os.path.isfile(LOGFILE):
		with open(LOGFILE, 'w+') as file:
			file.write(ts + '\r\n' + str(e) + '\r\n')
	else:
		with open(LOGFILE, 'a') as file:
			file.write(ts + '\r\n' + str(e) + '\r\n')