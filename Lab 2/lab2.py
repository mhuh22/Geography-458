
# coding: utf-8

# In[ ]:

# Name: Matthew Huh
# Geography 458
# Lab 2

#imports necessary access points
import sys
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\ArcToolbox\\Scripts')
import arcpy
from arcpy import env
env.workspace = "C:\\Users\\Matt\\Documents\\Geog458\\"
env.overwriteOutput = True
from subprocess import call


# In[2]:

#sets up input parameters
infile = arcpy.GetParameterAsText(0)
class_table = arcpy.GetParameterAsText(1)

#prompts user to enter the files
arcpy.AddMessage("Please enter the correct file")
arcpy.AddMessage("0: " + infile)
arcpy.AddMessage("1: " +  class_table)

#adds the population category field
arcpy.AddField_management(infile,"POP12CAT", "LONG")

#initializes cursor for the classification table
cursor1 = arcpy.da.SearchCursor(class_table, ["lowerbound", "upperbound", "value"])

#stores values from the classification table as an "array"
lowerbound = []
upperbound = []
value = []

#adds bounds and classification levels to lists
for row in cursor1:
    lowerbound.append(row[0])
    upperbound.append(row[1])
    value.append(row[2])
value.append(9999)

cursor2 =  arcpy.da.UpdateCursor(infile, ["POP2012", "ALANDM", "POP12CAT"])
for cur_row in cursor2:
    i = 0
    popdens = (cur_row[0]/cur_row[1]*1000000)
    
    #computes population density from population and area and compares it to the boundaries
    if (cur_row[1] == 0 or popdens > upperbound[-1]):
        cur_row[2] = value[-1]
    else:
        while int(popdens)>int(upperbound[i]):
            i+=1
        cur_row[2] = i + 1
    cursor2.updateRow(cur_row)
    
outfile = arcpy.CopyFeatures_management(infile,"copy.shp")

