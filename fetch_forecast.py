import sys
from argparse import ArgumentParser
import requests	
import json
import csv

def parse_arguments():
    parser = ArgumentParser(description='Fetches latest weather forecast for next 10 days from wunderground')
    #key is based on the account: waterenvuurmanager@gmail.com
    parser.add_argument('-k', '--key', help='apikey for wunderground', default='be8a560b17cc78f1',
                        required=False)
    parser.add_argument('-o', '--outdir', help='output directory', default='./',
                        required=False)
    args = parser.parse_args()
    return args

def main():
	s = requests.Session()
	args = parse_arguments()
	key = args.key
	outdir = args.outdir
	uri = 'http://api.wunderground.com/api/'+key+'/forecast10day/q/NL/Amersfoort.json'
	s = requests.Session()
	response = s.get(uri)
	outfile= 'forecast.csv'
	data = json.loads(response.text)
	if ('error' in data['response']):
		print 'Error: ' + data['response']['error']['type'] + '  ' + data['response']['error']['description'] 
		return 1
	
	days = data['forecast']['simpleforecast']['forecastday']
	with open(outdir + '/' + outfile, 'wb') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=',')
		csvwriter.writerow([
				'period',
				'date',
				'Tlo',
				'Thi',
				'Havg',
				'Hmin',
				'Hmax',
				'qpf_allday',
				'qpf_day',
				'snow_allday',
				'snow_day',
				'snow_night',
				'Vmaxwind',
				'dirmaxwind',
				'Vavewind',
				'diravewind'
			])
		for day in days:
			csvwriter.writerow([
				day['period'],
				str(day['date']['year']) + '-' + str(day['date']['month']) + '-' + str(day['date']['day']),
				day['low']['celsius'],
				day['high']['celsius'],
				day['avehumidity'],
				day['minhumidity'],
				day['maxhumidity'],
				day['qpf_allday']['mm'],
				day['qpf_day']['mm'],
				day['snow_allday']['cm'],
				day['snow_day']['cm'],
				day['snow_night']['cm'],
				day['maxwind']['kph'],
				day['maxwind']['degrees'],
				day['avewind']['kph'],
				day['avewind']['degrees'],
			])
	print 'forecast written to ' + outdir + '/' + outfile
	print 'done'
		
	

if __name__ == '__main__':
    status = main()
    sys.exit(status)
