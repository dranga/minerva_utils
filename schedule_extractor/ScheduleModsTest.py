#! /usr/bin/python

import ScheduleMods

inputFile = 'input_sched.html'
outputFile = 'output_sched.html'
outputPdfFile = 'output_sched.pdf'

testHtml = False
testPdf = True

if(testHtml):

	fi = open(inputFile, 'r')
	sched = fi.readlines()
	fi.close()

	weekends = False
	color = "lightgray"

	sched_fixed_output = ScheduleMods.parseHtml(sched, weekends, color)

	fo = open(outputFile, 'w')
	fo.write("".join(sched_fixed_output)) #write the modified transcript to the output file
	fo.close()

if(testPdf):

	fi = open(outputFile, 'r')
	sched = fi.readlines()
	fi.close()

	fo  = open(outputPdfFile, 'w')

	ScheduleMods.ScheduleToPDF(fo, sched)

	fo.close()
