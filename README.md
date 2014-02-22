minerva_utils
=============

Set of utilities to access services on Minerva, McGill University's Administrative system.


Specifically :
* /transcript_extractor : a utility to extract an up-to-date unofficial transcript from the McGill website
* /schedule_extractor : a utility to extract a week's schedule from the McGill website

## Transcript Extractor
Because sometimes you need a version of your transcript handy (and waiting a couple days, walking to Service Point isn't convenient). Print screen and print page to PDF keeps all the links, the banner and in general is unconvenient. The transcript extractor fetches the transcript, strips extraneous data and saves a HTML file that can be open with any browser. Print to PDF for a clean, clear unofficial transcript.

###Usage
Run the utility through the command line as it requires input arguments.

To get full usage information run : McGill_transcript_extractor.py -h

`./transcript_extractor/McGill_transcript_extractor.py john.doe0@mail.mcgill.ca output.html` will extract the student's (replace john.doe0@mail.mcgill.ca with your own McGill email) transcript to output.html. You will be prompted to input the password associated with the email.

The code can be modified to use a local version of the transcript html (retrieved by saving the transcript html when on the transcript page). The Perl file is the original local implementation and does not contain any additions and bug fixes the Python script contains.

There are no optional flags

## Schedule Extractor
Sometimes it's nice to have a paper copy of your schedule (before you place your classes in your digial calendar or memorize lecture locations or when your digital calendar is down). Minerva makes it difficult to get a no-nonsense schedule copy (again print screen and direct print to PDF give poor results), this is my solution. The schedule extractor removes the cruft (banner, links, CRN ...) while keeping important information (class location, course code ...), saves it to a HTML file from which a clean schedule can be printed.


###Usage
Run the utility through the command line as it requires input arguments.

To get full usage information run : McGill_schedule_extractor.py -h

`./schedule_extractor/McGill_schedule_extractor.py john.doe0@mail.mcgill.ca output.html mm/dd/yyyy` will extract the student's (replace john.doe0@mail.mcgill.ca with your own McGill email) schedule of the week in which mm/dd/yyyy occurs to output.html. You will be prompted to input the password associated with the email.

The code can be modified to use a local version of the schedule html (retrieved by saving the schedule html when on the schedule page). The Perl file is the original local implementation and does not contain any additions and bug fixes the Python script contains.

optional flags can be used to change the highlight color


## Dependencies
* Python 2.7 or greater (using getpass and argparse libraries)

##Known bugs
* Extracted transcript : in output html, the message decribing codes in columns doesn't display correctly under Firefox 27.0 (displays fine under Chrome).
* Extracted schedule : in output html, courses don't exactly line up with the times they occur.