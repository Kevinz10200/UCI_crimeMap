# UCI_crimeMap
Generates HTML map with UCIPD data

Takes either a link to a remote PDF file hosted by UCIPD
or a downloaded PDF file stored locally.

Parses the table within with tabula-py library and saves
it as a csv file in order to delete duplicate rows.

Then calls google maps API to trade address to geo coordinates,
Saves a local copy to minimalize API calls.

Either reads local location data stored in JSON, or pings API
for geo coordinates.

Uses folium library to output a pretty map in HTML to visualize data.

# requirments:
folium      for generating a map in HTML
tabula-py   for parsing table from PDF file
pandas      for dataframe and processing
