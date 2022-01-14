import tabula
import pandas
from collections import defaultdict
import csv # for parsing csv files to remove duplicate rows

class pdf_parser:
    
    def __init__(self):
        # init database to empty pandas df
        self.df = 0
    
    # called by both ways of reading
    def finishReadingToDF(self):
        # remove duplicate columns, the reason for converting to csv
        with open('testlog.csv', 'r', newline='') as in_file, open('testlog1.csv', 'w', newline='') as out_file:
            reader = csv.reader(in_file)
            writer = csv.writer(out_file)
            seen = set() # set for fast O(1) amortized lookup
            for row in reader:
                row = tuple(row)
                if row in seen: continue # skip duplicate
                seen.add(row)
                writer.writerow(row)
        # read processed csv
        self.df = pandas.read_csv("testlog1.csv")
    
    # read from a local pdf of crimelog table
    def readFromPDF(self, local_location: str, pages: str='all'):
        # convert into a local csv file to make processing rows easier
        tabula.convert_into("testlog.pdf", "testlog.csv", output_format="csv", pages=pages)
        self.finishReadingToDF();
                
    # read from a linked pdf
    def readFromURL(self, link: str, pages: str='all'):
        tabula.convert_into(link, "testlog.csv", output_format="csv", pages=pages)
        self.finishReadingToDF();
    
    def processDataframe(self):
        #  flatten list of dataframes into a single dataframe
        # self.df = pandas.concat(self.df) # no longer needed due to using csv for processing
        # slice out first line of each page since it is the title to avoid 'Unnamed'
        self.df.columns = self.df.iloc[0]
        # reindex after change
        self.df = self.df.iloc[1:,].reindex()
    
    def describeData(self):
        # prints a short summary of the parsed data
        print(self.df.describe().to_string())
        
    def giveLocationData(self, uniqueAddress: bool = False) -> list:
        # returns a python list of addresses stored in the address.
        # will contain duplicates unless specified not to by uniqueAddress=True
        if uniqueAddress:
            return list(set(self.df['Location'].values.tolist()))
        else:
            return self.df['Location'].values.tolist()

    
    def giveData(self):
        # returns the pandas DataFrame of the data parsed, this returns the df in its current state
        return self.df
        
    
if __name__ == "__main__":
    parser = pdf_parser()
    
    parser.readFromPDF("testLog.pdf", 'all')
    
    parser.processDataframe()
    
    parser.describeData()
    
    print()
    
    addressList = parser.giveLocationData()
    print(f"{len(addressList)} addresses found.\n")
    for address in addressList:
        print(address)
    
    
    