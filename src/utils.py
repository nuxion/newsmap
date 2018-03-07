from souphelper.souputils import SoupHelper, getURL

def linksFrom (uri, allBlocks, element):
    """ Carga el site de pagina12.com.ar y busca todos los links
    de las noticias que quiero grabar, en este caso las principales.
    Params:
        uri: <<string>
        allBlocks: <<string>> bloque general donde estara el link.
        element: <<string>> class id del elemento especifico.

    Return: <<array>> de los links encontrados. """

    noticias = SoupHelper(getURL(uri))
    noticias.getAllBlocks(allBlocks)

    noticias.linksInElements(element)
    links = []
    for (link, text) in noticias.dictLinks.items():
        links.append(link)

    return links

def compareLinks(new_links, work_dir):
    """ Metodo que compara las dos listas de los nuevos y viejos links
    y devuelve un array con los links valido para hacer el scrap.
    A futuro separar read file y write file. """

    links_file = "{}/links.txt".format(work_dir)
    old_links = []
    with open(links_file, 'r') as lfile:
        for line in lfile:
            old_links.append(line)
    true_links = []

    for elem in new_links:
        try:
            old_links.remove(elem)
        except ValueError:
            true_links.append(elem)

    with open(links_file, 'a') as lfile:
        for l in true_links:
            lfile.write(l)

    return true_links







