#!/usr/bin/perl
#
use open qw/ :std :encoding(utf8) /;

use warnings;
use strict;
use utf8;
use JSON;
use Encode;

my $filename = 'Kafer_mittereuropas_öko2.txt';

open(FH, '<', $filename) or die $!;

my $start = 0;
my $bloque = 0;
my $line;
my @data = ();

my %hash = ();
my %params = ();
my $last_param = '';

while(<FH>){
    $line = $_;
    chomp $line;
    if ($line =~ /^01..000..000/) { 
        $start = 1; 
    }
    if ($start) {
        if ($line =~ /^\s*(\*?\d+[#-., ]+\d+[#-., ]+\d+[#-., ]+)(.*)/) {

            if (%hash) {
                my $json = to_json( \%hash );
                push ( @data, $json );
            }

            $bloque = 1;
            $hash{'spline'} = $2;
            my $species = $2;

            $1 =~ /(\*?\d+)[.# ]+(\d+)[.# ]+(\d+)/;
            $hash{'id'} = $1." ".$2." ".$3;
            
            #$species =~ /^\s*([bm]\s+)?(\w+)\s+(\w+)[.,]?\s+(.+)?/;
            my $pre = '';
            my $arten = '';
            my $verbr = '';
            if ($species =~ /^\s*([abm])\s+(.+)/) {
                $pre = "[$1] ";
                $species = $2;
            }

            if ($species =~ /^ssp\.\s+(\w+)\s+(\w+)[.,]?\s+(.+)?/) {
                $arten = "ssp. $1 $2.";
                if ($3) {
                    $verbr = $3;
                }
            } elsif ($species =~ /^(\w+)\s+(\w+)[.,]?\s+ssp[.,]\s+(\w+)\s+(\w+)\s+(.+)?/) {
                $arten = "$1 $2. ssp. $3 $4";
                if ($5) {
                    $verbr = $5;
                }
            } else {
                if ($species =~ /^(\w+)\s+(\w+)[.,]?\s+(.+)?/) {
                    $arten = "$1 $2.";
                    if ($3) {
                        $verbr = $3;
                    }
                } else {

                    next;
                }
            }
            $hash{'Arten'} = $pre.$arten;
            $hash{'Verbreitung'} = $verbr;

            %params = ();
            $last_param = '';
        } else {
            
            if ($bloque == 1) {
                my @oko = split / # /,$line;
                %params = ("oko" => [@oko]);
            } else {
                if ( $line =~ /^(H):(.+)/) {
                    $params{'Habitat'} = $2;
                    $last_param = 'Habitat';
                }
                elsif ( $line =~ /^(Ni):(.+)/) {
                    $params{'Niche'} = $2;
                    $last_param = 'Niche';
                }
                elsif ( $line =~ /^(Na):(.+)/) {
                    $params{'Nahrung'} = $2;
                    $last_param = 'Nahrung';
                } else {
                    # newline
                    $params{$last_param} .= " ".$line;
                }

            }
            $hash{'params'} = \%params;

            $bloque = $bloque + 1;
        }

        $start = $start +1; 
    }
}

close(FH);

binmode(STDOUT, ":utf8");
print "[";
print join ",", @data;
print "]";
