#!/usr/bin/python

#  NAME::   nps_alerts_test
#  WRITER:: Draper Wittkopp
#  COURSE:: CS411: Professional Workforce Development II
#  GROUP::  Black: Hike Planner
#  DATE::   19 August 2016
#  UPDATE:: 19 August 2016
#  SUMMARY::


"""
TESTING:
Retrieves alerts and conditions from the National Park Service. A list of parks and their URLs are provided to the
program in a file (nps_update). The HTML is then accessed from the URLs and scanned for alerts and conditions.
The alerts and conditions are then put into a file.
"""


from Queue import Queue
import unittest
import nps_alerts_v2
import csv
import os


class TestOutput(unittest.TestCase):

    def test_print_to_file(self):
        nps_alerts_v2.alerts = [["Test Park: 1", "Testing", "This is a test"],
                                ["Test Park: 2", "Testing", "This is a second test"]]
        nps_alerts_v2.out_file = "./nps_alerts_testing/TestPrintToFileResults.txt"
        comp_file = "./nps_alerts_testing/TestPrintToFileCompare.txt"
        nps_alerts_v2.print_to_file()
        f1 = open(nps_alerts_v2.out_file, "r")
        f2 = open(comp_file, "r")
        file_read1 = f1.read()
        file_read2 = f2.read()
        f1.close()
        f2.close()
        self.assertEqual(file_read1, file_read2)

    def test_print_to_sheet(self):
        nps_alerts_v2.alerts = [["Test Park: 1", "Testing", "This is a test"],
                                ["Test Park: 2", "Testing", "This is a second test"]]
        nps_alerts_v2.out_file = "./nps_alerts_testing/TestPrintToSheetResults.csv"
        comp_file = "./nps_alerts_testing/TestPrintToSheetCompare.csv"
        read_result = []
        read_comp = []
        nps_alerts_v2.print_to_sheet()
        f1 = open(nps_alerts_v2.out_file, "r")
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
        pass

    def test_output_file_type(self):
        nps_alerts_v2.alerts = [["Test Park: 1", "Testing", "This is a test"],
                                ["Test Park: 2", "Testing", "This is a second test"]]
        output_file = "./nps_alerts_testing/TestOutputFileType"
        # Remove existing test files
        if os.path.exists(output_file + ".txt"):
            os.remove(output_file + ".txt")
        elif os.path.exists(output_file + ".csv"):
            os.remove(output_file + ".csv")
        elif os.path.exists(output_file + ".cpp"):
            os.remove(output_file + ".cpp")
        else:
            pass
        # Case 1: .txt
        nps_alerts_v2.out_file = output_file + ".txt"
        nps_alerts_v2.output_file_type()
        # Case 2: .csv
        nps_alerts_v2.out_file = output_file + ".csv"
        nps_alerts_v2.output_file_type()
        # Case 3: other
        nps_alerts_v2.out_file = output_file + ".cpp"
        nps_alerts_v2.output_file_type()
        # Test Cases
        case1 = os.path.exists(output_file + ".txt")
        case2 = os.path.exists(output_file + ".csv")
        case3 = os.path.exists(output_file + ".cpp")
        self.assertEqual(case1 & case2 & case3, True)

    def test_output_file_type_case1(self):
        nps_alerts_v2.alerts = [["Test Park: 1", "Testing", "This is a test"],
                                ["Test Park: 2", "Testing", "This is a second test"]]
        nps_alerts_v2.output_file = "./nps_alerts_testing/TestOutputFileType.txt"
        comp_file = "./nps_alerts_testing/TestPrintToFileCompare.txt"
        nps_alerts_v2.output_file_type()
        f1 = open(nps_alerts_v2.out_file, "r")
        f2 = open(comp_file, "r")
        file_read1 = f1.read()
        file_read2 = f2.read()
        f1.close()
        f2.close()
        self.assertEqual(file_read1, file_read2)

    def test_output_file_type_case2(self):
        nps_alerts_v2.alerts = [["Test Park: 1", "Testing", "This is a test"],
                                ["Test Park: 2", "Testing", "This is a second test"]]
        nps_alerts_v2.out_file = "./nps_alerts_testing/TestOutputFileType.csv"
        comp_file = "./nps_alerts_testing/TestPrintToSheetCompare.csv"
        read_result = []
        read_comp = []
        nps_alerts_v2.output_file_type()
        f1 = open(nps_alerts_v2.out_file, "r")
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
        nps_alerts_v2.alerts = [["Test Park: 1", "Testing", "This is a test"],
                                ["Test Park: 2", "Testing", "This is a second test"]]
        nps_alerts_v2.output_file = "./nps_alerts_testing/TestOutputFileType.cpp"
        comp_file = "./nps_alerts_testing/TestPrintToFileCompare.txt"
        nps_alerts_v2.output_file_type()
        f1 = open(nps_alerts_v2.out_file, "r")
        f2 = open(comp_file, "r")
        file_read1 = f1.read()
        file_read2 = f2.read()
        f1.close()
        f2.close()
        self.assertEqual(file_read1, file_read2)


