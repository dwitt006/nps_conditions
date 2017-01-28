#!/usr/bin/python

#  NAME::   nps_alerts
#  WRITER:: Draper Wittkopp
#  COURSE:: CS411: Professional Workforce Development II
#  GROUP::  Black: Hike Planner
#  DATE::   01 June 2016
#  UPDATE:: 20 August 2016
#  SUMMARY::


"""
Retrieves alerts and conditions from the National Park Service. A list of parks and their URLs are provided to the
program in a file (nps_update). The HTML is then accessed from the URLs and scanned for alerts and conditions.
The alerts and conditions are then put into a file.
"""


from HTMLParser import HTMLParser
from Queue import Queue
from threading import Thread
import csv
import sys
import urllib2


in_file = "nps_parks.txt"  # Default input file location
out_file = "nps_alerts.txt"  # Default output file location
display = False  # Determines on screen display of results
parallel = False  # Determines sequential or parallel run
alerts = []  # Contains lists of park names and alerts
html_files = []  # Contains a list of park names and html's
parks = []  # Contains lists of park names and urls
url_count = 10  # Number of urls for each thread


# HTMLParser subclass for custom handlers
class HTMLFileParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.inline = False
        self.alerts = []  # Should contain alert title followed by description

    # Finds start tag 'h3' and 'span'
    def handle_starttag(self, tag, attrs):
        self.inline = False
        # Tags for h3 contain the title for the alert
        if tag == "h3":
            for name, value in attrs:
                if name == "class" and value == "Alert-title":
                    self.inline = True
                else:
                    pass
        # Tags for span contain the alert's description
        elif tag == "span":
            for name, value in attrs:
                if name == "tabindex" and value == "0":
                    self.inline = True
                else:
                    pass
        else:
            pass

    # Finds end tag to 'h3' and 'span'
    def handle_endtag(self, tag):
        if tag == "h3":
            self.inline = False
        elif tag == "span":
            self.inline = False
        else:
            pass

    # Appends data associated with 'option' to park name list
    def handle_data(self, data):
        if self.inline and data.strip():
            self.alerts.append(data)


# Reads and determines which arguments are being used
def read_args():
    global in_file
    global out_file
    global display
    global parallel
    global url_count
    initial_args = []  # List of optional arguments
    supplementary_args = []  # List of arguments needed for the options
    if len(sys.argv) > 1:
        # For the arguments, determines if any options are used
        for i in range(1, len(sys.argv)):
            # If an option is found, it is added to the list
            if (type(sys.argv[i]) is str) and (sys.argv[i][0] == "-"):  # Strings with first character '-' are options
                # For each string arg, adds char following '-' to list
                for c in range(1, len(sys.argv[i])):
                    initial_args.append(sys.argv[i][c])
            else:
                supplementary_args.append(sys.argv[i])  # Strings w/o '-' are args needed for options
        i = 0
        while i < len(initial_args):
            # -i updates the input file
            if initial_args[i] == "i":
                in_file = supplementary_args[i]
                # Determines if file exists
                try:
                    infile = open(in_file, "r")
                    infile.close()
                except IOError:
                    print "No such file: {}".format(in_file)
                    sys.exit()
            # -o updates the output file
            elif initial_args[i] == "o":
                out_file = supplementary_args[i]
            # -p prints the output to screen
            elif initial_args[i] == "p":
                display = True  # Updates bool
                del initial_args[i]  # Not needed in list
                i -= 1  # Moves to previous position in loop
            # -P uses threading to run parallel
            elif initial_args[i] == "P":
                parallel = True  # Updates bool
                del initial_args[i]  # Not needed in list
                i -= 1  # Moves to previous position in loop
            elif initial_args[i] == "u":
                url_count = supplementary_args[i]
            # Any other option is invalid
            else:
                print "Error: invalid argument: {}".format(initial_args[i])
                sys.exit()
            i += 1  # Moves to following position in loop
    else:
        pass


# Prints results to screen
def print_to_screen():
    # For each park, prints name and alert titles and alert descriptions to screen
    for i in range(len(alerts)):
        for j in range(len(alerts[i])):
            if j == 0:
                print "\n\t{}:\n".format(alerts[i][j])
            elif j != 0 and (j % 2 == 0):
                print "\t\t\t{}\n".format(alerts[i][j])
            else:
                print "\t\t{}\n".format(alerts[i][j])


# Write results text to file
def print_to_file():
    # For each park, writes name, alert titles, and alert descriptions to file
    f = open(out_file, "w")
    for i in range(len(alerts)):
        for j in range(len(alerts[i])):
            if j == 0:  # First index is park name
                f.write("{}:\n".format(alerts[i][j]))  # Write name
            elif j != 0 and (j % 2 == 0):  # All other even indices are descriptions
                f.write("\t\t{}\n".format(alerts[i][j]))  # Write alert description
            else:
                f.write("\t{}\n".format(alerts[i][j]))  # Write alert title
    f.close()


