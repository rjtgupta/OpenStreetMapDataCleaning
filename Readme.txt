Description of Files -
Report.pdf	       -> Final Project Report
Cleaning.py            -> Python file where all cleaning has been performed and data is converted from XML to .csv format according to the schema and is entered in the respective tables.
Schema.py              -> Python file providing the schema to be followed for conversion from XML to .csv format.
County_check.py        -> Python file checking the county names to make sure they are in the correct format and making required changes if they aren't so.
PostCode_check.py      -> Python file checking the postal codes to make sure they are in the correct format and making required changes if they aren't so.
Source_check_values.py -> Python file used to print the different values printed when the tag with attribute 'k' = 'source'.
Source_check.py        -> Python file to standardize the values analysed in the file 'Source_check_values.py'.
Street_check.py        -> Python file used to check the last part of street names for any abbreviations and making the required changes.
Link.txt	       -> File containing the link to the dataset and a description of the Area being analyzed.
sample_file.osm	       -> OSM File containing a sample of the data analysed.
References.txt	       -> File containing a list of all sources referred for completion of the project.