SELECT 
  "Zone destination", 
  "Installation destination",
  "Volume (origin m3)", 
  "End (origin)"
FROM 
  trades
WHERE 
  "Zone origin" == '$zone' 
  AND "Installation origin" == '$installation' 
;
