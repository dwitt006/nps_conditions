#!/usr/bin/python

#  NAME::   nps_update_test
#  WRITER:: Draper Wittkopp
#  COURSE:: CS411: Professional Workforce Development II
#  GROUP::  Black: Hike Planner
#  DATE::   18 August 2016
#  UPDATE:: 18 August 2016
#  SUMMARY::


"""
TESTING:
Retrieves the url for individual parks from the NPS website,
creates a list of all the parks and their websites, and outputs
the data into a file.
"""

import unittest
import nps_update
import csv
import os


class TestOutput(unittest.TestCase):

    def test_print_to_file(self):
        nps_update.park_name = ["Test Name: 1", "Test Name: 2"]
        nps_update.park_url = ["Test URL: 1", "Test URL: 2"]
        nps_update.out_file = "./nps_update_testing/TestPrintToFileResult.txt"
        comp_file = "./nps_update_testing/TestPrintToFileCompare.txt"
        nps_update.print_to_file()
        f1 = open(nps_update.out_file, "r")
        f2 = open(comp_file, "r")
        file_read1 = f1.read()
        file_read2 = f2.read()
        f1.close()
        f2.close()
        self.assertEqual(file_read1, file_read2)

    def test_print_to_sheet(self):
        nps_update.park_name = ["Test Name: 1", "Test Name: 2"]
        nps_update.park_url = ["Test URL: 1", "Test URL: 2"]
        nps_update.out_file = "./nps_update_testing/TestPrintToSheetResult.csv"
        comp_file = "./nps_update_testing/TestPrintToSheetCompare.csv"
        read_result = []
        read_comp = []
        nps_update.print_to_sheet()
        f1 = open(nps_update.out_file, "r")
        f2 = open(comp_file, "r")
        csv_read1 = csv.reader(f1)
        csv_read2 = csv.reader(f2)
        for row in csv_read1:
            read_result.append(row)
        for row in csv_read2:
            read_comp.append(row)
        f1.close()
        f2.close()
        self.assertEqual(read_result, read_comp)

    def test_file_type(self):
        nps_update.park_name = ["Test Name: 1", "Test Name: 2"]
        nps_update.park_url = ["Test URL: 1", "Test URL: 2"]
        # Remove existing test files
        if os.path.exists("./nps_update_testing/TestFileType.txt"):
            os.remove("./nps_update_testing/TestFileType.txt")
        elif os.path.exists("./nps_update_testing/TestFileType.csv"):
            os.remove("./nps_update_testing/TestFileType.csv")
        elif os.path.exists("./nps_update_testing/TestFileType.cpp"):
            os.remove("./nps_update_testing/TestFileType.cpp")
        else:
            pass
        # Case 1: .txt
        nps_update.out_file = "./nps_update_testing/TestFileType.txt"
        nps_update.file_type()
        # Case 2: .csv
        nps_update.out_file = "./nps_update_testing/TestFileType.csv"
        nps_update.file_type()
        # Case 3: other
        nps_update.out_file = "./nps_update_testing/TestFileType.cpp"
        nps_update.file_type()
        # Test Cases
        case1 = os.path.exists("./nps_update_testing/TestFileType.txt")
        case2 = os.path.exists("./nps_update_testing/TestFileType.csv")
        case3 = os.path.exists("./nps_update_testing/TestFileType.cpp")
        self.assertEqual(case1 & case2 & case3, True)

    def test_file_type_case1(self):
        nps_update.park_name = ["Test Name: 1", "Test Name: 2"]
        nps_update.park_url = ["Test URL: 1", "Test URL: 2"]
        nps_update.out_file = "./nps_update_testing/TestFileType.txt"
        comp_file = "./nps_update_testing/TestPrintToFileCompare.txt"
        nps_update.file_type()
        f1 = open(nps_update.out_file, "r")
        f2 = open(comp_file, "r")
        file_read1 = f1.read()
        file_read2 = f2.read()
        f1.close()
        f2.close()
        self.assertEqual(file_read1, file_read2)

    def test_file_type_case2(self):
        nps_update.park_name = ["Test Name: 1", "Test Name: 2"]
        nps_update.park_url = ["Test URL: 1", "Test URL: 2"]
        nps_update.out_file = "./nps_update_testing/TestFileType.csv"
        comp_file = "./nps_update_testing/TestPrintToSheetCompare.csv"
        read_result = []
        read_comp = []
        nps_update.file_type()
        f1 = open(nps_update.out_file, "r")
        f2 = open(comp_file, "r")
        csv_read1 = csv.reader(f1)
        csv_read2 = csv.reader(f2)
        for row in csv_read1:
            read_result.append(row)
        for row in csv_read2:
            read_comp.append(row)
        f1.close()
        f2.close()
        self.assertEqual(read_result, read_comp)

    def test_file_type_case3(self):
        nps_update.park_name = ["Test Name: 1", "Test Name: 2"]
        nps_update.park_url = ["Test URL: 1", "Test URL: 2"]
        nps_update.out_file = "./nps_update_testing/TestFileType.cpp"
        comp_file = "./nps_update_testing/TestPrintToFileCompare.txt"
        nps_update.file_type()
        f1 = open(nps_update.out_file, "r")
        f2 = open(comp_file, "r")
        file_read1 = f1.read()
        file_read2 = f2.read()
        f1.close()
        f2.close()
        self.assertEqual(file_read1, file_read2)


class TestReadArgs(unittest.TestCase):

    def test_update_url_html(self):
        nps_update.sys.argv.append("-u")
        nps_update.sys.argv.append("https://www.google.com")
        nps_update.read_args()
        self.assertEqual(nps_update.url, "https://www.google.com")
        pass

    def test_update_output_file(self):
        nps_update.sys.argv.append("-o")
        nps_update.sys.argv.append("./nps_update_testing/TestUpdateOutputFile.csv")
        nps_update.read_args()
        self.assertEqual(nps_update.out_file, "./nps_update_testing/TestUpdateOutputFile.csv")
        pass

    def test_update_display(self):
        nps_update.sys.argv.append("-p")
        nps_update.read_args()
        self.assertEqual(nps_update.display, True)
        pass

    def test_multi_update(self):
        nps_update.sys.argv.append("-upo")
        nps_update.sys.argv.append("https://www.google.com")
        nps_update.sys.argv.append("./nps_update_testing/TestMultiUpdateOutputFile.csv")
        nps_update.read_args()
        self.assertEqual(nps_update.out_file, "./nps_update_testing/TestMultiUpdateOutputFile.csv")


class TestListUpdates(unittest.TestCase):

    def test_clean_park_name(self):
        nps_update.park_name = ["Test1      ", "&", "Test2"]
        nps_update.clean_park_name()
        self.assertEqual(nps_update.park_name[0], "Test1 & Test2")
        pass

    def test_update_park_url(self):
        nps_update.park_url = ["TEST"]
        nps_update.update_park_url()
        self.assertEqual(nps_update.park_url[0], "https://www.nps.gov/TEST/planyourvisit/conditions.htm")
        pass


class TestHTMLFileParser(unittest.TestCase):

    def test_handle_data(self):
        nps_update.park_name = []
        nps_update.park_url = []
        parser = nps_update.HTMLFileParser()
        parser.feed(u"<html><option value='TEST'>This is a test</option></html>")
        self.assertEqual(nps_update.park_name[0], "This is a test")
        self.assertEqual(nps_update.park_url[0], "TEST")
        pass


if __name__ == '__main__':
    unittest.main()
