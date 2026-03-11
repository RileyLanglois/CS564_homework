SELECT COUNT(DISTINCT ic.Category)
FROM ItemCategories ic
WHERE ic.ItemID IN (
    SELECT ItemID
    FROM Bids
    WHERE Amount > 100.00
);