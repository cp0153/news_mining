import requests
import datetime

api_key = '23b2fa848a2a45aa85546b463a7afc0a'

ARTICLES_URL = 'https://newsapi.org/v1/articles'
SOURCES_URL = 'https://newsapi.org/v1/sources'


if __name__ == "__main__":
	payload = {'language': 'en'}

	r = requests.get(SOURCES_URL, params=payload)

	if r.status_code != 200:
		print("error")
	else:
		# create dict of sources
		sources_list = r.json()['sources']

	with open('news_api/query_results.txt', 'a') as fp:

		for source in sources_list:
			payload = {'source': source['id'], 'apiKey': api_key, 'sortBy': 'top'}
			r = requests.get('https://newsapi.org/v1/articles', params=payload)
			
			if r.status_code == 200:
				fp.write('{}, '.format(datetime.datetime.now().isoformat()))
				fp.write(r.text)
				fp.write('\n')
			else:
				fp.write('{}, {}, {}\n'.format(datetime.datetime.now().isoformat(), r.status_code, r.text))
