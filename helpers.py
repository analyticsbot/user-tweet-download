import requests, os, zipfile, stat

def getPathDriver(config, sys_platform):
	CURRENT_WKD = os.getcwd()
	print ('CURRENT_WKD', CURRENT_WKD)
	paths = {}
	# handle chrome
	if config['CHROME'].getboolean('USE_CHROME') and config['CHROME']['CHROME_GECKODRIVER_LOCATION'] == 'None':
		print (1)
		if sys_platform == 'linux':
			driver_url = config['CHROME']['linux64']
			print (11)
		elif sys_platform == 'macos':
			driver_url = config['CHROME']['macos']
			print (12)
		elif sys_platform == 'windows':
			driver_url = config['CHROME']['windows']
			print (13)

		# download
		r = requests.get(driver_url, allow_redirects=True)
		print (14)
		open(os.path.join(CURRENT_WKD, driver_url.split('/')[-1]), 'wb').write(r.content)
		print (15)
		r.close()
		print (16)

		# unzip
		with zipfile.ZipFile(os.path.join(CURRENT_WKD, driver_url.split('/')[-1]), 'r') as zip_ref:
			zip_ref.extractall(CURRENT_WKD)
		print (17)
		
		path_to_driver = os.path.join(CURRENT_WKD, 'chromedriver')
		print (18)
		os.chmod(path_to_driver, stat.S_IXUSR)


	elif config['CHROME'].getboolean('USE_CHROME') and config['CHROME']['CHROME_GECKODRIVER_LOCATION']:
		path_to_driver = config['CHROME']['CHROME_GECKODRIVER_LOCATION']
		print (19)
	else:
		path_to_driver = False
		print (20)

	paths['chrome'] = path_to_driver
	print (21)
	
	# handle firefox
	if config['FIREFOX'].getboolean('USE_FIREFOX') and config['FIREFOX']['FIREFOX_GECKODRIVER_LOCATION'] == 'None':
		if sys_platform == 'linux' and bit_system == 32:
			driver_url = config['FIREFOX']['linux32']
			print (211)
		elif sys_platform == 'linux' and bit_system == 64:
			driver_url = config['FIREFOX']['linux64']
			print (212)
		elif sys_platform == 'macos':
			driver_url = config['FIREFOX']['macos']
			print (213)
		elif sys_platform == 'windows' and bit_system == 32:
			driver_url = config['FIREFOX']['windows32']
			print (214)
		elif sys_platform == 'windows' and bit_system == 64:
			driver_url = config['FIREFOX']['windows64']
			print (215)

		# download
		r = requests.get(driver_url, allow_redirects=True)
		open(os.path.join(CURRENT_WKD, driver_url.split('/')[-1]), 'wb').write(r.content)
		r.close()
		print (216)

		# unzip
		with zipfile.ZipFile(os.path.join(CURRENT_WKD, driver_url.split('/')[-1]), 'r') as zip_ref:
			zip_ref.extractall(CURRENT_WKD)
		path_to_driver = os.path.join(CURRENT_WKD, 'geckodriver')
		os.chmod(path_to_driver, stat.S_IXUSR)

		print (217)

	elif config['FIREFOX'].getboolean('USE_FIREFOX') and config['FIREFOX']['FIREFOX_GECKODRIVER_LOCATION']:
		path_to_driver = config['FIREFOX']['FIREFOX_GECKODRIVER_LOCATION']
		print (218)
	else:
		path_to_driver = False

	paths['firefox'] = path_to_driver

	return paths