class TestInput(unittest.TestCase):

    def test_read_file(self):
        nps_alerts_v2.parks = []
        nps_alerts_v2.in_file = "./nps_alerts_testing/TestReadFile.txt"
        compare = [["Test Name: 1", "Test URL: 1"], ["Test Name: 2", "Test URL: 2"]]
        nps_alerts_v2.read_file()
        self.assertEqual(nps_alerts_v2.parks, compare)

    def test_read_sheet(self):
        nps_alerts_v2.parks = []
        nps_alerts_v2.in_file = "./nps_alerts_testing/TestReadSheet.csv"
        compare = [["Test Name: 1", "Test URL: 1"], ["Test Name: 2", "Test URL: 2"]]
        nps_alerts_v2.read_sheet()
        self.assertEqual(nps_alerts_v2.parks, compare)

    def test_input_file_type_case1(self):
        nps_alerts_v2.parks = []
        nps_alerts_v2.in_file = "./nps_alerts_testing/TestReadFile.txt"
        compare = [["Test Name: 1", "Test URL: 1"], ["Test Name: 2", "Test URL: 2"]]
        nps_alerts_v2.input_file_type()
        self.assertEqual(nps_alerts_v2.parks, compare)

    def test_input_file_type_case2(self):
        nps_alerts_v2.parks = []
        nps_alerts_v2.in_file = "./nps_alerts_testing/TestReadSheet.csv"
        compare = [["Test Name: 1", "Test URL: 1"], ["Test Name: 2", "Test URL: 2"]]
        nps_alerts_v2.input_file_type()
        self.assertEqual(nps_alerts_v2.parks, compare)

    def test_input_file_type_case3(self):
        nps_alerts_v2.parks = []
        nps_alerts_v2.in_file = "./nps_alerts_testing/TestReadFile.cpp"
        compare = [["Test Name: 1", "Test URL: 1"], ["Test Name: 2", "Test URL: 2"]]
        nps_alerts_v2.input_file_type()
        self.assertEqual(nps_alerts_v2.parks, compare)


class TestReadArgs(unittest.TestCase):

    def test_update_in_file(self):
        nps_alerts_v2.in_file = ''
        compare = "./nps_alerts_testing/TestReadFile.txt"
        nps_alerts_v2.sys.argv.append("-i")
        nps_alerts_v2.sys.argv.append(compare)
        nps_alerts_v2.read_args()
        self.assertEqual(nps_alerts_v2.in_file, compare)

    def test_update_out_file(self):
        nps_alerts_v2.out_file = ''
        compare = "test_file.txt"
        del nps_alerts_v2.sys.argv[1:]
        nps_alerts_v2.sys.argv.append("-o")
        nps_alerts_v2.sys.argv.append(compare)
        nps_alerts_v2.read_args()
        self.assertEqual(nps_alerts_v2.out_file, compare)

    def test_update_display(self):
        del nps_alerts_v2.sys.argv[1:]
        nps_alerts_v2.sys.argv.append("-p")
        nps_alerts_v2.read_args()
        self.assertEqual(nps_alerts_v2.display, True)

    def test_update_parallel(self):
        del nps_alerts_v2.sys.argv[1:]
        nps_alerts_v2.sys.argv.append("-P")
        nps_alerts_v2.read_args()
        self.assertEqual(nps_alerts_v2.parallel, True)

    def test_update_url_count(self):
        compare = 5
        del nps_alerts_v2.sys.argv[1:]
        nps_alerts_v2.sys.argv.append("-u")
        nps_alerts_v2.sys.argv.append(compare)
        nps_alerts_v2.read_args()
        self.assertEqual(nps_alerts_v2.url_count, compare)

    def test_multi_update(self):
        in_file = "./nps_alerts_testing/TestReadFile.txt"
        out_file = "test_file.txt"
        url_count = 9
        del nps_alerts_v2.sys.argv[1:]
        nps_alerts_v2.sys.argv.append("-ipoPu")
        nps_alerts_v2.sys.argv.append(in_file)
        nps_alerts_v2.sys.argv.append(out_file)
        nps_alerts_v2.sys.argv.append(url_count)
        nps_alerts_v2.read_args()
        self.assertEqual(nps_alerts_v2.url_count, url_count)


