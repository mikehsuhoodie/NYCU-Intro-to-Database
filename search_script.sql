USE FinalProject;

-- 【1】設定測試用參數 (在此用來搜尋 Description)
--     你只要改變 @inputDescription 的值，就能搜尋不同酒名
SET @inputDescription = 'Belvedere Vodka';

-- 【2】若想建一張新的彙整表，確保不存在
-- DROP TABLE IF EXISTS CombinedAlcoholInfo;

-- 【3】從五張表抓取「你想要的欄位」，再 LEFT JOIN 起來
--     並將查詢結果直接建成一張名為 CombinedAlcoholInfo 的表。
-- CREATE TABLE CombinedAlcoholInfo AS
SELECT DISTINCT
    -- 來自 EndInvFINAL12312016 的欄位
    e.Brand,
    e.onHand,
    e.City,
    e.Price AS SellPrice,

    -- 來自 2017PurchasePricesDec 的欄位
    REPLACE(REPLACE(decTable.VendorName, '\r', ''), '\n', '') AS DecVendorName,

    -- 來自 PurchasesFINAL12312016 的欄位
    REPLACE(REPLACE(pur.Quantity, '\r', ''), '\n', '') AS PurchaseQuantity,
    pur.Dollars  AS PurchaseDollars,

    -- 來自 InvoicePurchases12312016 的欄位
    inv.PayDate AS InvoicePayDate

FROM EndInvFINAL12312016 AS e

-- (1) 連接 2017PurchasePricesDec：用 Brand 對應
JOIN 2017PurchasePricesDec AS decTable
  ON e.Brand = decTable.Brand

-- (2) 連接 PurchasesFINAL12312016：
--     這裡常見的做法是透過 InventoryId (或 Brand) 連接
LEFT JOIN PurchasesFINAL12312016 AS pur
  ON e.InventoryId = pur.InventoryId
  AND e.Brand       = pur.Brand

-- (3) 連接 InvoicePurchases12312016：
--     PurchasesFINAL12312016 有 PONumber & VendorNumber
--     InvoicePurchases12312016 也有 PONumber & VendorNumber => 可JOIN
LEFT JOIN InvoicePurchases12312016 AS inv
  ON pur.VendorNumber = inv.VendorNumber
  AND pur.PONumber    = inv.PONumber

-- (5) 在 WHERE 條件放「搜尋描述關鍵字」
WHERE e.Description LIKE CONCAT('%', @inputDescription, '%')
    -- 以下「過濾掉」任何欄位為 NULL 的紀錄
    AND e.Brand         IS NOT NULL
    AND e.onHand        IS NOT NULL
    AND e.City          IS NOT NULL
    AND e.Price         IS NOT NULL
    
    AND decTable.VendorName   IS NOT NULL
    
    AND pur.Quantity    IS NOT NULL
    AND pur.Dollars     IS NOT NULL
    
    AND inv.PayDate     IS NOT NULL
;
