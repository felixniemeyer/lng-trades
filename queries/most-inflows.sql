select 
    destination,
    sum(dest_volume) as inflow
from tidy_trades
group by destination
order by inflow