#! /usr/bin/perl

use warnings;
use strict;

my $infile = "input_transcript.html";
my $outfile = "output_transcript.html";

open(my $IN, "<", $infile)
	or die("Input file cannot be opened.\n");
open(my $OUT, ">", $outfile) 
	or die("Output file cannot be opened.\n");

#Slurp in file
my @inlines = <$IN>;
my @outlines;
my $counter = 0;
my $table = 0;

print $OUT "<html>";

foreach (@inlines) {
	#information about remarks (special letters)
	if(/<SPAN.*Wingdings.*>.*<\/SPAN>/.../<p>/) {push(@outlines, $_);}
	
	#syle for table
	if(/<STYLE.*>/.../<\/STYLE>/) {push(@outlines, $_);}
	
	#table with student info
	if(/<TABLE.*CLASS="student_info".*>/.../<\/TABLE/) {push(@outlines, $_);}
	
	#lines with transcript information
	if(/<TABLE.*CLASS="main.*>/) {
		$table = 1;
		$counter = 1;
		push(@outlines, $_);
		next;
	}
	elsif(/<TABLE.*/ && $table == 1) {
		$counter++;
		push(@outlines, $_);
		next;
	}
	elsif(/<\/TABLE>/ && $table == 1) {
		$counter--;
		push(@outlines, $_);
		next;
	}
	
	if($counter != 0 && $table == 1) {
		push(@outlines, $_);
	}
}

print $OUT @outlines;
print $OUT "</html>";

close $IN;
close $OUT;
