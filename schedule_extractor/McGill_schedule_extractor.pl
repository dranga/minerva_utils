#! /usr/bin/perl

use warnings;
use strict;

my $infile = "input.html";
my $outfile = "output.html";

open(my $IN, "<", $infile)
	or die("Input file cannot be opened.\n");
open(my $OUT, ">", $outfile) 
	or die("Output file cannot be opened.\n");

#Slurp in file
my @inlines = <$IN>;
my @outlines;

#append CSS txt to output file
my $CSS = <<STYLE
<html>
<style type="text/css">
table{
border-collapse:collapse;
border:1px solid #000;
}
table td{
border:1px solid #000;
}
 </style>
STYLE
;
print $OUT $CSS;

#Don't parse HTML with RE they said
#Just watch me
foreach (@inlines) {
	if(/^<TABLE.*This layout table is used to present the weekly course schedule.*>/.../<\/TABLE>/) { #process only lines in between 2 matches (inclusive)
		if(/^<\/TR>/) { #remove Saturday and Sunday
			pop @outlines;
			pop @outlines;
		}
		if(/CLASS="ddlabel"/) { #modify class info
			s/<A HREF=".*">//; #remove useless link
			s/([A-Z]{4} \d{3}-\d{3}<BR>).*<BR>(.*<BR>)/$1$2/; #remove CRN and number of occurences, keep class code and start and end time
		}
		push(@outlines, $_);
	}
}
	
print $OUT @outlines;
print $OUT "</html>";

close $IN;
close $OUT;
