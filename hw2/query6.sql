select count(*)
from Users
where UserID in (select SellerID from Items)
AND UserID in (select userID from Bids);
