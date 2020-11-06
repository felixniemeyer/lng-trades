WITH distinct_origins AS (
	select 
		distinct 
		"Zone Origin" as zone, 
		"Installation Origin" as installation 
	from trades 
	union
	select 
		distinct 
		"Zone Destination" as zone, 
		"Installation Destination" as installation
	from trades
)
SELECT
	zone,
	count(*) as c
from 
	distinct_origins
group by zone
