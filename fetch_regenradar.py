import sys
import gdal
from osgeo import osr
from ftplib import FTP
from datetime import datetime, timedelta
from argparse import ArgumentParser
from netCDF4 import Dataset
import numpy as np

def parse_arguments():
	parser = ArgumentParser(description='Fetches latest rainrader  image from neo server')
	parser.add_argument('-u', '--url', help='url to grab from', default='data.knmi.nl',required=False)
	parser.add_argument('-o', '--outdir', help='output directory', default='./',required=False)
	args = parser.parse_args()
	return args
		
def main():
	args = parse_arguments()
	uri = args.url
	d = datetime.today() - timedelta(days=2)
	filelist = []
	#ftp = FTP(uri)
	#ftp.login()
	#ftp.cwd('download/radar_corr_accum_24h/1.0/noversion/'+str(d.year)+'/'+str(d.month)+'/'+str(d.day)+'/')
	#ftp.dir('-t',filelist.append)
	#for i, r in enumerate(filelist):
	#	filelist[i] = r.split()
	#filelist.sort(key = lambda x : x[8])
	#filelist.reverse()
	#filename = filelist[0][8]
	outdir = args.outdir
	#ftp.retrbinary("RETR " + filename, open(outdir+'/'+filename,"wb").write)
	#ftp.quit()
	filename = 'RAD_NL25_RAC_24H_201610300800.h5'
	rootgrp = Dataset(outdir+'/'+filename, "r", format="NETCDF4")
	data = np.array(rootgrp.groups['image1']['image_data'])

	x_pixels = 700  # number of pixels in x
	y_pixels = 765  # number of pixels in y
	PIXEL_SIZE = 1  # size of the pixel...        
	x_min = 0 #575694 - (700000/2)  
	y_max = -3649.979 #6819814 # + (765000/2)  # x_min & y_max are like the "top left" corner.
	proj_projection = '+proj=stere +lat_0=90 +lon_0=0 +lat_ts=60 +a=6378.14 +b=6356.75 +x_0=0 y_0=0'
	srs = osr.SpatialReference()
	srs.ImportFromProj4(proj_projection)
	wkt_projection = srs.ExportToWkt()
	#wkt_projection = 'PROJCS["unnamed",GEOGCS["unnamed ellipse",DATUM["WGS84",SPHEROID["unnamed",6378.14,298.1832632071011]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",90],PARAMETER["central_meridian",0],PARAMETER["scale_factor",1],PARAMETER["false_easting",0],PARAMETER["false_northing",0]]'
	driver = gdal.GetDriverByName('GTiff')
	
	dataset = driver.Create(
		outdir+'/'+filename.replace('.h5','.tif'),
		x_pixels,
		y_pixels,
		1,       
		gdal.GDT_Float32, )
	print y_max;
	dataset.SetProjection(wkt_projection)
	dataset.SetGeoTransform((x_min, PIXEL_SIZE, 0, y_max, 0, -PIXEL_SIZE))
	dataset.GetRasterBand(1).WriteArray(data)
	dataset.GetRasterBand(1).SetNoDataValue(65535)
	dataset.FlushCache()  # Write to disk.
		

if __name__ == '__main__':
    status = main()
    sys.exit(status)