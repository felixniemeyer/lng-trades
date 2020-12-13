CREATE VIEW IF NOT EXISTS nodes
AS
select 
	node, 
	sum(inflow) as inflow, 
	sum(outflow) as outflow
from 
	(
	select 
		0 as inflow,
		orig_volume as outflow,
		origin as node
	from 
		tidy_trades
	union
	select 
		dest_volume as inflow,
		0 as outflow,
		destination as node
	from 
		tidy_trades
	)
group by node
;
