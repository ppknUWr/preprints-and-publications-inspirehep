# preprints-and-publications-inspirehep

## Podział prac:
- jedna osoba zajmie się pobraniem danych od użytkownika np:
	python script.py -a "Remigiusz Durka or Maciej Matyka" -o site.html
	python script.py --authors autours.txt -y "2020 or 2019"

[-a,--authors] - string taki jak w przykładzie lub plik w formacie txt.
[-y, --year] - użytkownik podaje konkretny rok, lata lub przedział czasowy używając przy tym operatorów logicznych(<, <=, >, >=, or). Jest to argument niewymagany, więc jeśli użytkownik go nie użyje to domyślnie zwróci całą historie.
[-o,--output] - użytkownik podaje nazwe pliku html (np. "site.html") lub ścieżke (np."/home/usr/site.html).

- druga osoba zajmie się pobraniem danych z api wg. parametrów, a następnie ich zparsowaniem. Najlepiej jakby była to lista słowników, 
gdzie każdy słownik będzie zawierał: tytuł, link do artykułu, autora/autorów, link do autorów na inspirehtp oraz date (earliest_date).
Przykładowy słownik:
{
"title": "Horizon temperature on the real line",
"link_to_article": "https://inspirehep.net/literature/1670639",
"authors": ["Michele Arzano","Jerzy Kowalski-Glikman"],
"link_to_authors": ["https://inspirehep.net/authors/1034076","-"],
"date" : "27-08-2018"
}
- trzecia osoba na podstawie otrzymanych zparsowanych danych generuje plik html lub printuje to wszystko do konsoli (zależnie od parametru -o). 
