#!/usr/bin/perl
#
use open qw/ :std :encoding(utf8) /;

use warnings;
use strict;
use utf8;
use JSON;

#my $json = JSON->new;

my $filename = 'Kafer_mittereuropas_öko2.txt';

open(FH, '<', $filename) or die $!;

my $start = 0;
my $bloque = 0;
my $line;
my @data = ();

my %hash = ();
my %params = ();

while(<FH>){
    $line = $_;
    chomp $line;
    if ($line =~ /^01..000..000/) { 
        $start = 1; 
    }
    if ($start) {
        if ($line =~ /^\s*(\*?\d+[#-., ]+\d+[#-., ]+\d+[#-., ]+)(.*)/) {

            if (%hash) {
                my $json = encode_json \%hash;
                push ( @data, $json );
            }

            $bloque = 1;
            $hash{'id'} = $1;
            #$hash{'spline'} = $2;
            $2 =~ /^\s*(\w+)\s+(\w+)[.,]?\s+(.+)/;
            $hash{'species'} = $1." ".$2.".";
            $hash{'Arten'} = $3;
            %params = ();
        } else {
            
            if ($bloque == 1) {
                my @oko = split / # /,$line;
                %params = ("oko" => [@oko]);
            } else {
                if ( $line =~ /^(H):(.+)/) {
                    $params{'Habitat'} = $2;
                }
                elsif ( $line =~ /^(Ni):(.+)/) {
                    $params{'Niche'} = $2;
                }
                elsif ( $line =~ /^(Na):(.+)/) {
                    $params{'Nahrung'} = $2;
                }
            }
            $hash{'params'} = \%params;

            $bloque = $bloque + 1;
        }

        $start = $start +1; 
    }
}

close(FH);

print "[";
print join ",", @data;
print "]";
