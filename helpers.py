import requests, os, shutil, stat, struct

def getPathDriver(config, sys_platform):
	CURRENT_WKD = os.getcwd()
	print ('CURRENT_WKD', CURRENT_WKD)
	paths = {}

	bit_system = struct.calcsize("P") * 8

	# handle chrome
	if config['CHROME'].getboolean('USE_CHROME') and config['CHROME']['CHROME_GECKODRIVER_LOCATION'] == 'None':
		if sys_platform == 'linux':
			driver_url = config['CHROME']['linux64']
		elif sys_platform == 'macos':
			driver_url = config['CHROME']['macos']
		elif sys_platform == 'windows':
			driver_url = config['CHROME']['windows']

		path_to_driver = downloadAndExtract(driver_url, 'chromedriver')

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

		path_to_driver = downloadAndExtract(driver_url, 'geckodriver')


	elif config['FIREFOX'].getboolean('USE_FIREFOX') and config['FIREFOX']['FIREFOX_GECKODRIVER_LOCATION']:
		path_to_driver = config['FIREFOX']['FIREFOX_GECKODRIVER_LOCATION']
	else:
		path_to_driver = False

	paths['firefox'] = path_to_driver

	return paths


# Download and extract a browser driver archive
def downloadAndExtract(url, driver_name):
	arc_path = os.path.join(os.getcwd(), url.split('/')[-1])

	driver_dir = os.path.join(os.getcwd(), 'drivers')
	driver_path = os.path.join(driver_dir, driver_name)

	# Check if the driver is already present
	if not os.path.exists(driver_path):

		# Download the file
		r = requests.get(url, allow_redirects=True)
		open(arc_path, 'wb').write(r.content)
		r.close()

		# Extract the archive
		shutil.unpack_archive(arc_path, driver_dir)

		# Change permissions
		os.chmod(driver_path, stat.S_IXUSR)

		# Delete downloaded archive
		os.remove(arc_path)

	# Return the path of the driver
	return driver_path
