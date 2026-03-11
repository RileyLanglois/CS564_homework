SELECT COUNT(*)
FROM (
    SELECT ItemID
    FROM ItemCategories
    GROUP BY ItemID
    HAVING COUNT(*) = 4
);