# Write results to spreadsheet
def print_to_sheet():
    # For each park, writes name, alert titles, and alert descriptions to csv style spreadsheet
    sheet = csv.writer(open(out_file, "wb"))
    for alert in alerts:
        row = alert
        sheet.writerow(row)


# Determine file type for output
def output_file_type():
    # Changing of file name and destination is optional
    if out_file.endswith(".txt"):  # If the file is txt, print_to_file
        print_to_file()
    elif out_file.endswith(".csv"):  # If the is csv, print_to_sheet
        print_to_sheet()
    else:
        print_to_file()  # If any other file type, use standard print_to_file


# Read from a standard file
def read_file():
    global parks
    input_file = open(in_file, 'r')  # Open input file
    file_string = input_file.read()  # Create string from input file
    input_file.close()  # Close input file
    parks = file_string.split('\n')  # Split the string at '\n', creating a list of strings
    parks.remove('')  # Remove any empty string from the list
    # Make the list two dimensional
    for i in range(len(parks)):
        park = parks[i].split('\t')  # Split the string at '\t', creating a list of strings
        parks[i] = park
        # Remove whitespace at end of string
        for j in range(len(parks[i])):
            parks[i][j] = parks[i][j].rstrip()


# Read from spreadsheet
def read_sheet():
    global parks
    input_file = open(in_file, 'r')  # Open input file
    park_reader = csv.reader(input_file)  # use reader from csv module
    # Add each row to list of parks
    for row in park_reader:
        parks.append(row)
    input_file.close()  # Close input file


# Determines file type for input
def input_file_type():
    # Changing of input file name and destination is optional
    if in_file.endswith(".txt"):  # If the file is txt, print_to_file
        read_file()
    elif in_file.endswith(".csv"):  # If the is csv, print_to_sheet
        read_sheet()
    else:
        read_file()  # If any other file type, use standard print_to_file


# Obtains a copy of the html from the provided park url
# Container could be list or queue
def get_html(park, container):
    park_html = []
    try:
        response = urllib2.urlopen(park[1])  # Opens url
        html_file = response.read()  # Copies html
        html_file = unicode(html_file, encoding='ascii', errors='ignore')  # Removes non-ascii char
        park_html.append(park[0])   # Add park name to park_html
        park_html.append(html_file)  # Add park html to park_html
        # Container is list
        if type(container) is list:
            container.append(park_html)  # Add park_html to list
        # Container is Queue
        else:
            container.put(park_html)  # Put park_html in queue
    # Improper url
    except urllib2.HTTPError:
        # print "Error: invalid url: {}2".format(park[1])
        pass


# Obtains html files sequentially
def sequential_html_manager():
    global html_files
    # For each park in parks list
    # put html file in html list
    for park in parks:
        get_html(park, html_files)


# Works with parallel_html_manager
def parallel_html_worker(parks_arg, container):
    # For each park in parks list
    # use get_html with provided list and queue
    for park in parks_arg:
        get_html(park, container)


# Obtains html files parallel
def parallel_html_manager():
    global html_files
    html_container = Queue()  # Queue for html files
    threads = []  # List of threads
    x = 0
    # Give ten parks to each thread
    while x <= len(parks):
        # Create threads
        this_thread = Thread(target=parallel_html_worker, args=(parks[x:(x + url_count)], html_container))
        this_thread.start()  # Start thread
        threads.append(this_thread)  # Add thread to list
        x += url_count  # Iterate parks by provided number
    for thread in threads:  # Iterate list of threads
        thread.join()  # join() each thread
    # Return html list to parent thread
    while not html_container.empty():  # While queue is not empty
        html_files.append(html_container.get())  # Move elements from queue to list
    html_files.sort(key=lambda z: z[0])  # Sort html_files according to park name


def html_parser_manager():
    global alerts
    for park in html_files:
        parser = HTMLFileParser()  # Creates an HTMLFileParser for the provided park list
        parser.alerts.append(park[0])  # Adds the park name to the alert list
        parser.feed(park[1])  # Feed html file to parser
        # If number of alerts is greater than 1
        # Add to alerts
        if len(parser.alerts) > 1:
            alerts.append(parser.alerts)
        # Else pass
        else:
            pass


# Cleans list of alerts
# removes any '\n' from the retrieved html
# Joins strings that were separated by '&' and excess whitespace from html
def clean_alerts():
    global alerts
    for i in range(len(alerts)):
        j = 0
        while j < len(alerts[i]):
            # If the current name is now '&', combine and remove the list's previous and following strings
            if alerts[i][j] == "&":
                alerts[i][j] = " ".join(alerts[i][j-1:j+2])
                alerts[i][j] = alerts[i][j].replace('\n', '')  # Remove '\n'
                del alerts[i][j-1]
                del alerts[i][j]
            else:
                alerts[i][j] = alerts[i][j].replace('\n', '')  # Remove '\n'
                j += 1


def main():
    read_args()
    input_file_type()
    if parallel:
        parallel_html_manager()
    else:
        sequential_html_manager()
    html_parser_manager()
    clean_alerts()
    output_file_type()
    if display:
        print_to_screen()
    pass

if __name__ == '__main__':
    main()
