import argparse
import sys
from xml.etree import ElementTree as ET
import urllib.request, json
import itertools

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--author", dest="a", required=True,
                    help="To search more than people use 'or' between authors e.g. 'Stephen Hawking or Richard Feynman \
                     or Albert Einstein'")
parser.add_argument("-o", "--output", dest="o", type=str, default="site.html",
                    help="Give the name of output file with format .html e.g. 'site.html'")
parser.add_argument("-s", "--size", dest="s", type=int,
                    help="Give number of publications, default it takes all of them.")
parser.add_argument("-y", "--year", dest="y", type=str,
                    help="Enter the year. E.g --2019 means all years to 2019, 2019--2019 or 2019 means this one year, 2019-- means 2019 and upper")

args = parser.parse_args()                  # rozbicie
file = args.o                               # nazwa pliku do jakiego trafi

if args.a[-4:] == ".txt":
    with open(args.a, "r") as f:
        args.a = " or ".join(f.read().splitlines())
name = 'a%20' + args.a.replace(' ', '%20')  # dest=a, zamienia spacje na odpowiednie znaki

inspirehep_profile = 'https://inspirehep.net/api/literature?sort=mostrecent&q=' + name
if args.y != None:                                      # data
    if len(args.y) == 4:
        args.y = args.y + "--" + args.y
    inspirehep_profile += '&earliest_date=' + args.y

size = args.s
if size == None:                                        # pobranie by poznac dlugosc
    data = json.loads(urllib.request.urlopen(inspirehep_profile + '&format=json').read())
    size = data['hits']['total']

inspirehep_profile += "&size=" + str(size) + '&format=json '                        # pobranie wlasciwe
data = json.loads(urllib.request.urlopen(inspirehep_profile).read())

# tablice na dane
titles = []
links_to_articles = []
authors = []                            # tablica tablic autorow
links_to_authors = []                   # tablica tablic linkow autorow

for hit in data['hits']['hits']:
    titles.append(hit['metadata']['titles'][0]['title'])
    links_to_articles.append('https://inspirehep.net/literature/' + str(hit['metadata']['control_number']))
    authors_hit = []
    links_to_authors_hit = []
    for author in hit['metadata']['authors']:   # autorow wiecej niz 1 dla publikacji
        authors_hit.append(author['first_name'] + ' ' + author['last_name'])
        if 'record' not in author:
            links_to_authors_hit.append("-")    # gdy nie ma linku dla autora
        else:
            links_to_authors_hit.append(author['record']['$ref'])
    authors.append(authors_hit)
    links_to_authors.append(links_to_authors_hit)

container = ET.Element('div')
for i in range(len(titles)):
    div = ET.Element('div')
    p_title = ET.Element('p')
    b_title = ET.Element('b')
    a_title = ET.Element('a', attrib={'href': links_to_articles[i]})
    p_authors = ET.Element('p')

    div.append(p_title)         # dodaj tytul publikacji
    p_title.append(b_title)     # dodaj pogrubienie
    a_title.text = titles[i]    # dodaj link do publikaji
    b_title.append(a_title)     # dodaj link do do znacznika b

    for j in range(len(links_to_authors[i])):
        if j == 0:
            p_authors.text = "By "
        if links_to_authors[i][j] != "-":
            a_authors = ET.Element('a', attrib={'href': "".join(links_to_authors[i][j].split("/api"))})
            if j == len(links_to_authors[i]) - 1:
                # zrobic zeby kropki i przeciniki byly w p a nie a
                a_authors.text = authors[i][j] + "."
            else:
                a_authors.text = authors[i][j] + ", "
            p_authors.append(a_authors)
        else:
            if j == len(links_to_authors[i]) - 1:
                span_out_authors = ET.Element('span')
                span_out_authors.text = authors[i][j] + ", "
                p_authors.append(span_out_authors)
    div.append(p_authors)
    container.append(div)
ET.ElementTree(container).write(file, method='html')
