# modules
import toCoord
import pdf_parser
import Mapper

# libraries
import json # for parsing string of saved dict back into dict
import sys # for exiting gracefully

def main():
    global useAPI

    print('Running main')
    
    print("Reading PDF from local location...")
    
    parser = pdf_parser.pdf_parser()
    
    parser.readFromPDF("testLog.pdf", 'all')
    
    print("Finished Reading.")
    
    print("Processing data...\n")
    parser.processDataframe()
    
    # 
    address_list = parser.giveLocationData()
    
    # prints a short summary
    print("Short Summary:")
    parser.describeData()
    
    # my address for your coordinates
    toCoordinates = toCoord.toCoord()
    
    # enable if requesting data from maps api
    if useAPI:
        print("\nUsing API for address to coordinates")
        location_dict = toCoordinates.encodeURL(address_list)
    else: # else load local cached coords
        print("\nUsing locally cached address / coordinate data")
        location_dict = loadLocalCoord()
    # how many addresses loaded
    addressCount = len(location_dict)
    
    print("\ndata dictionary ready for mapping;")
    print(f"{addressCount} unique locations ready.\n")
    
    #print(location_dict)
    
    # mapper section
    mapper = Mapper.Mapper(location_dict, parser.df)
    # dataframe of address and coordinates ready
    print("Dataframe with appended coordinate columns ready.")
    
    print("Generating map")
    mapper.generateMap()
    print("Writing to HTML file")
    mapper.outputMapToHTML("1-7-2022")
    print("HTML file outputted.")
    
    print("exiting (0)")
    sys.exit(0)
    
    
def loadLocalCoord():
    with open("coords.txt") as file:
        address_data = file.read()
    # use json lib to turn str to dict
    return json.loads(address_data)
    


if __name__ == "__main__":
    # determines if to ping API for coords or load cached local file to prevent overuse of API
    global useAPI
    useAPI = False
    
    main()
    
    
    
    