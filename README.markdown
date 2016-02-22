# Library Searcher

Bulk-seaching my local library's catalogue.

We're trying a home-preschool program that suggests about 20 books every week.
Doing 20 searches and copying the call numbers into a spreadsheet is a bit of
a drag -- so I wrote this.

## USAGE:


1. Wite a file (`list_of_searches.txt` in this example) with one
   search-box query per line.  I use `[Author's Last Name][Tab][Title]`.
2. `python search.py list_of_searches.txt`
3. Open `done.html` in your favorite browser.
4. Print (Landscape works best).
5. FIXME: You should probably delete `books.sqlite3` before doing your next search.

`render_results.py` can also be run standalone, in case you want to
tweak the layout without re-querying the website constantly.

## TODO:

- Make the preferred list of libraries (easily) configurable
- List any books that aren't in preferred libraries
- List any books that aren't in ANY libraries
- Allow choosing non-first search results for any given query
- Better test coverage

### Also:

- Wrap in Flask API?
- Direct PDF generation with ReportLab?
- Port to single-page app with Elm?
    - (note: eventually incompatible with the ReportLab idea)
    - Can possibly handle printable rendering with [pdfmake](http://pdfmake.org/)
    - Would have to switch from SQL to functional-whatever result processing
      (Probably a good thing to learn anyway)


