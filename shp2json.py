#pip install PyShp
import shapefile
from json import dumps

shp_files = ["Point_Buffer.shp"] #path of shapefiles

for shp_file in shp_files:
	# read the shapefile
	reader = shapefile.Reader(shp_file)
	fields = reader.fields[1:]
	field_names = [field[0] for field in fields]
	buffer = []
	for sr in reader.shapeRecords():
		atr = dict(zip(field_names, sr.record))
		geom = sr.shape.__geo_interface__
		buffer.append(dict(type="Feature", \
		geometry=geom, properties=atr)) 
	   
		# write the GeoJSON file
	json_file = shp_file.replace("shp", "json")
	geojson = open(json_file, "w")
	geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
	geojson.close()
	
print("the geojson are generated !");