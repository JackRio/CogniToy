import re
import requests
import wikipedia
from bs4 import BeautifulSoup


def search(response):
	error = 'There is currently no text in this page.'
	search = response['output']['entities'][0]['value']
	wiki_page = 'https://wiki.kidzsearch.com/wiki/'
	wiki_page += search
	html_page = requests.get(wiki_page)
	soup = BeautifulSoup(html_page.text,'lxml')
	for table in soup.find_all("table"):
		table.extract()
	name_box = soup.select('p')

	para = name_box[0].getText()
	if(para.find(error) == 0):
		para = wikipedia.summary(search,sentences = 5) 
	elif((len(para) < 150) and (len(name_box) > 1)):
		para += '$' +  name_box[1].getText() 
		
	para = re.sub(r'\[.*?\]','',para)
	para = para.replace('  ','')
	return para	
