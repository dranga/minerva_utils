#! /usr/bin/python

import urllib, urllib2, cookielib
import StringIO
import re
import sys

#version check
if not(sys.version_info.major > 2 or (sys.version_info.major >= 2 and sys.version_info.minor >= 7)) :
	print "Schedule extractor requires  python 2.7 or greater to parse input arguments"
	sys.exit(0)
	

import getpass
import argparse

#if argparse is unavailable, manual input
#username = sys.argv[1]
#password = sys.argv[2]
#output_file = sys.argv[3]

#argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("email", help = "McGill email")
parser.add_argument("output_file", help = "File to write to (e.g. output.html)")
args = parser.parse_args()

username = args.email
output_file = args.output_file

#prompt for password
password = getpass.getpass("McGill Password: ")

fo = open(output_file, 'w')
html_start = """
<html>
<TITLE>UNOFFICIAL Transcript for ID </TITLE>
"""

val_url = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_ValLogin' #validation URL
transc_url = 'https://horizon.mcgill.ca/pban1/bzsktran.P_Display_Form?user_type=S&tran_type=V' #transcript URL
#cookie handling
cj = cookielib.CookieJar()
val_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

#login with provided data
login_data = urllib.urlencode({'sid' : username, 'PIN' : password})
val_opener.addheaders.append(('Cookie', 'TESTID=set'))
val_opener.open(val_url, login_data)

#do some cookie magic to get
transc_opener = urllib2.build_opener()
for cookie in cj:
	if(cookie.name == 'SESSID'):
		transc_opener.addheaders.append(('Cookie', 'SESSID=' + cookie.value))

resp = transc_opener.open(transc_url)

#transcript HTML retreived
transc_html = StringIO.StringIO(resp.read())


fo.write(html_start)

transc_fixed = list()
match_found = 0
count = 0

for line in transc_html :
	
	#start of transcript special info
	if(re.search('<SPAN.*Wingdings.*>.*<\/SPAN', line)):
		match_found = 1
		
	#line after the end of transcript special info, stop capturing
	if(re.search('^Please click', line) and match_found == 1):
		#transc_fixed.pop()
		match_found = 0
		
	#start of transcript style	
	if(re.search('<STYLE.*>', line)):
		match_found = 2
	
	#end of transcript style (needs to be captured)
	if(re.search('<\/STYLE', line) and match_found == 2):
		#transc_fixed.pop()
		transc_fixed.append(line)
		match_found = 0
	
	#start of student info
	if(re.search('<TABLE.*CLASS="student_info".*', line)):
		match_found = 3
		
	#end of student info (needs to be captured)
	if(re.search('<\/TABLE', line) and match_found == 3):
		#transc_fixed.pop()
		transc_fixed.append(line)
		match_found = 0
		
	#start of transcript
	if(re.search('<TABLE.*CLASS="main.*', line)):
		match_found = 4
		#count = 1 #start of table
	
	#while in transcript keep track of table tags
	if(match_found == 4):
		if(re.search('<TABLE.*', line)):
			count += 1
		
		elif(re.search('<\/TABLE>', line)):
			count -= 1
		
		if(count == 0): #last closing table tag needs to be captured
			match_found = 0
		
	if(match_found != 0):
		transc_fixed.append(line)
		

fo.write("".join(transc_fixed)) #write the modified transcript to the output file
fo.write("</html>")
fo.close()
