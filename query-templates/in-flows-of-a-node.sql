SELECT 
  "Zone origin", 
  "Installation origin",
  "Volume (destination m3)", 
  "End (destination)"
FROM 
  trades
WHERE 
  "Zone destination" == '$zone' 
  AND "Installation destination" == '$installation' 
;