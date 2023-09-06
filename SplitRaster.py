#Author : Phummipat Daungklang
#Objective : this module is to split one raster to saveral raster using to identify number of row and number of columnn
#Parameter : file_name,output_dir,num_of_rows,num_of_cols
#Example use :
#   splitRaster = SplitRaster()
#   splitRaster = splitRaster.split(file_name,output_dir,prefix_filename,num_of_rows,num_of_cols)
#Example parameters value
#   file_name = "raster/ndvi.tif"
#   output_dir = "raster/ndvi_plit"
#   num_of_rows = 2
#   num_of_cols = 2

import sys
import string
import os
import arcpy
from arcpy.sa import *
import pythonaddins
import json

arcpy.env.overwriteOutput = True
def displayMessage(message):
    print message
    arcpy.AddMessage(message)

class SplitRaster():
    def split(self,file_name,output_dir,prefix_filename,num_of_rows,num_of_cols):
        try:
            raster = arcpy.sa.Raster(str(file_name))
            raster_extent = raster.extent
            xMax = raster_extent.XMax
            xMin = raster_extent.XMin
            yMax = raster_extent.YMax
            yMin = raster_extent.YMin

            xStep = float(xMax - xMin)/float(num_of_cols)
            yStep = float(yMax - yMin)/float(num_of_rows)
            
            xStart = xMin
            cellX = [xStart]
            colsCount = 0
            while colsCount < num_of_cols :
                xStart = xStart + xStep
                colsCount = colsCount + 1
                cellX.append(xStart)

            yStart = yMin
            cellY = [yStart]
            rowsCount = 0
            while rowsCount < num_of_rows :
                yStart = yStart + yStep
                rowsCount = rowsCount + 1
                cellY.append(yStart)
	    
            tile_id = 0
            displayMessage("Start Spliting Raster.")
			
            for row in range(len(cellY)-1):
                for col in range(len(cellX)-1):
                    xMin = cellX[col]
                    yMin = cellY[row]
                    xMax = cellX[col+1]
                    yMax = cellY[row+1]
                    bbox = str(xMin)+" "+str(yMin)+" "+str(xMax)+" "+str(yMax)

                    message = "Spliting tile number "+str(tile_id)
                    displayMessage(message)
					
                    try:
                        arcpy.Clip_management(str(file_name),
                                              bbox,str(output_dir)+"/"+str(prefix_filename)+str(tile_id)+".tif",
                                              "#", "#", "NONE")
                    except arcpy.ExecuteError:
                        displayMessage(arcpy.GetMessages(2))
					
                    tile_id = tile_id + 1

            displayMessage("Split Raster Success")
        except arcpy.ExecuteError:
            displayMessage(arcpy.GetMessages(2))


try:
    errCount = 0
    file_name_arg = arcpy.GetParameterAsText(0)
    file_name = os.path.abspath(file_name_arg)

    if (len(file_name) <= 0):
        errCount = errCount + 1

    output_dir = arcpy.GetParameterAsText(1)
    if (len(file_name) <= 0):
        errCount = errCount + 1

    prefix_filename = os.path.basename(file_name) 
    prefix_filename = str(os.path.splitext(prefix_filename)[0])+"_"

    num_of_cols = 0
    if (len(arcpy.GetParameterAsText(2)) <= 0):
        errCount = errCount + 1
    else:
        num_of_cols = int(arcpy.GetParameterAsText(2))
            
    num_of_rows = 0 
    if (len(arcpy.GetParameterAsText(3)) <= 0):
        errCount = errCount + 1
    else:
        num_of_rows = int(arcpy.GetParameterAsText(3))

    if (errCount > 0):
        displayMessage("Please Identify all of parameters,\nUser only use this module via ArcMap")
    else:
        splitRaster = SplitRaster()
        splitRaster.split(file_name,output_dir,prefix_filename,num_of_rows,num_of_cols)
            
except arcpy.ExecuteError:
    displayMessage(arcpy.GetMessages(2))


