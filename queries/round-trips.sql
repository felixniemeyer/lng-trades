SELECT 
    * 
FROM
    trades
WHERE
  "Zone destination" == "Zone origin"
  AND "Installation destination" == "Installation origin"