import sys
import gdal
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
	ftp = FTP(uri)
	ftp.login()
	ftp.cwd('download/radar_corr_accum_24h/1.0/noversion/'+str(d.year)+'/'+str(d.month)+'/'+str(d.day)+'/')
	ftp.dir('-t',filelist.append)
	for i, r in enumerate(filelist):
		filelist[i] = r.split()
	filelist.sort(key = lambda x : x[8])
	filelist.reverse()
	filename = filelist[0][8]
	outdir = args.outdir
	ftp.retrbinary("RETR " + filename, open(outdir+'/'+filename,"wb").write)
	ftp.quit()
	
	rootgrp = Dataset(outdir+'/'+filename, "r", format="NETCDF4")
	data = np.array(rootgrp.groups['image1']['image_data'])

	x_pixels = 700  # number of pixels in x
	y_pixels = 765  # number of pixels in y
	PIXEL_SIZE = 1000  # size of the pixel...        
	x_min = 576457 - (700000/2)  
	y_max = 6818515 + (765000/2)  # x_min & y_max are like the "top left" corner.
	wkt_projection = 'PROJCS["unnamed",GEOGCS["unnamed ellipse",DATUM["unknown",SPHEROID["unnamed",6378.14,298.1832632071011]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",60],PARAMETER["central_meridian",0],PARAMETER["scale_factor",1],PARAMETER["false_easting",0],PARAMETER["false_northing",0]]'
	
	driver = gdal.GetDriverByName('GTiff')
	
	dataset = driver.Create(
		outdir+'/'+filename.replace('.h5','.tif'),
		x_pixels,
		y_pixels,
		1,       
		gdal.GDT_Float32, )
	
	dataset.SetGeoTransform((x_min, 1000, 0, y_max, 0, -1000))  
	
	dataset.SetProjection(wkt_projection)
	dataset.GetRasterBand(1).WriteArray(data)
	dataset.FlushCache()  # Write to disk.
		

if __name__ == '__main__':
    status = main()
    sys.exit(status)