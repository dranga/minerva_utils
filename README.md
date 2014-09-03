minerva_utils
=============

Set of utilities to access services on Minerva, McGill University's Administrative system.


Specifically :
* /transcript_extractor : a utility to extract an up-to-date unofficial transcript from the McGill website
* /schedule_extractor : a utility to extract a week's schedule from the McGill website

__UPDATE:__ default behaviour is now to output to printable PDF for both utilities.

## Transcript Extractor
Because sometimes you need a version of your transcript handy (and waiting a couple days, walking to Service Point isn't convenient). Print screen and print page to PDF keeps all the links, the banner and in general is unconvenient. The transcript extractor fetches the transcript, strips extraneous data and saves a HTML file that can be open with any browser. Print to PDF for a clean, clear unofficial transcript.


###Usage
Run the utility through the command line as it requires input arguments.

To get full usage information run : McGill_transcript_extractor.py -h

`./transcript_extractor/McGill_transcript_extractor.py john.doe0@mail.mcgill.ca output.pdf` will extract the student's (replace john.doe0@mail.mcgill.ca with your own McGill email) transcript to output.pdf. You will be prompted to input the password associated with the email.

The code can be modified to use a local version of the transcript html (retrieved by saving the transcript html when on the transcript page). The Perl file is the original local implementation and does not contain any additions and bug fixes the Python script contains.

Optional flags for html only or additional output also possible.

## Schedule Extractor
Sometimes it's nice to have a paper copy of your schedule (before you place your classes in your digial calendar or memorize lecture locations or when your digital calendar is down). Minerva makes it difficult to get a no-nonsense schedule copy (again print screen and direct print to PDF give poor results), this is my solution. The schedule extractor removes the cruft (banner, links, CRN ...) while keeping important information (class location, course code ...), saves it to a HTML file from which a clean schedule can be printed.


###Usage
Run the utility through the command line as it requires input arguments.

To get full usage information run : McGill_schedule_extractor.py -h

`./schedule_extractor/McGill_schedule_extractor.py john.doe0@mail.mcgill.ca output.pdf mm/dd/yyyy` will extract the student's (replace john.doe0@mail.mcgill.ca with your own McGill email) schedule of the week in which mm/dd/yyyy occurs to output.pdf. You will be prompted to input the password associated with the email.

The code can be modified to use a local version of the schedule html (retrieved by saving the schedule html when on the schedule page). The Perl file is the original local implementation and does not contain any additions and bug fixes the Python script contains.

optional flags can be used to change the highlight color and for html only or additional output.


## Dependencies
* Python 2.7 or greater (using getpass, argparse, urllib, urllib2, cookielib libraries)
* pisa, Python html to pdf library

##Known bugs
* Extracted transcript : in output html, the message decribing codes in columns doesn't display correctly under Firefox 27.0 (displays fine under Chrome).
* Extracted transcript : execution fails returning error decribing wrong version of `reportlab` (despite having latest version). Fix, requires administative powers, sudo).
  1. (optional, linux) In a command line run `pip freeze | grep 'reportlab'`, the output should reveal what version of reportlab is installed. This bug affects versions 3.0 and above. if a version of 2.0 or below is reported, upgrade to a newer version of report lab.
  2. Find `pisa_util.py` file (in Linux, under `/usr/lib/pymodules/python2.7/sx/pisa3`) change the lines checking the versions to:
  
    `if not((reportlab.Version[0] == "2" and reportlab.Version[2] >= "1") or (reportlab.Version[0] > "2")):`
    
    `raise ImportError("Reportlab Version 2.1+ is needed!")`
    
    `REPORTLAB22 = ((reportlab.Version[0] == "2" and reportlab.Version[2] >= "2") or (reportlab.Version[0] > "2"))`

   
* FIXED: ~~Extracted schedule : in output html, courses don't exactly line up with the times they occur.~~
* Extracted schedule : if there is no schedule to display (e.g. a term during which no classes are taken) a ho.pisa exception is raised, a blank file is produced
