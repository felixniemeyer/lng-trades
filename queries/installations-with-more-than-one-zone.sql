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
	installation 
	zone_count
FROM
	(
		SELECT
			installation,
			count(*) as zone_count
		from 
			distinct_origins
		group by installation 
	)
WHERE
	zone_count > 1
