import StringIO
import re
	
def parseHtml(lineList):
	html_start = """
<html>
<TITLE>UNOFFICIAL Transcript for ID </TITLE>
"""

	transc_fixed = list()
	transc_fixed.append(html_start)
	match_found = 0
	count = 0

	for line in lineList :
		
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

	return transc_fixed

def toPDF(fo, linelist):

	import ho.pisa as pisa 
	TD = 0
	temp = []
	transc_fixed = []

	#number of columns in a "course" part of the transcript
	COL_PER_ROW = 11

	#strings to be replaced
	COURSE_STR = '<TD +NOWRAP +CLASS="dedefault">'
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

			#print "CHANGING WIDTH"
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
				#print "FOUND COURSE LINE", TD
			else :
				#print ">>", line, "<<"
				#append anything in temp into transc_fixed
				transc_fixed.extend(temp)
				transc_fixed.append(line)
				temp = []
				TD = 0

	transc_fixed = "".join(transc_fixed)

	#for debugging
	#fo_html_new = open("output_to_pdf.html", 'w')
	#fo_html_new.write(transc_fixed)
	#fo_html_new.close()

	pisa.pisaDocument(transc_fixed,fo) #write the modified transcript to the output file