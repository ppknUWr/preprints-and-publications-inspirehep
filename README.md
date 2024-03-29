# preprints-and-publications-inspirehep
## Opis:
Skrypt pozwala generować raporty na temat ostatnich prac/ artykułów naukowych wskazanej osoby lub osób i eksportować do plików HTML, które z łatwością mogą zostać załączone do strony wydziału albo instytutu.
W tym celu wykorzystujemy składnie:<br>

	python script.py -a "Remigiusz Durka or Maciej Matyka" -s 10 -o site.html
	python script.py --authors authors.txt -y "2020-2019"
	
	Parametry:
	[-a,--authors] - string taki jak w przykładzie lub plik w formacie txt.
	[-y, --year] - zawężenie danych do konkretnego roku lub przedziału lat.
	[-s, --size] - ilość preprintów/publikacji do zwrócenia.
	[-o,--output] - użytkownik podaje nazwe pliku html (np. "site.html") lub ścieżke (np."/home/usr/site.html).

## Podział prac:
- pierwsza osoba (x_name) zajmie się pobraniem danych od użytkownika np:<br>
	python script.py -a "Remigiusz Durka or Maciej Matyka" -o site.html<br>
	python script.py --authors authors.txt -y "2018-2020"<br>

	[-a,--authors] - string taki jak w przykładzie lub plik w formacie txt.<br>
	[-y, --year] - użytkownik podaje konkretny rok, lata lub przedział czasowy używając przy tym operatorów logicznych(<, <=, >, >=, or). Jest to argument niewymagany, więc 	jeśli użytkownik go nie użyje to domyślnie zwróci całą historie. (Najlepiej żeby ta osoba pracowała sciśle z osobą drugą nad tą rzeczą.) <br>
	[-o,--output] - użytkownik podaje nazwe pliku html (np. "site.html") lub ścieżke (np."/home/usr/site.html).<br>

- druga osoba (y_name) zajmie się pobraniem danych z api wg. parametrów (nad pobraniem wg. parametru -y najlepiej pracować sciśle z osobą pierwszą), a następnie ich zparsowaniem. Najlepiej jakby była to lista słowników,<br> 
gdzie każdy słownik będzie zawierał: tytuł, link do artykułu, autora/autorów, link do autorów na inspirehtp oraz date (earliest_date).<br>
Przykładowy słownik:<br>
{<br>
"title": "Horizon temperature on the real line",<br>
"link_to_article": "https://inspirehep.net/literature/1670639",<br>
"authors": ["Michele Arzano","Jerzy Kowalski-Glikman"],<br>
"link_to_authors": ["https://inspirehep.net/authors/1034076", "-"],<br>
"date" : "27-08-2018"<br>
}<br> 
- trzecia osoba (z_name) na podstawie otrzymanych zparsowanych danych generuje plik html lub printuje to wszystko do konsoli (zależnie od parametru -o).<br>
	Przykład:<br>
	<img src="https://raw.githubusercontent.com/ppknUWr/preprints-and-publications-inspirehep/main/example_html.png">
