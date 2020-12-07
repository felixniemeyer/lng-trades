select 
	t1."Vessel", 
	t1."End (origin)", 
	t1."Installation Destination",
	t2."Installation Destination"
from 
	trades as t1, 
	trades as t2
where 
	t1."Zone Origin" == t2."Zone Origin" AND
	t1."Installation Origin" == t2."Installation Origin" AND
	t1."End (origin)" == t2."End (origin)" AND
	t1."Vessel" == t2."Vessel" AND
	t1."Installation Destination" != t2."Installation Destination"

