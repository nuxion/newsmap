import re
from os.path import dirname, abspath
import utils
from souphelper.souputils import SoupHelper


def forLinks (links):
    """ Trabajo con un array de links
    para ir armando la informacion de cada una de las noticias.
    Params: array of links. """

    for l in links:
        articulo = SoupHelper(getURL(l))
        news = Article()
        news.setURL(l)
        articulo.getBlock("^fecha$", 1)
        news.setDate (articulo.block.text)
        # Busco el titulo de la noticia
        articulo.getBlock("^encabezado$",1)
        titular = articulo.block.find(class_=re.compile("^titulo"))
        news.setTitle(titular.text)

        # Busco y seteo el cuerpo de la noticia
        articulo.getBlockByID("^cuerpo", 1)
        news.setText(articulo.block.text)
        news.printNews()
        news.setDicts()
        news.jDump(news.fullDict)
        news.writeFile("json/")
        #articulo.linksInBlocks("^article-breadcrumb$")
        #linksBlock(articulo)
        #print (articulo.dictLinks.items())
        print ("------------------")


if __name__ == "__main__":
    # por el momento creo el objeto tipo soup
    # dentro del metodo linksFrom, pero probablemente
    # en el futuro necesite seguir trabajando con el
    # ej: sacar el featured content.
    current_dir = dirname(abspath(__file__))
    work_dir = "{}/files".format(dirname(current_dir))
    uri = "https://www.lanacion.com.ar/revista-brando-t61735/"

    # Busca en la pagina principal, debo selecionar el bloque mas inmediato
    # que contiene los links y el bloque que contiene los links,
    # retorna un array con los links
    links = utils.linksFrom(uri, "^nota$", "^figure")
    true_links = utils.compareLinks(links, work_dir)

    for l in true_links:
        print (l)

    #forLinks(t)
