The first tool is a command-line tool that parses a KiCad .cmp file into a .JSON file with the component values and footprint IDs. The second tool opens the .JSON file in a browser window and uses the data to search octopart. To this data you can add the price and manufacturer ID obtained from octopart. When finished the data is saved as a CSV, which octopart accepts and can be used to create a shopping cart (I think).

Requirements:
Python (sys, os, getopt, json), HTML5 capable browser (and internet connection for connection to octopart)

Usage:
    
python kicad_cmp_converter.py [input cmp file] [output file] [output type, CSV or JSON (upper or lowercase is OK)]
    
python kicad_cmp_converter.py test.cmp test.csv csv
