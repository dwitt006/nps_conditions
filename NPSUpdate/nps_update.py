#!/usr/bin/python

#  NAME::   nps_update
#  WRITER:: Draper Wittkopp
#  COURSE:: CS411: Professional Workforce Development II
#  GROUP::  Black: Hike Planner
#  DATE::   04 May 2016
#  UPDATE:: 17 August 2016
#  SUMMARY::


"""
Retrieves the url for individual parks from the NPS website,
creates a list of all the parks and their websites, and outputs
the data into a file.
"""


from HTMLParser import HTMLParser
import csv
import sys
import urllib2


url = "https://www.nps.gov/findapark/index.htm"  # Website used to list all parks
html_file = ""  # Copy of the url's html
out_file = "nps_parks.txt"  # Output file; txt default; csv optional
park_name = []  # List of park names
park_url = []  # List of park urls
display = False  # Display output optional


# Updates the html_file from url
def update_html():
    global html_file
    response = urllib2.urlopen(url)  # Opens url
    html_file = response.read()  # Copies html


# Prints results to screen
def print_to_screen():
    # For each park, prints name and url to display
    for i in range(len(park_name)):
        print "{}  {}\t{}".format(str(i+1).ljust(5), str(park_name[i]).ljust(75), park_url[i])
    print "\tpark name len: {}\n\tpark url len: {}".format(len(park_name), len(park_url))


# Print text to file
def print_to_file():
    # For each park, prints name and url to file
    f = open(out_file, "w")
    for i in range(len(park_name)):
        f.write("{}\t{}\n".format(str(park_name[i]).ljust(75), park_url[i]))
    f.close()


# Print to spreadsheet
def print_to_sheet():
    # For each park, prints name and url to csv style spreadsheet
    sheet = csv.writer(open(out_file, "wb"))
    for i in range(len(park_name)):
        row = [park_name[i], park_url[i]]
        sheet.writerow(row)


# Determine file type
def file_type():
    # Changing of file name and destination is optional
    if out_file.endswith(".txt"):  # If the file is txt, print_to_file
        print_to_file()
    elif out_file.endswith(".csv"):  # If the is csv, print_to_sheet
        print_to_sheet()
    else:
        print_to_file()  # If any other file type, use standard print_to_file


# Reads and determines argument implementation
def read_args():
    global url
    global out_file
    global display
    initial_args = []  # List of optional arguments
    supplementary_args = []  # List of arguments needed for the options
    if len(sys.argv) > 1:
        # For the arguments, determines if any options are used
        for i in range(1, len(sys.argv)):
            # If an option is found, it is added to the list
            if sys.argv[i][0] == "-":  # Strings with first character '-' are options
                # For each string arg, adds char following '-' to list
                for c in range(1, len(sys.argv[i])):
                    initial_args.append(sys.argv[i][c])
            else:
                supplementary_args.append(sys.argv[i])  # Strings w/o '-' are args needed for options
        i = 0
        # Determines which options are used
        while i < len(initial_args):
            # -u updates the url
            if initial_args[i] == "u":
                url = supplementary_args[i]
                # Attempt to use the provided url
                try:
                    update_html()
                # Improper url
                except ValueError:
                    print "Error: invalid url: {}".format(url)
                    sys.exit()
                # -u used w/o the supplementary argument
                except IndexError:
                    print "Error: url not provided"
                    sys.exit()
            # -o updates the output file
            elif initial_args[i] == "o":
                try:
                    out_file = supplementary_args[i]
                except IndexError:
                    print "Error: file not provided"
                    sys.exit()
            # -p prints the output to screen
            elif initial_args[i] == "p":
                display = True  # Updates bool
                del initial_args[i]  # Not needed in list
                i -= 1  # Moves to previous position in loop
            # Any other option is invalid
            else:
                print "Error: invalid argument: {}".format(initial_args[i])
                sys.exit()
            i += 1  # Moves to following position in loop
        # If option -u was not implemented, html is updated with default url
        if html_file == '':
            update_html()
        else:
            pass
    # If no options were implemented, html is updated with default url
    else:
        update_html()


# Clean list of park names
# Joins strings that were separated by '&' and excess whitespace from html
def clean_park_name():
    global park_name
    for index, name in enumerate(park_name):
        park_name[index] = " ".join(name.split())  # Split the string
        # If the current name is now '&', remove it and combine the list's previous and following strings
        if name == "&":
            park_name[index] = " ".join(park_name[index-1:index+2])
            del park_name[index+1]
            del park_name[index-1]
        else:
            pass


# Update park_url to include full urls
def update_park_url():
    for i in range(len(park_url)):
        # Changes simple string, taken from html, to full url
        # url for alerts and conditions
        park_url[i] = "https://www.nps.gov/{}/planyourvisit/conditions.htm".format(park_url[i])


# HTMLParser subclass for custom handlers
class HTMLFileParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.inline = False

    # Finds start tag 'option', appends 'value' to url list
    def handle_starttag(self, tag, attrs):
        global park_url
        self.inline = False
        if tag == "option":
            for name, value in attrs:
                if name == "value" and len(value) > 2:
                    self.inline = True
                    park_url.append(value)
                else:
                    pass
        else:
            pass

    # Finds end tag to 'option'
    def handle_endtag(self, tag):
        if tag == "option":
            self.inline = False
        else:
            pass

    # Appends data associated with 'option' to park name list
    def handle_data(self, data):
        global park_name
        if self.inline and data.strip():
            park_name.append(data)


def main():
    read_args()
    parser = HTMLFileParser()
    parser.feed(html_file)
    clean_park_name()
    update_park_url()
    file_type()
    if display:
        print_to_screen()

if __name__ == '__main__':
    main()
