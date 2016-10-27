import sys
from ftplib import FTP
from datetime import datetime, timedelta
from argparse import ArgumentParser

def parse_arguments():
	parser = ArgumentParser(description='Fetches latest rainrader  image from neo server')
	parser.add_argument('-u', '--url', help='url to grab from', default='data.knmi.nl',required=False)
	args = parser.parse_args()
	return args
	
def main():
	args = parse_arguments()
	uri = args.url
	d = datetime.today() - timedelta(days=1)
	filelist = []
	ftp = FTP(uri)
	ftp.login()
	ftp.cwd('download/radar_corr_accum_24h/1.0/noversion/'+str(d.year)+'/'+str(d.month)+'/'+str(d.day)+'/')
	ftp.dir('-t',filelist.append)
	filename = filelist[0].split()[8]
	
	ftp.retrbinary("RETR " + filename, open(filename,"wb").write)
	ftp.quit()

if __name__ == '__main__':
    status = main()
    sys.exit(status)