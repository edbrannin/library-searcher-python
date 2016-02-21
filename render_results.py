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
    'Irondequoit Public Library'
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

def render_results():
    rows = session.execute(sql)
    return template.render(rows=rows).encode('utf-8')

if __name__ == '__main__':
    print render_results()
