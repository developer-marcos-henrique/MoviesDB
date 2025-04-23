from bs4 import BeautifulSoup
import json

class filters:
    def __init__(self, data):
        self.data = data
        self.output = []

    def process(self):
        for x in self.data:
            match x[0]:
                case "9animetv":
                    tmp = [x[0], []]

                    html = BeautifulSoup(x[1], "html.parser").select("div[id='main-content']  h3.film-name a")

                    for content in html:
                        name = content.get_text()
                        url = content['href']

                        
                        tmp[1].append((name, url))
                        self.output.append(tmp)

                case "aniwatch":
                    tmp = [x[0], []]

                    html = BeautifulSoup(x[1]['html'], "html.parser").select("a")

                    for content in html:
                        url = content['href']
                        name = content.select_one("h3.dynamic-name")
                        
                        if name:
                            name = name.get_text()

                        tmp[1].append((name, url))
                        self.output.append(tmp)

                case "animefire":
                    tmp = [x[0], []]
                    
                    for content in x[1]:
                        url = content[5]
                        name = content[0]

                        tmp[1].append((name, url))
                        self.output.append(tmp)


                case "animesbr":
                    tmp = [x[0], []]

                    html = BeautifulSoup(x[1], "html.parser").select("div.search-page div.result-item article div.details a")

                    for i in html:
                        name = i.get_text()
                        url = i['href']

                        tmp[1].append((name, url))
                        self.output.append(tmp)
                
                case "goyabu":
                    tmp = [x[0], []]

                    if "error" in x[1].keys():
                        continue
                    
                    for i in x[1].items():
                        name = i[1]['title']
                        url = i[1]['url']

                        tmp[1].append((name, url))
                        self.output.append(tmp)
                        
        return self.output