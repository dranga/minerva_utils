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

color = "lightgray"

#if argparse is unavailable, manual input
#username = sys.argv[1]
#password = sys.argv[2]
#output_file = sys.argv[3]
#date = sys.argv[4]

#argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("email", help = "McGill email (e.g. john.doe0@mail.mcgill.ca")
parser.add_argument("output_file", help = "File to write to (e.g. output.html)")
parser.add_argument("weekof", help = "Schedule for specific week mm/dd/yyyy")
parser.add_argument("-c","--color", help = "Highlight color (any css valid color, e.g. '-c red' or '-c #f00'). default: lightgray") 
parser.add_argument("-w","--weekend", help = "display weekends (default : off)", action="store_true")
args = parser.parse_args()

username = args.email
output_file = args.output_file
date = args.weekof
color = args.color or color #overwrite default if available
weekends = True if args.weekend else False


#prompt for password
password = getpass.getpass("McGill Password: ")

fo = open(output_file, 'w')

#inline css syle
#show gridlines and color cells
html_style = """
<html>
<style type="text/css">
table{
border-collapse:collapse;
border:1px solid #000;
}
table td{
border:1px solid #000;
}
.ddlabel { background-color: """+ color +""";}
 </style>
"""

val_url = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_ValLogin' #validation URL
shed_url = 'https://horizon.mcgill.ca/pban1/bwskfshd.P_CrseSchd?start_date_in=' + date #schedule URL
#cookie handling
cj = cookielib.CookieJar()
val_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

#login with provided data
login_data = urllib.urlencode({'sid' : username, 'PIN' : password})
val_opener.addheaders.append(('Cookie', 'TESTID=set'))
val_opener.open(val_url, login_data)

#do some cookie magic to get schedule
shed_opener = urllib2.build_opener()
for cookie in cj:
	if(cookie.name == 'SESSID'):
		shed_opener.addheaders.append(('Cookie', 'SESSID=' + cookie.value))

resp = shed_opener.open(shed_url)

#schedule HTML retreived
shed_html = StringIO.StringIO(resp.read())

fo.write(html_style) #write css into output

shed_fixed = list()
match_found = False

for line in shed_html :
	#if beginning of schedule table or inside the table keep going otherwise go to next itteration
	if(not(re.search('<TABLE.*This layout table is used to present the weekly course schedule.*>', line) or match_found == True)) : continue
	
	match_found = True
	
	#if line is end of row, remove previous 2 elements (removing saturday and sunday)
	if(re.search('<\/TR>',line) and  not weekends):
		shed_fixed.pop()
		shed_fixed.pop()
	
	#modify course block
	if(re.search('CLASS="ddlabel', line)):
		line = re.sub('<A HREF=".*">','',line) #remove link
		line = re.sub('([A-Z]{4} \d{3}-\d{3}<BR>).*<BR>(.*<BR>)',r'\1\2',line) #remove some less useful information (keep course code, times, location)
	
	#line is to be written to the output file (valid line)
	shed_fixed.append(line)
	
	#if the line is the end of the schedule table
	if(re.search('<\/TABLE>',line) and match_found == True) : break
	
		
fo.write("".join(shed_fixed)) #write the modified shedule to the output file
fo.write("</html>")
fo.close()
