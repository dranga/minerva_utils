import urllib, urllib2, cookielib
import StringIO

class MinervaConnect(object):
	
	val_url = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_ValLogin' #validation URL
	shed_url = 'https://horizon.mcgill.ca/pban1/bwskfshd.P_CrseSchd?start_date_in='

	def __init__(self, username, password):

		self.username = username
		self.password = password

		#cookie handling
		self.cj = cookielib.CookieJar()
		self.val_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

	def Login(self):
		login_data = urllib.urlencode({'sid' : self.username, 'PIN' : self.password})
		self.val_opener.addheaders.append(('Cookie', 'TESTID=set'))
		self.val_opener.open(self.val_url, login_data)

	def OpenValidatedURL(self,url):
		transc_opener = urllib2.build_opener()
		for cookie in self.cj:
			if(cookie.name == 'SESSID'):
				transc_opener.addheaders.append(('Cookie', 'SESSID=' + cookie.value))

		return transc_opener.open(url)

	def GetSchedule(self, date):
		
		resp = self.OpenValidatedURL(self.shed_url + date)

		#schedule HTML retreived
		sched_html = StringIO.StringIO(resp.read())

		return sched_html