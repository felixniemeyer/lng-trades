with flows as (
	select 
		"Zone Origin" || " / " || "Installation Origin" as origin,
		"Zone Destination" || " / " || "Installation Destination" as destination, 
		cast("Volume (origin m3)" as int) as outflow,
		cast("Volume (destination m3)" as int) as inflow
	from trades
)
select 
	node, 
	sum(inflow) as inflow, 
	sum(outflow) as outflow
from 
	(
	select 
		0 as inflow,
		outflow,
		origin as node
	from 
		flows
	union
	select 
		inflow,
		0 as outflow,
		destination as node
	from 
		flows
	)
group by node
;
