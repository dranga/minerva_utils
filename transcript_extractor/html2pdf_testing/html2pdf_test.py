#! /usr/bin/python

import ho.pisa as pisa
import re

html_file = "output.html"
pdf_file = "output_transcript.pdf"


fo_pdf = open(pdf_file, 'w')

fo_html = open(html_file, 'r')
#read lines into list
transc = fo_html.readlines()
fo_html.close()
fo_html_new = open("output_to_pdf.html", 'w')

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

#itterate through list & modify html --> add widths that fail
for line in transc:
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


fo_html_new.write(transc_fixed)
fo_html_new.close()
	
#transc_fixed = re.sub('', '', transc_fixed)

pisa.pisaDocument(transc_fixed,fo_pdf) #write the modified transcript to the output file
fo_pdf.close()
