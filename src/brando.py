import re
import json
from os.path import dirname, abspath
import utils
from souphelper.souputils import SoupHelper,getURL


def makeArticle(uri, _id):
    """ Arma el json de la noticia
    return <<dict_type>>. """


    noticia = {'_id':_id}
    html_article = SoupHelper(getURL(uri))

    # Fecha
    html_article.getBlock("^fecha$", 1)
    noticia.update({'fecha': str(html_article.block.text)})

    # Busco el titulo de la noticia
    html_article.getBlock("^encabezado$",1)
    titular = html_article.block.find(class_=re.compile("^titulo"))
    noticia.update({'titulo': str(titular.text)})

    # Busco y seteo el cuerpo de la noticia
    html_article.getBlockByID("^cuerpo", 1)
    noticia.update({'texto': str(html_article.block.text)})

    return noticia
def makeID(uri):
    """
    Aparentemente las uris de las noticias en la nacion tienen un ID asociado.
    se extrae solo el numero como tentativa de id, habria que sumar la fecha
    o calcular un timestamp de la notica. Otra opcion podria ser
    hacer un hash del texto o del primer parrafo de la noticia.
    """
    ONLY_NUMS = re.compile('[0-9]*').search
    try:
        return int(ONLY_NUMS(s_dat).group(0))
    except AttributeError:
        return -1
    except:
        return -2



if __name__ == "__main__":
    # por el momento creo el objeto tipo soup
    # dentro del metodo linksFrom, pero probablemente
    # en el futuro necesite seguir trabajando con el
    # ej: sacar el featured content.
    current_dir = dirname(abspath(__file__))
    work_dir = "{}/files/brando".format(dirname(current_dir))
    base_url="https://www.lanacion.com.ar"
    uri = "{}/revista-brando-t61735/".format(base_url)

    # Busca en la pagina principal, debo selecionar el bloque mas inmediato
    # que contiene los links y el bloque que contiene los links,
    # retorna un array con los links
    links = utils.linksFrom(uri, "^nota$", "^figure")
    true_links = utils.compareLinks(links, work_dir)

    for l in true_links:
        article_uri = "{}{}".format(base_url, l)
        _id = makeID(l)
        # armo el articulo basandome en el html del site
        article = makeArticle(article_uri, _id)
        # armo el json
        json_article = json.dumps(article, indent=4)
        # salvo el json usando el nombre del uri
        name_file = "{}/{}.json".format(work_dir, l.strip("/"))
        with open(name_file, 'w') as json_file:
            json_file.write(json_article)
        print (json_article)

