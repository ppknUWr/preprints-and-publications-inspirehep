import argparse
from xml.etree import ElementTree as ET
import urllib.request
import json
import unicodedata


def remove_accents(input_str):
    """Do obsłużenia znaków diakrytycznych w podanych autorach, ponieważ api obsluguje tylko format znaków ASCII."""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('utf-8')


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--author", dest="authors", required=True,
                        help="To search more than people use 'or' between authors e.g. 'Stephen Hawking or Richard Feynman \
                         or Albert Einstein'")
    parser.add_argument("-o", "--output", dest="output", type=str, default="site.html",
                        help="Give the name of output file with format .html e.g. 'site.html'")
    parser.add_argument("-s", "--size", dest="size", type=int,
                        help="Give number of publications, default it takes all of them.")
    parser.add_argument("-y", "--year", dest="year", type=str,
                        help="Enter the year. E.g --2019 means all years to 2019, 2019--2019 or 2019 means this one year, 2019-- means 2019 and upper")
    return parser.parse_args()


def get_data(authors, size=None, year=None):
    if authors[-4:] == ".txt":
        with open(authors, "r") as f:
            authors = " or ".join(f.read().splitlines())
    authors = remove_accents(authors) # Dodane w celu obsluzenia znakow diaktrycznych np. "ę" zamieni na "e" itp.
    name = 'a%20' + authors.replace(' ', '%20')  # dest=a, zamienia spacje na odpowiednie znaki

    inspirehep_profile = 'https://inspirehep.net/api/literature?sort=mostrecent&q=' + name
    if year is not None:  # data
        if '--' not in year:
            year = year + "--" + year
        inspirehep_profile += '&earliest_date=' + year

    if size is None:  # pobranie by poznac dlugosc
        data = json.loads(urllib.request.urlopen(inspirehep_profile + '&format=json').read())
        size = data['hits']['total']

    inspirehep_profile += "&size=" + str(size) + '&format=json '  # pobranie wlasciwe
    print(inspirehep_profile) # debug
    data = json.loads(urllib.request.urlopen(inspirehep_profile).read())
    return data


def parse_data(json_data):
    articles = []
    for hit in json_data['hits']['hits']:
        article = {}
        article['title'] = hit['metadata']['titles'][0]['title']
        article['date'] = hit['metadata']['earliest_date']
        article['link_to_article'] = 'https://inspirehep.net/literature/' + str(hit['metadata']['control_number'])
        if "arxiv_eprints" in hit['metadata'].keys():
            article['primary_arxiv_category'] = hit['metadata']['arxiv_eprints'][0]['categories'][0]
            article['arxiv_eprints'] = hit['metadata']['arxiv_eprints'][0]['value']
        authors_hit = []  # tablica autorow
        links_to_authors_hit = []  # tablica linkow autorow
        for author in hit['metadata']['authors']:  # autorow wiecej niz 1 dla publikacji
            authors_hit.append(author['first_name'] + ' ' + author['last_name'])
            if 'record' not in author:
                links_to_authors_hit.append("-")  # gdy nie ma linku dla autora
            else:
                links_to_authors_hit.append(author['record']['$ref'])
        article['authors'] = authors_hit
        article['links_to_authors'] = links_to_authors_hit
        if 'publication_info' in hit['metadata'].keys() and "journal_title" in hit['metadata']['publication_info'][
            0].keys():  # Dodanie na szybko sprawdzenia, czy zawiera "journal_title"
            pub_info = hit['metadata']['publication_info'][0]
            article['publication_info'] = "Published in: " + pub_info['journal_title'] + " " + pub_info[
                'journal_volume'] + " (" + str(pub_info['year']) + ") • "  # + pub_info['artid'] # do naprawienia artid
        articles.append(article)
    return articles


def to_html(articles, output_file):
    container = ET.Element('div')
    for article in articles:
        div = ET.Element('div')
        p_title = ET.Element('p')
        b_title = ET.Element('b')
        a_title = ET.Element('a', attrib={'href': article['link_to_article']})
        p_authors = ET.Element('p')
        span_date = ET.Element('span')
        span_arxiv = ET.Element('span')
        span_pub_info = ET.Element('span')

        span_comma = ET.Element('span')  # dodawanie elementu z przecinkiem
        span_comma.text = ", "

        div.append(p_title)  # dodaj tytul publikacji
        p_title.append(b_title)  # dodaj pogrubienie
        a_title.text = article['title']  # dodaj link do publikacji
        b_title.append(a_title)  # dodaj link do do znacznika b
        span_date.text = " (" + article['date'] + ")"
        if 'publication_info' in article.keys():
            span_pub_info.text = article['publication_info']
        if 'primary_arxiv_category' in article.keys():
            span_arxiv.text = "e-Print: " + article['arxiv_eprints'] + " [" + article['primary_arxiv_category'] + "]"
        else:
            span_arxiv.text = ""
        for i in range(len(article['links_to_authors'])):
            if i == 0:
                p_authors.text = "By "
            if article['links_to_authors'][i] != "-":
                a_authors = ET.Element('a', attrib={'href': "".join(article['links_to_authors'][i].split("/api"))})
                a_authors.text = article['authors'][i]
                p_authors.append(a_authors)
                if i != len(article['links_to_authors']) - 1:
                    p_authors.append(span_comma)
            else:
                span_out_authors = ET.Element('span')
                span_out_authors.text = article['authors'][i]
                p_authors.append(span_out_authors)
                if i != len(article['links_to_authors']) - 1:
                    p_authors.append(span_comma)

        p_authors.append(span_date)
        div.append(p_authors)
        div.append(span_pub_info)
        div.append(span_arxiv)
        container.append(div)
    ET.ElementTree(container).write(output_file, method='html')


if __name__ == '__main__':
    args = get_arguments()  # pobranie argumentow
    unparsed_data = get_data(args.authors, args.size, args.year)  # pobranie danych z api-s
    parsed_data = parse_data(unparsed_data)  # parsowanie danych z api
    to_html(parsed_data, args.output)  # export do html
