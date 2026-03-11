select count(distinct ic.Category)
from ItemCategories ic
where ic.ItemID in (
    select ItemID
    from Bids
    where Amount > 100.00
);