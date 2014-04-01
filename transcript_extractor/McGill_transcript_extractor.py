#! /usr/bin/python

import urllib, urllib2, cookielib
import StringIO
import re
import sys

#version check
#if not(sys.version_info.major > 2 or (sys.version_info.major >= 2 and sys.version_info.minor >= 7)) :
#	print "Transcript extractor requires  python 2.7 or greater to parse input arguments"
#	sys.exit(0)
	
try:
	import getpass
except ImportError:
	sys.exit("Transcript extractor requires getpass module to run, It is unavailable on this system");

try:
	import argparse
except ImportError:
	sys.exit("Transcript extractor requires argparse module to run, It is unavailable on this system");

nopdf = False

try:
	import ho.pisa as pisa 
except ImportError:
	print("PDF generation module pisa is required to generate a final pdf. It is unavailable on this system")
	nopdf = True

#if argparse is unavailable, manual input
#username = sys.argv[1]
#password = sys.argv[2]
#output_file = sys.argv[3]

#argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("email", help = "McGill email")
parser.add_argument("output_file", help = "File to write to (e.g. output.html)")
parser.add_argument("--html", help = "Keep generated html (default: False, unless PDF generation module is unavailable)")
parser.add_argument("--nopdf", help = "Do not generate a final PDF, keep html only(default: False, unless PDF module is unavailable)",  action="store_true")
args = parser.parse_args()

username = args.email
output_file = args.output_file
nopdf = nopdf or args.nopdf
html_file = args.html

#prompt for password
password = getpass.getpass("McGill Password: ")

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

#fo.write(html_start)

transc_fixed = list()
transc_fixed.append(html_start)
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
		

transc_fixed.append("</html>")

if(nopdf or not (html_file is None)):
	fo = open(html_file, 'w')
	fo.write("".join(transc_fixed)) #write the modified transcript to the output file
	fo.close()

if(not nopdf):

	toPDF(fo_pdf, linelist)
	#ok but ends up scrunched up 
	#fix w/ reduce colspan = "11" to colspan = "8"
	#transc_fixed = re.sub('COLSPAN="11"','COLSPAN="8"',"".join(transc_fixed))
	#didn't help :(

	#it was pointed out that Points doesn't have WIDTH attribute, that might cause it to be tiny
	#also Title column doesn't have a set width 

	#Soln : fix the width
	transc_fixed = "".join(transc_fixed)
	
	transc_fixed = re.sub('<TD NOWRAP', '<TD COLSPAN="1"', transc_fixed)
	#transc_fixed = re.sub('<TD CLASS="delabel" scope="row" ><p class="centeraligntext"><SPAN class=fieldmediumtextbold>Title</SPAN></TD>',
	#						'<TD COLSPAN="3" CLASS="delabel" scope="row" ><p class="centeraligntext"><SPAN class=fieldmediumtextbold>Title</SPAN></TD>',
	#						transc_fixed)

	fo = open(html_file, 'w')
	fo.write(transc_fixed) #write the modified transcript to the output file
	fo.close()

	fo = open(output_file, 'w')
	pisa.pisaDocument(transc_fixed,fo)
	fo.close()

def toPDF(fo, linelist):
	TD = 0
	temp = []
	transc_fixed = []

	#number of columns in a "course" part of the transcript
	COL_PER_ROW = 11

	#strings to be replaced
	COURSE_STR = '<TD +CLASS="dedefault">'
	POINT_STR = '<TD CLASS="dedefault"><SPAN class=fieldmediumtext>Points</SPAN></TD>'

	#width (in px) of columns in "course" part of the transcript
	WIDTH = [ 	55,		#empty field
				100,	#course code and number
				55,		#section
				200,	#course name
				55,		#number of credits
				55,		#empty field
				55,		#letter grade earned
				55,		#empty field
				55,		#empty field
				55,		#number of credits earned
				100 ]	#average letter grade
	POINT_WIDTH = 80

	for line in linelist:
		if(TD == COL_PER_ROW):
			#from temp array change 
			#<TD CLASS="dedefault"><SPAN class=fieldmediumtext>.*</SPAN></TD>
			#to
			#<TD WIDTH="$width"CLASS="dedefault"><SPAN class=fieldmediumtext>.*</SPAN></TD>

			#$width, 11 width values in array
			for i in range(len(temp)):
				templine = temp[i]
				#add width to string
				substr = '<TD CLASS="dedefault" WIDTH="' + `WIDTH[i]` + 'px">'
				templine = re.sub(COURSE_STR, substr, templine)
				#write to array
				transc_fixed.append(templine)

			#clear variable
			temp = [];
			TD = 0

		else :
			#if TD is "right"
			#	add to temp array
			#else
			#	write to final

			if (re.search(POINT_STR,line)):
				#print("FOUND POINT LINE")
				#append anything in temp into transc_fixed
				line = '<TD CLASS="dedefault" WIDTH="'+ `POINT_WIDTH` + 'px"><SPAN class=fieldmediumtext>Points</SPAN></TD>'
				transc_fixed.extend(temp)
				transc_fixed.append(line)
				temp = []
				TD = 0
			elif (re.search(COURSE_STR,line)):
				temp.append(line)
				TD += 1
			else :
				#append anything in temp into transc_fixed
				transc_fixed.extend(temp)
				transc_fixed.append(line)
				temp = []
				TD = 0

	transc_fixed = "".join(transc_fixed)

	return transc_fixed