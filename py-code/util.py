import os

LOGFILE = 'log.txt'

def log_exception(e):
	if not os.path.isfile(LOGFILE):
		with open(LOGFILE, 'w+') as file:
			file.write(str(e) + '\r\n')
	else:
		with open(LOGFILE, 'a') as file:
			file.write(str(e) + '\r\n')