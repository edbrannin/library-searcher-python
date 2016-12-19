import click
from jinja2 import Environment, FileSystemLoader

from model import *

session = setup_sqlalchemy()()

env = Environment(loader=FileSystemLoader("."))

template = env.get_template("results.html.j2")

sql = """
select
  r.author,
  r.title,
  h.branch_name,
  h.collection_name,
  h.call_class,
  count(*) as "count"
from
  resources r,
  resource_holdings h,
  resource_status s
where
  r.id = h.item_id
  and s.resource_id = h.item_id
  and s.item_identifier = h.barcode
  and position = 0
  and branch_name in (
     'Rochester Public Library Central',
    'Irondequoit Public Library',
    'Fairport Public Library'
    )
  and available = 1
group by
  r.author,
  r.title,
  h.branch_name,
  h.collection_name,
  h.call_class
order by
  author,
  title,
  branch_name,
  collection_name asc,
  call_class
"""

<<<<<<< HEAD

unlisted_sql = """
SELECT max(rr.search_query) search_query
     ,  rr.author
     ,  rr.title
FROM resources rr
WHERE NOT EXISTS
    (SELECT 1
     FROM resources r
        ,  resource_holdings h
        ,  resource_status s
     WHERE r.id = h.item_id
       AND s.resource_id = h.item_id
       AND s.item_identifier = h.barcode
       AND POSITION = 0
       AND branch_name IN ( 'Rochester Public Library Central'
                          ,  'Irondequoit Public Library' )
       AND available = 1
       AND r.author = rr.author
       AND r.title = rr.title
     GROUP BY r.author
            ,  r.title
            ,  h.branch_name
            ,  h.collection_name
            ,  h.call_class
     ORDER BY author
            ,  title
            ,  branch_name
            ,  collection_name ASC, call_class)
GROUP BY author
       ,  title
ORDER BY search_query
       ,  author
       ,  title
"""

@click.command()
@click.argument("out_file", type=click.File('wb'))
def render_results(out_file):
    rows = session.execute(sql).fetchall()
    missing_rows = session.execute(unlisted_sql).fetchall()
    text = template.render(rows=rows, missing_rows=missing_rows).encode('utf-8')
    out_file.write(text)

if __name__ == '__main__':
    render_results()

