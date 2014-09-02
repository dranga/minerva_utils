import StringIO
import re

#need to add right css
#need to add label for dashed minor lines
#need to add width for th.ddheader lines (w/ hours)

#need to add condition for dashed or no minor 
	
def parseHtml(lineList, weekends, color):
#inline css syle
#show gridlines and color cells
	html_start = """
<html>
<style type="text/css">

th.ddheader {
background-color: """+ color +""";
color: black;
font-family: Verdana,Arial Narrow,  helvetica, sans-serif;
font-weight: bold;
font-size: 90%;
font-style: normal;
text-align: left;
vertical-align: top;
padding-top: 1px;
padding-left: 1px;
border: 1px solid #000;
border-collapse:collapse;
}

th.ddlabel {
background-color: """+ color +""";
color: black;
font-family: Verdana,Arial Narrow,  helvetica, sans-serif;
font-weight: bold;
font-size: 90%;
font-style: normal;
text-align: left; 
vertical-align: top;
padding-top: 1px;
padding-left: 1px;
border: 1px solid #000;
border-collapse:collapse;
}

td.ddlabel {
background-color: """+ color +""";
color: black;
font-family: Verdana,Arial Narrow,  helvetica, sans-serif;
font-weight: bold;
font-size: 90%;
font-style: normal;
text-align: left;
vertical-align: top;
padding-top: 1px;
padding-left: 1px;
border: 1px solid #000;
border-collapse:collapse;
}

td.dddefault {
color: black;
font-family: Verdana,Arial Narrow,  helvetica, sans-serif;
font-weight: normal;
font-size: 90%;
font-style: normal;
text-align: left;
vertical-align: top;
padding-top: 1px;
padding-left: 1px;
border: 1px solid #000;
/*border: 0px solid #000;
border-right: 1px solid #000;*/
border-collapse:collapse;
}
/*
tr {
	border: 0px solid #000;
	border-top: 1px dashed #000;
}

tr.ddlabel {
	border-top: 1px solid #000;
}
*/
table.datadisplaytable {
	border: 1px solid #000;
border-collapse:collapse;
}
</style>
"""

	sched_fixed = list()
	sched_fixed.append(html_start)
	match_found = False

	for line in lineList :
		#if beginning of schedule table or inside the table keep going otherwise go to next itteration
		if(not(re.search('<TABLE.*This layout table is used to present the weekly course schedule.*>', line) or match_found == True)) : continue
		
		match_found = True
		
		#if line is end of row, remove previous 2 elements (removing saturday and sunday)
		if(re.search('<\/TR>',line) and  not weekends):
			sched_fixed.pop()
			sched_fixed.pop()
		
		#modify course block
		if(re.search('CLASS="ddlabel', line)):
			line = re.sub('<A HREF=".*">','',line) #remove link
			line = re.sub('([A-Z]{4} \d{3}-\d{3}<BR>).*<BR>(.*<BR>)',r'\1\2',line) #remove some less useful information (keep course code, times, location)
		
		#line is to be written to the output file (valid line)
		sched_fixed.append(line)
		
		#if the line is the end of the schedule table
		if(re.search('<\/TABLE>',line) and match_found == True) : break
		
	sched_fixed.append("</html>")

	return sched_fixed

def ScheduleToPDF(fo, linelist):

	import ho.pisa as pisa 

	sched_pdf = list()
	
	for line in lineList :
		if(re.search('<TH ROWSPAN="4" CLASS="ddlabel"', line)):
			line = line + ' width="42px"'

		sched_pdf.append(line)

	linelist_fixed = "".join(sched_pdf)

	pisa.pisaDocument(linelist_fixed,fo) #write the modified transcript to the output file