#Name: Matthew Huh
#Geography 458 Lab 3

#imports necessary modules
from geopy import Nominatim
from bs4 import BeautifulSoup
import urllib2
import requests
import csv
from itertools import izip

from subprocess import call
import os
os.environ["GDAL_DATA"] = "C:\\OSGeo4W\\share\\gdal"
os.environ["GDAL_DRIVER_PATH"] = "C:\\OSGeo4W\\bin\\gdalplugins"
os.environ["PROJ_LIB"] = "C:\\OSGeo4W\\share\\proj"
os.environ["PATH"] = "C:\\OSGeo4W\\bin;"+os.environ["PATH"]+";C:\\OSGeo4W\\apps\\msys\\bin;C:\\OSGeo4W\\apps\\Python27\\Scripts"

#sets up workspace
import sys
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\ArcToolbox\\Scripts')
import arcpy
from arcpy import env
env.overwriteOutput = True
env.workspace = 'C:\\Users\\mhuh22\\PycharmProject\\untitled'

#file i/o
BASE_URL = "https://foursquare.com/top-places/seattle/"
category = BASE_URL + "best-places-coffee"
directory = 'C:\\Users\\mhuh22\\PycharmProject\\untitled'

#extracts and reads content
r = requests.get(category)
soup = BeautifulSoup(r.content)
venuename = soup.find_all("div", {"class": "name"})

#gathers lists for names, ratings, addresses, latitudes, and longitudes
venues=[]
ratings = []
location = []
latitude = []
longitude = []

#finds the names, ratings, and addresses from the page and appends them to the list
i=0
for item in venuename:
    if (i<9):
        venues.append(((item.contents[0].find_all("a",{"class":"venueLink"})[0].text).encode("utf-8"))[4:])
        ratings.append((item.contents[1].text).encode("utf-8"))
        location.append((item.contents[2].text).encode("utf-8"))
    else:
        venues.append(((item.contents[0].find_all("a",{"class":"venueLink"})[0].text).encode("utf-8"))[5:])
        ratings.append((item.contents[1].text).encode("utf-8"))
        location.append((item.contents[2].text).encode("utf-8"))
    i+=1

#extracts city and state data
citystate = "," + location[0].split(',')[1] + ", " + location[0].split(", ")[2]

#finds geocoder
geolocator = Nominatim()
j=0
for j in range (0,(len(location))):

    #removes special characters
    location[j] = location[j].split('(')[0]
    location[j] = location[j].split('#')[0] + citystate

    #finds latitude and longitude
    loc = geolocator.geocode(location[j])
    latitude.append(loc.latitude)
    longitude.append(loc.longitude)
    j+=1

#creates csv file and adds lists as fields
with open ('coffeetable.csv', 'wb') as csvfile:
    csv.writer(csvfile, lineterminator='\n').writerow(('venues', 'ratings', 'location', 'latitude', 'longitude'))
    writer = csv.writer(csvfile)
    writer.writerows(izip(venues, ratings, location, latitude, longitude))

arcpy.CreateFeatureclass_management(env.workspace, 'coffeepoints.shp', 'POINT',"","","",'WGS 1984')