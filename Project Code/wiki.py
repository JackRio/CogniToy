import wikipedia
print (wikipedia.summary("Wikipedia"))



wikisearch = input("About what you want to search on wiki:")
page = wikipedia.summery(wikisearch,sentance = 2)
print(page.content)