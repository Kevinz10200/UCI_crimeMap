import folium
from folium.plugins import MarkerCluster

import pandas
import io

class Mapper():
    def __init__(self, coordinateDict: dict, original_df):
        # coordinateDict = {str Address: {str ;at: float, str: lng}}
        # original_df is the dataframe parsed previously, with all the data from UCIPD's pdf
        # turn dict of address:coord_dicts to list of 3-tuples for conversion to pandas df
        addressList = [(address, coord_dict['lat'], coord_dict['lng']) for address,coord_dict in coordinateDict.items()]
        
        print(addressList)
        
        #self.df = pandas.DataFrame(addressList, columns=["Location", "Latitude", "Longitude"])
        
        # make shallow copy of original df
        self.df = original_df
        self.df['Latitude'] = 0.0
        self.df['Longitude'] = 0.0
        self.df.reset_index(drop=True)
        #print(self.full_df.to_string())
        
        #print()
        print(self.df)
        
        print()
        # insert lat and lng data by looking up location from coordinateDict
        for i, _ in self.df.iterrows():
            lookupAddress = self.df.at[i, 'Location']
            self.df.at[i, 'Latitude'] = coordinateDict[lookupAddress]['lat']
            self.df.at[i, 'Longitude'] = coordinateDict[lookupAddress]['lng']
        
        print()
        print(self.df.to_string())
    
    
    # returns the address coordinate dataframe
    def getDF(self):
        return self.df
    
    
    def generateMap(self):
        # generate center with mean of all coordinates
        self.map = folium.Map(location=self.df[["Latitude", "Longitude"]].mean().to_list(), zoom_start=12)
        
        # display overlapping pins as clusters
        pin_cluster = MarkerCluster().add_to(self.map)
        
        for _, row in self.df.iterrows():
            # generate what will be displayed in the popup
            htmlText = "<b>Location:</b> " + row['Location'] \
                    + " <br><b>Case #:</b> " + row['Case #'] \
                    + " <br><b>Nature:</b> " + row['Nature']
                    
            iframe = folium.IFrame(htmlText)
            popup = folium.Popup(iframe, min_width=250, max_width=1000)
            
            location = (row["Latitude"], row["Longitude"])
            folium.Marker(location=location,
                              popup = popup,
                              tooltip=row['Nature']).add_to(pin_cluster)
    
    def outputMapToHTML(self, filename: str) -> None:
        if filename[-5:] == ".html":
            self.map.save(filename)
        else:
            self.map.save(filename + ".html")
            