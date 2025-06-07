import csv
from csv import DictReader
from google import genai
#https://www.gov.uk/government/publications/recommended-open-standards-for-government/tabular-data-standard
#https://aistudio.google.com/app/apikey
"""
This project uses csv formats in the form of RFC 4180 open standard in line with the uk government
"""

class backend():
    """The main backend class which deals with setting up paramaters for the renderer."""
    def __init__(self):
        self.prompt = ""
        
    def harvest(file=None):
        """Gathers all the data from the csv file"""
        if file == None:
            return 
        
        with open(file,'r') as data:
            sep = ","
            keys = backend.Harvest_Headers(data, sep)
            values = backend.Harvest_values(data, sep)

        return keys, values

    def seperator(data):
        headers = next(data)
        for char in headers:
            if char == ";":
                return ";"
            elif char == ",":
                return ","

    def Harvest_Headers(data, sep):
        headers = next(data)
        headers = f"{headers[:-1]}{sep}"
        pointer_str = 0
        titles = []
        for i in range(len(headers)):
            if headers[i] == sep:
                titles.append(headers[pointer_str:i])
                pointer_str = i+1
        return titles
    
    def Harvest_values(data, sep=","):
        data = list(csv.reader(data))  # Convert iterator to a list
        values = []
        for line in data:  # Exclude the last line
            value = []
            if any(line):
                for val in line:
                    if val == "":
                        val = "None"
                    value.append(val)
                    
            values.append(value)
        return values