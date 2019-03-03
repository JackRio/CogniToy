import re
import requests
import wikipedia
from bs4 import BeautifulSoup
response = {
  "output": {
    "generic": [],
    "intents": [
      {
        "intent": "Defination",
        "confidence": 0.5067428588867188
      }
    ],
    "entities": [
      {
        "entity": "Famous_Personalities",
        "location": [
          24,
          28
        ],
        "value": "alia_bhatt",
        "confidence": 1
      }
    ]
  }
}


error = 'There is currently no text in this page.'
search = response['output']['entities'][0]['value']
wiki_page = 'https://wiki.kidzsearch.com/wiki/'
wiki_page += search
html_page = requests.get(wiki_page)
soup = BeautifulSoup(html_page.text,'lxml')
name_box = soup.select('p')

para = name_box[0].getText()
if(para.find(error) == 0):
	para = wikipedia.summary(search,sentences = 5) 
elif((len(para) < 150) and (len(name_box) > 1)):
	para += '$' +  name_box[1].getText() 
	
para = re.sub(r'\[.*?\]','',para)
para = para.replace('  ','')	
print(para)