import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random

def generateData(): 

    listOfSources = ["bbc-news", "usa-today", "the-washington-post", "abc-news", "cnn"]
    l = len(listOfSources)-1
    ind1 = random.randint(0, l)
    
    print("Current source is : ", listOfSources[ind1])

    query_params = {
          "sources": listOfSources[ind1],
          "apiKey": "API_Key",
    }
    
    main_url = "https://newsapi.org/v2/everything"
    # fetching data in json format
    response = requests.get(main_url, params=query_params)

    data = response.json()['articles']
    res = []
    for d in data:
        res.append(d['title'])

    stopWordsSet = set(stopwords.words('english'))

    proccessedData = []
    import re
    tag = '[^a-zA-Z]'

    for x in res:
        list = word_tokenize(x)
        for y in list:
            y = re.sub(tag, '', y)
            if (y.lower() not in stopWordsSet and len(y) > 3):
                proccessedData.append(y.lower())

    sentence = " ".join(proccessedData)
    return sentence

if __name__ == "__main__":
    generateData()
