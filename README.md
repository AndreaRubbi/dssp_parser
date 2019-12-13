# dssp_parser by: Andrea Rubbi
Python program which is able to analyze dssp files in order to estimate the interacting area and interacting residues between monomers of a complex protein 

This program is part of a larger project whose aim is to analyze the Hemoglobin complex and its components.
It is written in python and it is quite easy to use:

### How to use it:

run the program using: 
$ ./dssp_parser.py

It will then ask you some info:
chain of interest --> input on terminal
dssp of a trimer with the selected chain --> input by selecting a file from the
                                             automatically opened window
dssp of the tetramer --> same as above

Then it asks whether you would like to analyze the interacting 
surface with the tetramer or with the trimer --> 'r' for trimer / 'e' for tetramer

It asks whether you would like to calculate the total accessible 
area of the chain in the complex --> 'y' to calculate it

#### Finally:

It asks whether you would like to calculate the relative accessible area of the chain both 
in the tatramer and in the trimer

It also reports a table with all the residues with a significantly changing accessible area
with respect to the chain in the trimer or in the tetramer

After that it asks whether you would like to analyze another interaction or not.

## Requirements:

 -- colored --> python3 -m pip install colored
 -- numpy--> python3 -m pip install numpy
 -- easygui --> python3 -m pip install easygui
 -- pandas --> python3 -m pip install pandas


