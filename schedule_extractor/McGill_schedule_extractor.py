#! /usr/bin/python

import sys

from MinervaConnect import MinervaConnect
import ScheduleMods


#version check
#if not(sys.version_info.major > 2 or (sys.version_info.major >= 2 and sys.version_info.minor >= 7)) :
#	print "Schedule extractor requires  python 2.7 or greater to parse input arguments"
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

defaultColor = "lightgray"
defaultName_html = "output.html"
defaultName_pdf = "output.pdf"

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
parser.add_argument("--html", help = "Keep generated html (default: False, unless PDF generation module is unavailable)")
parser.add_argument("--nopdf", help = "Do not generate a final PDF, keep html only(default: False, unless PDF module is unavailable)",  action="store_true")
args = parser.parse_args()

username = args.email
output_file = args.output_file
date = args.weekof
color = args.color or defaultColor #overwrite default if available
nopdf = nopdf or args.nopdf
html_file = args.html
weekends = True if args.weekend else False


#prompt for password
password = getpass.getpass("McGill Password: ")

minervaInst = MinervaConnect(username, password)

minervaInst.Login()

sched_fixed = ScehduleMods.parseHtml(MinervaInst.getSchedule(date), weekends, color)

#generate html
if(nopdf or not (output_file is None)):
	if (html_file is None):
		html_file = defaultName_html
	fo = open(html_file, 'w')
	fo.write("".join(sched_fixed)) #write the modified transcript to the output file
	fo.close()


#generate pdf
if(not nopdf):

	fo = open(output_file, 'w')
	ScehduleMods.ScheduleToPDF(fo, sched_fixed)
	fo.close()