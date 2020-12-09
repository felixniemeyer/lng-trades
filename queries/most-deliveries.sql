SELECT 
  "Zone destination", "Installation destination",
  count(*) as inflow_count
FROM 
  trades
group by
  "Zone destination", "Installation destination"
order by inflow_count