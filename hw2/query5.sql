select count(*)
from Users
where UserID in (select SellerID from Items)
AND Rating > 1000;