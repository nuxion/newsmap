import json
import re
from souphelper.souputils import SoupHelper, getURL


#uri2 = "https://www.pagina12.com.ar/16889-el-poder-de-la-memoria"
#pagina = SoupHelper(getURL(uri2))
#pagina.getBlock("^article-date$", 1)

def linksFrom (uri):
    """ Carga el site de pagina12.com.ar y busca todos los links
    de las noticias que quiero grabar, en este caso las principales. 
    Params: str uri 
    Return: array of links. """
    #uri = "https://www.pagina12.com.ar"
    site = SoupHelper(getURL(uri)) 
    site.getBlock("^block-articles$", 1)
    noticias = SoupHelper(str(site.block)) 
    noticias.getAllBlocks("^article-body$")
    noticias.linksInBlocks("^article-title")
    links = []
    for (link, text) in noticias.dictLinks.items():
        links.append(link)
    return links

def forLinks (links):  
    """ Trabajo con un array de links
    para ir armando la informacion de cada una de las noticias. 
    Params: array of links. """
    
    for l in links:
        # Necesito validar si el link es link a un "tema"
        # o a una noticia 
        m = re.search('temas', l)
        if re.search('temas', l):
            print ("Es un tema")
        else: 
            # tengo la url concreta de la noticia
            # empiezo a trabajar con ella
            articulo = SoupHelper(getURL(l))
            news = Article()
            news.setURL(l)
            # Obtengo la cabecera de la noticia 
            # de donde sacare seccion y fecha
            articulo.getBlock("^article-info$", 1) 
            # Consigo la seccion a la que pertenece el articulo
            links = linksBlock(articulo.block)
            # Elimino links vacios, y seteo la seccion
            # y el tema si es que hay:
            news.setSection(links)
            news.setDate (articulo.findAttrs("time", "datetime"))
            # Busco el titulo de la noticia
            articulo.getBlock("^article-titles$",1)
            titular = articulo.block.find(class_=re.compile("^article-title$"))   
            news.setTitle(titular.text)
            # Busco y seteo el cuerpo de la noticia
            articulo.getBlock("^article-text$", 1) 
            news.setText(articulo.block.text)
            news.printNews()
            news.setDicts()
            news.jDump(news.fullDict)
            news.writeFile("json/")
            #articulo.linksInBlocks("^article-breadcrumb$")
            #linksBlock(articulo)
            #print (articulo.dictLinks.items())
        print ("------------------")

 
        
def linksBlock (soup):
   """ TEMPORAL
   Como linksInBlocks() solo trae el primer link encontrado
   se realizó un nuevo metodo para que busque todos los links. 
   Recibe un objeto del tipo SoupTag 
   y devuelve un objeto del tipo Dict. """
   
   #print (soup) # debug
   sresult = soup.find_all("a") # .attrs['href'] 
   links={}
   for s in sresult:
       links[s.attrs['href']]= s.text
       #if not re.search('^\/$',s.attrs['href']):
       #    print ("####")
       #    print (s.text)
       #    print (s.attrs['href'])
       #    print ("####")
   #print (links.items())
   return links

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
   """     
        
if __name__ == "__main__":
    # por el momento creo el objeto tipo soup 
    # dentro del metodo linksFrom, pero probablemente
    # en el futuro necesite seguir trabajando con el 
    # ej: sacar el featured content.
    links = linksFrom("https://www.pagina12.com.ar") 
    # debug
    for l in links:
        print (l)
    forLinks(links)
        
