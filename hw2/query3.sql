select count(*)
from (
    select ItemID
    from ItemCategories
    group by ItemID
    having count(*) = 4
);