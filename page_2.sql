-- 1) 使用同一個資料庫
USE FinalProject;


-- 2) 建立測試用參數 (方便在純 SQL 中測試)

-- 假設我們想找的酒名關鍵字是 "Belvedere Vodka"
SET @inputDescription = 'Belvedere Vodka';


-- 3) 做法 A：直接執行查詢

SELECT 
    e.InventoryId,
    e.Description,
    e.Brand,
    e.Size,
    e.OnHand,
    e.City,
    p.VendorName
FROM EndInvFINAL12312016 AS e
-- 這裡以 2017PurchasePricesDec 為例，假設它能對應拿到 VendorName
LEFT JOIN 2017PurchasePricesDec AS p
    ON e.Brand = p.Brand
WHERE e.Description LIKE CONCAT('%', @inputDescription, '%');



-- 4) 做法 B：建立一個 Stored Procedure
--    這樣在 Flask 中只要執行 CALL get_alcohol_info('Bud Light') 即可。

/*DELIMITER $$
CREATE OR REPLACE PROCEDURE get_alcohol_info(IN inputDesc VARCHAR(255))
BEGIN
    SELECT 
        e.InventoryId,
        e.Description,
        e.Brand,
        e.Size,
        e.OnHand,
        e.City,
        p.VendorName
    FROM EndInvFINAL12312016 AS e
    LEFT JOIN 2017PurchasePricesDec AS p
        ON e.Brand = p.Brand
    WHERE e.Description LIKE CONCAT('%', inputDesc, '%');
END $$
DELIMITER ;
*/
-- 執行方式(示範):
-- CALL get_alcohol_info('Bud Light');

