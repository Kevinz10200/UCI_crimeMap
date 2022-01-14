import json
import urllib
import requests


class toCoord:
    # init tokens and other constants
    maps_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    AUTH_KEY = "your API key goes here"
    
    # default constructor
        
    def encodeURL(self, addressList) -> dict:
        # given a list of addresses, output a dict in the form of:
        # dict{"address": {'lat': coord, 'lng': coord}}
        # the value can be linked to multiple lists
        
        outDict = {}
                
        for address in addressList:
            parameters = {
                "address": self.processAddress(address),
                "key": self.AUTH_KEY 
                }
            
            encodedURL = f"{self.maps_url}{urllib.parse.urlencode(parameters)}"
            outDict[address] = self.exchangeCoord(encodedURL)
            
        # save locally to not overuse api
        self.exportCoordinates(outDict)
            
        return outDict
    
    def processAddress(self, fullAddress: str) -> str:
        # slices address to only include starting from a street number
        # this minimalizes bad returns from API
        # also appends CA to make sure it is in California
        # ex: East Campus Parking Structure, 670 California Av, Irvine
        # turns into 670 California Av, Irvine, CA
        # if no street number present, it will return the address as-is
        for i,character in enumerate(fullAddress):
            if (character.isdigit()):
                return fullAddress[i:] + ", CA", # append state to end in case identical address exists elsewhere
        # return as-is
        return fullAddress + ", CA"
    
    def exchangeCoord(self, url):
        req = requests.get(url)
        
        # turn bytes into dict
        request_content = json.loads(req.content)
        
        # only interested in lat and lng coords
        request_content = request_content.get("results")[0].get("geometry").get("location")
        
        return request_content # returns a dict of coordinates
    
    
    def exportCoordinates(self, data):
        # writes a local cache of returned coordinates
        with open('coords.txt', 'a') as outfile:
            json.dump(data, outfile)
        
        
        
if __name__ == "__main__":
    pass
    
    
    
    
    
    
    