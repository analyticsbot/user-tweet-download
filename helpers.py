import requests, os, zipfile, stat

def getPathDriver(config, sys_platform):
	CURRENT_WKD = os.getcwd()
	print ('CURRENT_WKD', CURRENT_WKD)
	paths = {}
	# handle chrome
	if config['CHROME'].getboolean('USE_CHROME') and config['CHROME']['CHROME_GECKODRIVER_LOCATION'] == 'None':
		if sys_platform == 'linux':
			driver_url = config['CHROME']['linux64']
		elif sys_platform == 'macos':
			driver_url = config['CHROME']['macos']
		elif sys_platform == 'windows':
			driver_url = config['CHROME']['windows']

		# download
		r = requests.get(driver_url, allow_redirects=True)
		open(os.path.join(CURRENT_WKD, driver_url.split('/')[-1]), 'wb').write(r.content)
		r.close()

		# unzip
		with zipfile.ZipFile(os.path.join(CURRENT_WKD, driver_url.split('/')[-1]), 'r') as zip_ref:
			zip_ref.extractall(CURRENT_WKD)
		
		path_to_driver = os.path.join(CURRENT_WKD, 'chromedriver')
		os.chmod(path_to_driver, stat.S_IXUSR)


	elif config['CHROME'].getboolean('USE_CHROME') and config['CHROME']['CHROME_GECKODRIVER_LOCATION']:
		path_to_driver = config['CHROME']['CHROME_GECKODRIVER_LOCATION']
	else:
		path_to_driver = False

	paths['chrome'] = path_to_driver
	
	# handle firefox
	if config['FIREFOX'].getboolean('USE_FIREFOX') and config['FIREFOX']['FIREFOX_GECKODRIVER_LOCATION'] == 'None':
		if sys_platform == 'linux' and bit_system == 32:
			driver_url = config['FIREFOX']['linux32']
		elif sys_platform == 'linux' and bit_system == 64:
			driver_url = config['FIREFOX']['linux64']
		elif sys_platform == 'macos':
			driver_url = config['FIREFOX']['macos']
		elif sys_platform == 'windows' and bit_system == 32:
			driver_url = config['FIREFOX']['windows32']
		elif sys_platform == 'windows' and bit_system == 64:
			driver_url = config['FIREFOX']['windows64']

		# download
		r = requests.get(driver_url, allow_redirects=True)
		open(os.path.join(CURRENT_WKD, driver_url.split('/')[-1]), 'wb').write(r.content)
		r.close()

		# unzip
		with zipfile.ZipFile(os.path.join(CURRENT_WKD, driver_url.split('/')[-1]), 'r') as zip_ref:
			zip_ref.extractall(CURRENT_WKD)
		path_to_driver = os.path.join(CURRENT_WKD, 'geckodriver')
		os.chmod(path_to_driver, stat.S_IXUSR)


	elif config['FIREFOX'].getboolean('USE_FIREFOX') and config['FIREFOX']['FIREFOX_GECKODRIVER_LOCATION']:
		path_to_driver = config['FIREFOX']['FIREFOX_GECKODRIVER_LOCATION']
	else:
		path_to_driver = False

	paths['firefox'] = path_to_driver

	return paths