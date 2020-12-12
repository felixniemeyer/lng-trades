SELECT 
    origin,
    destination, 
    sum(dest_volume) as volume, 
    count(*) as deliveries
FROM 
    tidy_trades
GROUP BY 
    origin, 
    destination