class TestHTMLFileParser(unittest.TestCase):

    def test_handle_data(self):
        parser = nps_alerts_v2.HTMLFileParser()
        parser.feed("<html><h3 tabindex='0' aria-hidden='true' class='Alert-title'>TEST</h3>"
                    "<span tabindex='0'>This is a test</span></html>")
        compare = ['TEST', 'This is a test']
        self.assertEqual(parser.alerts, compare)

    def test_html_parser_manager(self):
        nps_alerts_v2.alerts = []
        nps_alerts_v2.html_files = [["Test Park", "<html><h3 tabindex='0' aria-hidden='true' "
                                                  "class='Alert-title'>TEST</h3><span tabindex='0'>"
                                                  "This is a test</span></html>"]]
        compare = ["Test Park", "TEST", "This is a test"]
        nps_alerts_v2.html_parser_manager()
        self.assertEqual(nps_alerts_v2.alerts[0], compare)


class TestGettingHTML(unittest.TestCase):

    def test_get_html_case1(self):
        park = ["Test Park", "file:./nps_alerts_testing/TestGetHTML1.txt"]
        container = []
        compare = [["Test Park", "THIS IS A TEST #1"]]
        nps_alerts_v2.get_html(park, container)
        self.assertEqual(container, compare)

    def test_get_html_case2(self):
        park = ["Test Park", "file:./nps_alerts_testing/TestGetHTML1.txt"]
        container = Queue()
        open_container = []
        compare = [["Test Park", "THIS IS A TEST #1"]]
        nps_alerts_v2.get_html(park, container)
        while not container.empty():
            open_container.append(container.get())
        self.assertEqual(open_container, compare)

    def test_sequential_html_manager(self):
        nps_alerts_v2.html_files = []
        nps_alerts_v2.parks = [["Test Park: 1", "file:./nps_alerts_testing/TestGetHTML1.txt"],
                               ["Test Park: 2", "file:./nps_alerts_testing/TestGetHTML2.txt"],
                               ["Test Park: 3", "file:./nps_alerts_testing/TestGetHTML3.txt"]]
        compare = [["Test Park: 1", "THIS IS A TEST #1"],
                   ["Test Park: 2", "THIS IS A TEST #2"],
                   ["Test Park: 3", "THIS IS A TEST #3"]]
        nps_alerts_v2.sequential_html_manager()
        self.assertEqual(nps_alerts_v2.html_files, compare)

    def test_parallel_html_worker(self):
        parks = [["Test Park: 1", "file:./nps_alerts_testing/TestGetHTML1.txt"],
                 ["Test Park: 2", "file:./nps_alerts_testing/TestGetHTML2.txt"],
                 ["Test Park: 3", "file:./nps_alerts_testing/TestGetHTML3.txt"]]
        container = []
        compare = [["Test Park: 1", "THIS IS A TEST #1"],
                   ["Test Park: 2", "THIS IS A TEST #2"],
                   ["Test Park: 3", "THIS IS A TEST #3"]]
        nps_alerts_v2.parallel_html_worker(parks, container)
        self.assertEqual(container, compare)

    def test_parallel_html_manager(self):
        nps_alerts_v2.html_files = []
        nps_alerts_v2.parks = [["Test Park: 1", "file:./nps_alerts_testing/TestGetHTML1.txt"],
                               ["Test Park: 2", "file:./nps_alerts_testing/TestGetHTML2.txt"],
                               ["Test Park: 3", "file:./nps_alerts_testing/TestGetHTML3.txt"]]
        compare = [["Test Park: 1", "THIS IS A TEST #1"],
                   ["Test Park: 2", "THIS IS A TEST #2"],
                   ["Test Park: 3", "THIS IS A TEST #3"]]
        nps_alerts_v2.url_count = 1
        nps_alerts_v2.parallel_html_manager()
        self.assertEqual(nps_alerts_v2.html_files, compare)


class TestListUpdates(unittest.TestCase):

    def test_clean_alerts(self):
        nps_alerts_v2.alerts = [["Test Name", "Test\n", "&", "Test\n", "This is a test\n"]]
        compare = [["Test Name", "Test & Test", "This is a test"]]
        nps_alerts_v2.clean_alerts()
        self.assertEqual(nps_alerts_v2.alerts, compare)


if __name__ == '__main__':
    unittest.main()
