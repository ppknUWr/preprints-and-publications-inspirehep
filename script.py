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
                    help="Enter the year. E.g --2019 means all years to 2019, 2019--2019 means this one year, 2019-- means 2019 and upper")

args = parser.parse_args()
name = 'a%20' + args.a.replace(' ', '%20')
if args.y == None:
    date = ""
else:
    date = '&earliest_date=' + args.y
file = args.o
size = args.s
if size == None:
#data i size jeszcze
    inspirehep_profile = 'https://inspirehep.net/api/literature?q=' + name + date + '&format=json'
    data = json.loads(urllib.request.urlopen(inspirehep_profile).read())
    size = data['hits']['total']
inspirehep_profile = 'https://inspirehep.net/api/literature?q=' + name + date + "&sort=mostrecent&size=" + str(size) + '&format=json'
data = json.loads(urllib.request.urlopen(inspirehep_profile).read())
titles = []
links_to_articles = []
authors = []
links_to_authors = []
print(len(data['hits']['hits']))
for hit in data['hits']['hits']:
    titles.append(hit['metadata']['titles'][0]['title'])
    links_to_articles.append('https://inspirehep.net/literature/' + str(hit['metadata']['control_number']))
    authors_hit = []
    links_to_authors_hit = []
    for author in hit['metadata']['authors']:
        authors_hit.append(author['first_name'] + ' ' + author['last_name'])
        if 'record' not in author:
            links_to_authors_hit.append("-")
        else:
            links_to_authors_hit.append(author['record']['$ref'])
    authors.append(authors_hit)
    links_to_authors.append(links_to_authors_hit)
print(inspirehep_profile)
container = ET.Element('div')
for i in range(len(titles)):
    div = ET.Element('div')
    p_title = ET.Element('p')
    div.append(p_title)
    b_title = ET.Element('b')
    p_title.append(b_title)
    a_title = ET.Element('a', attrib={'href': links_to_articles[i]})
    a_title.text = titles[i]
    b_title.append(a_title)
    p_authors = ET.Element('p')
    for j in range(len(links_to_authors[i])):
        if(links_to_authors[i][j] != "-"):
            a_authors = ET.Element('a', attrib={'href': "".join(links_to_authors[i][j].split("/api"))})
            a_authors.text = authors[i][j]
            p_authors.append(a_authors)
        else:
            p_out_authors = ET.Element('p')
            p_out_authors.text = authors[i][j]
            p_authors.append(p_out_authors)
    div.append(p_authors)
    container.append(div)
ET.ElementTree(container).write(file, method='html')
