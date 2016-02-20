select
  -- r.search_query,
  -- r.position,
  -- r.format,
  r.author,
  r.title,
  h.branch_name,
  h.collection_name,
  h.call_class,
  -- s.available
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
order by
  author,
  title,
  branch,
  collection_name asc,
  call_class
