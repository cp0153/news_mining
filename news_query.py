import requests
import json
from pymongo import MongoClient
import datetime
from pprint import pprint
api_key = '23b2fa848a2a45aa85546b463a7afc0a'

ARTICLES_URL = 'https://newsapi.org/v1/articles'
SOURCES_URL = 'https://newsapi.org/v1/sources'

# nat_url = 'https://language.googleapis.com/v1/documents:analyzeEntities?key=AIzaSyAh9uz0qNveHuiNYNBhjanf5gq86Su5rlo'
nat_url = 'https://language.googleapis.com/v1/documents'
nat_url_key = 'AIzaSyAh9uz0qNveHuiNYNBhjanf5gq86Su5rlo'


def nat_query(article, query):
    if 'description' in article:
        url = nat_url + ':' + query + '?key=' + nat_url_key
        content = article['description']
        document = json.dumps({'document': {'content': content, 'type': 'PLAIN_TEXT'}})
        r = requests.post(url, data=document)
        if r.status_code == 200:
            return r.json()
        else:
            print(r.text, url)
            return r.json()


if __name__ == "__main__":
    payload = {'language': 'en'}

    r = requests.get(SOURCES_URL, params=payload)

    if r.status_code != 200:
        print("error")
        exit()
    else:
        # create dict of sources
        sources_list = r.json()['sources']

        client = MongoClient()
        db = client.news
        news_articles = db.news_articles

        for source in sources_list:
            payload = {'source': source['id'], 'apiKey': api_key, 'sortBy': 'top'}
            r = requests.get('https://newsapi.org/v1/articles', params=payload)

            if r.status_code == 200:
                articles = r.json()['articles']
                for article in articles:
                    article['query_date'] = datetime.datetime.now()
                    article['analyzeEntities'] = nat_query(article, 'analyzeEntities')
                    article['analyzeEntitySentiment'] = nat_query(article, 'analyzeEntitySentiment')
                    article['analyzeSentiment'] = nat_query(article, 'analyzeSentiment')
                    article['analyzeSyntax'] = nat_query(article, 'analyzeSyntax')
                    article['classifyText'] = nat_query(article, 'classifyText')
                    pprint(article)
                    post_id = news_articles.insert_one(article).inserted_id
