import sys
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import requests	

def parse_arguments():
    parser = ArgumentParser(description='Fetches latest spot image from neo server')
    parser.add_argument('-u', '--url', help='url to grab from', default='https://secure.neography.nl/satellietbeeld.nl/download/index.php',
                        required=False)
    parser.add_argument('-f', '--filename', help='filename', default='latest',
                        required=False)
    parser.add_argument('-U', '--user', help='username for neography server', 
                        required=True)
    parser.add_argument('-P', '--password', help='password', 
                        required=True)
    args = parser.parse_args()
    return args


def parse_rows(rows):
    results = []
    for row in rows:
        table_data = row.find_all('td')
        if table_data:
            results.append([data.get_text() for data in table_data])
    return results

def main():
	s = requests.Session()
	args = parse_arguments()
	uri = args.url
	filename = args.filename

	username = args.user
	password = args.password
	
	payload = {
		'act': 'dologin',
		'ft_user': username,
		'ft_pass': password
	}
	
	r_login  = s.post(uri, data=payload)
	response = s.get(uri, params={'sort':'date'})
	soup = BeautifulSoup(response.text, "lxml")
	 
	
	try:
		table = soup.find('table')
		rows = table.find_all('tr')
	except AttributeError as e:
		try:
			soup.find_all("class", class_="login")
			print "Login seems to have failed"
			return 1
		except:
			raise ValueError("No valid data found in output")
	table_data = parse_rows(rows)
	for row in table_data:
		if len(row) == 4:
			filename = row[1] if filename == 'latest' else filename
			params = {'method':'getfile','file':filename}
			print 'Downloading ' + filename
			download = s.get(uri, params=params, stream=True)
			with open(filename, 'wb') as fd:
				for chunk in download.iter_content(1024):
					fd.write(chunk)
			exit()

if __name__ == '__main__':
    status = main()
    sys.exit(status)
