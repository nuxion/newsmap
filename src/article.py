import json



class Article:
    def __init__(self):
        self.empty = ""
        self.topic = {}
        self.section = {}
        self.title = ""
        self.text = ""
        self.date = ""
        self.URL = ""
    def setURL (self, url):
        self.URL = str(url)
    def setDate (self, date):
        self.date = str(date)
    def setTitle (self, title):
        self.title = str(title)
    def setText (self, text):
        self.text = str(text)
    def setSection(self, links):
        """ Metodo que recibe un diccionario con el par link_path / text
        y devolera tambien un diccionario pero con un unico valor. """
        for (link_path, text) in links.items():
            if not re.search('^Pagina12$', text):
                if re.search('temas', link_path):
                    self.has_topic = True
                    self.topic[link_path] = text
                else:
                    self.section[link_path] = text
    def setDicts(self):
        self.extractID()
        self.cabecera = {"id":self.ID, "IDdate":self.date + "-" + self.ID}
        if self.topic:
            self.properties = {"section":self.section, "topic":self.topic, "date":self.date, "URL":self.URL}
        else:
            self.properties = {"section":self.section, "date":self.date, "URL":self.URL}
        self.info = {"titulo":self.title, "cuerpo":self.text}

        self.fullDict = {"header": self.cabecera, "properties":self.properties, "texts": self.info}

    def jDump (self, dumpDict):
        self.oJson=json.dumps(dumpDict, indent=4, ensure_ascii=False)
        print (self.oJson)

    def writeFile(self, pathjson):
        f = pathjson + self.cabecera["IDdate"] + ".json"
        with open (f, 'w') as json_data:
            json_data.write(self.oJson)

    def extractID(self):
        match = re.search('(?<=com\.ar\/)[0-9]+',self.URL)
        self.ID = str(match.group(0))
    def printNews(self):
        print ("URL: " + self.URL)
        print ("Title: " + self.title)
        print ("Section: " + str(self.section))
        if self.topic:
            print ("Topic: " + str(self.topic))
        print ("Date: " + self.date)
    """def writeToJson(self):
        #stuff
    def writeToDB(self):
    """"""

