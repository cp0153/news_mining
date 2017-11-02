import requests
import datetime
import json

# POST https://language.googleapis.com/v1/documents:analyzeEntities?key=AIzaSyAh9uz0qNveHuiNYNBhjanf5gq86Su5rlo


url = 'https://language.googleapis.com/v1/documents:analyzeEntities?key=AIzaSyAh9uz0qNveHuiNYNBhjanf5gq86Su5rlo'

# v1/documents:analyzeEntities?key=AIzaSyAh9uz0qNveHuiNYNBhjanf5gq86Su5rlo


if __name__ == "__main__":
	with open('news_api/query_results.txt', 'r') as a, open('news_api/nat_list.txt', 'a') as b:
		for line in a:
			start_of_json = line.find('{')
			data = json.loads(line[start_of_json:])
			if 'articles' in data:
				articles = data['articles']
				for article in articles:
					content = article['description']
					document = json.dumps({'document': {'content': content, 'type': 'PLAIN_TEXT'}})
					r = requests.post(url, data=document)
					if r.status_code == 200:
						b.write(r.text)
						b.write('\n')
					else:
						print(r.text)
