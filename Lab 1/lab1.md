

```python


#imports the only two input files
censusblocks=("C:\\Users\\Matt\\Downloads\\Geog_458\\saep_bg10.shp")
countynames=("C:\\Users\\Matt\\Downloads\\Geog_458\\WashingtonFIPS.dbf")

#Creates search cursor for both files
cursor1 = arcpy.da.SearchCursor(countynames, ["FIPSCounty", "COUNTYNAME"])
cursor2 = arcpy.da.SearchCursor(censusblocks, "*")

# "SHAPE@"

#Creates geojson files
for row in cursor1:    
    #creates empty shapefile for each county
    if arcpy.Exists('C:\\Users\\Matt\\Downloads\\Geog_458\\shapefiles\\' + row[1]+'.shp'):
        arcpy.Delete_management('C:\\Users\\Matt\\Downloads\\Geog_458\\shapefiles', row[1]+'.shp')
    countyshape = arcpy.CreateFeatureclass_management('C:\\Users\\Matt\\Downloads\\Geog_458\\shapefiles', row[1] + '.shp', "POLYGON", "C:\\Users\\Matt\\Downloads\\Geog_458\\saep_bg10.shp")
    cursor3 = arcpy.da.InsertCursor(countyshape, "*")
    
    #copies row from countynames and adds them to the new shapefile
    for now in cursor2:
        if row[0] == now[0]:
            cursor3.insertRow(now)
    del cursor3
    
    call(['C:\\OSGeo4W\\bin\\ogr2ogr',
        '-f','GeoJSON','-t_srs','WGS84',
        '-s_srs','EPSG:2927',
        'C:\\Users\\Matt\\Downloads\\Geog 458\\geojson\\' + row[1] + '.geojson',
        'C:\\Users\\Matt\\Downloads\\Geog 458\\shapfiles\\' + row[1] + '.shp'])
```


    ---------------------------------------------------------------------------

    ExecuteError                              Traceback (most recent call last)

    <ipython-input-3-36520d077380> in <module>()
         16     if arcpy.Exists('C:\\Users\\Matt\\Downloads\\Geog_458\\shapefiles\\' + row[1]+'.shp'):
         17         arcpy.Delete_management('C:\\Users\\Matt\\Downloads\\Geog_458\\shapefiles', row[1]+'.shp')
    ---> 18     countyshape = arcpy.CreateFeatureclass_management('C:\\Users\\Matt\\Downloads\\Geog_458\\shapefiles', row[1] + '.shp', "POLYGON", "C:\\Users\\Matt\\Downloads\\Geog_458\\saep_bg10.shp")
         19     cursor3 = arcpy.da.InsertCursor(countyshape, "*")
         20 
    

    C:\Program Files (x86)\ArcGIS\Desktop10.3\arcpy\arcpy\management.py in CreateFeatureclass(out_path, out_name, geometry_type, template, has_m, has_z, spatial_reference, config_keyword, spatial_grid_1, spatial_grid_2, spatial_grid_3)
       1805         return retval
       1806     except Exception, e:
    -> 1807         raise e
       1808 
       1809 @gptooldoc('CreateFishnet_management', None)
    

    ExecuteError: Failed to execute. Parameters are not valid.
    ERROR 000732: Feature Class Location: Dataset C:\Users\Matt\Downloads\Geog_458\shapefiles does not exist or is not supported
    Failed to execute (CreateFeatureclass).
    



```python
# Name: Matthew Huh
# Geography 458
# Lab 1

#imports necessary access points
import sys
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\ArcToolbox\\Scripts')
import arcpy
from arcpy import env
env.workspace = 'C:\\Users\\Matt\\Downloads\\Geog_458\\shapefiles'
env.overwriteOutput = True
from subprocess import call
import os
os.environ["GDAL_DATA"] = "C:\\OSGeo4W\\share\\gdal"
os.environ["GDAL_DRIVER_PATH"] = "C:\\OSGeo4W\\bin\\gdalplugins"
os.environ["PROJ_LIB"] = "C:\\OSGeo4W\\share\\proj"
os.environ["PATH"] = "C:\\OSGeo4W\\bin;"+os.environ["PATH"]+";C:\\OSGeo4W\\apps\\msys\\bin;C:\\OSGeo4W\\apps\\Python27\\Scripts"
```


```python
#re-creates cursors to search for county id's
cursor1 = arcpy.da.SearchCursor(countynames, ["FIPSCounty", "COUNTYNAME"])
cursor2 = arcpy.da.SearchCursor(censusblocks, ["COUNTYFP10","POP2013"])

#creates 2 lists, population and associated county name
poplist=[0]
countylist = []

#creates population total for each county
for row in cursor1:
    county = row[0]
    population = 0
    
    #adds to county population total if it is in the same county
    for now in cursor2:
        if row[0] == now[0]:
            population+=now[1]
        else:
            break
            
    #resets the counter to move on to the next county
    i=0
    
    #adds items to the list by checking the numbers from largest to smallest, adding them in the correct index
    while (poplist[i]>population):
        i+=1
    poplist.insert(i,int(population))
    countylist.insert(i,row[1])
 
#deletes placeholder
del poplist[-1]

#prints the results
for j in range(10):
    print str(j+1) + ") \t" + countylist[j] + " County Population: \t" + str(poplist[j])    
```

    1) 	King County Population: 	1980645
    2) 	Pierce County Population: 	812568
    3) 	Snohomish County Population: 	729395
    4) 	Spokane County Population: 	479204
    5) 	Clark County Population: 	433535
    6) 	Thurston County Population: 	259293
    7) 	Kitsap County Population: 	252586
    8) 	Yakima County Population: 	246176
    9) 	Whatcom County Population: 	204582
    10) 	Benton County Population: 	181005
    
