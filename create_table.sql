SET GLOBAL local_infile = 1;
DROP DATABASE IF EXISTS FinalProject;
CREATE DATABASE FinalProject;
USE FinalProject;

-- dataset

DROP TABLE IF EXISTS 2017PurchasePricesDec;
CREATE TABLE 2017PurchasePricesDec(
    Brand INT NOT NULL,
    `Description` VARCHAR(100),
    Price DECIMAL(10, 2),
    `Size` VARCHAR(20),
    Volume INT DEFAULT 0,
    Classification INT DEFAULT 0,
    PurchasePrice DECIMAL(10, 2),
    VendorNumber INT DEFAULT 0,
    VendorName VARCHAR(100),
    PRIMARY KEY (Brand)
);

load data local infile './Data/2017PurchasePricesDec.csv'
into table 2017PurchasePricesDec
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

DROP TABLE IF EXISTS  BegInvFINAL12312016;
CREATE TABLE BegInvFINAL12312016(
    InventoryId VARCHAR(50) NOT NULL,
    Store INT DEFAULT 0,
    City VARCHAR(100),
    Brand INT DEFAULT 0,
    `Description` VARCHAR(255),
    `Size` VARCHAR(20),
    onHand INT DEFAULT 0,
    Price DECIMAL(10, 2),
    startDate DATE,
    PRIMARY KEY (`InventoryId`)
);

load data local infile './Data/BegInvFINAL12312016.csv'
into table BegInvFINAL12312016
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

DROP TABLE IF EXISTS  EndInvFINAL12312016;
CREATE TABLE EndInvFINAL12312016(
    InventoryId VARCHAR(50) NOT NULL,
    Store INT DEFAULT 0,
    City VARCHAR(100),
    Brand INT DEFAULT 0,
    `Description` VARCHAR(255),
    `Size` VARCHAR(20),
    onHand INT DEFAULT 0,
    Price DECIMAL(10, 2),
    endDate DATE,
    PRIMARY KEY (`InventoryId`)
);

load data local infile './Data/EndInvFINAL12312016.csv'
into table EndInvFINAL12312016
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

DROP TABLE IF EXISTS  InvoicePurchases12312016;
CREATE TABLE InvoicePurchases12312016(
    VendorNumber INT NOT NULL,
    VendorName VARCHAR(150),
    InvoiceDate DATE,
    PONumber INT NOT NULL,
    PODate DATE,
    PayDate DATE,
    Quantity INT DEFAULT 0,
    Dollars DECIMAL(10, 2),
    Freight DECIMAL(10, 2),
    Approval VARCHAR(50),
    PRIMARY KEY (`VendorNumber`, `PONumber`)
);

load data local infile './Data/InvoicePurchases12312016.csv'
into table InvoicePurchases12312016
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

DROP TABLE IF EXISTS  PurchasesFINAL12312016;
CREATE TABLE PurchasesFINAL12312016(
    InventoryId VARCHAR(50) NOT NULL,
    Store INT DEFAULT 0,
    Brand INT DEFAULT 0,
    `Description` VARCHAR(255),
    `Size` VARCHAR(20),
    VendorNumber INT DEFAULT 0,
    VendorName VARCHAR(150),
    PONumber INT NOT NULL,
    PODate DATE,
    ReceivingDate DATE,
    InvoiceDate DATE,
    PayDate DATE,
    PurchasePrice DECIMAL(10, 2),
    Quantity INT DEFAULT 0,
    Dollars DECIMAL(10, 2),
    Classification INT DEFAULT 0,
    PRIMARY KEY (InventoryId, VendorNumber, InvoiceDate, PayDate)
);

load data local infile './Data/PurchasesFINAL12312016.csv'
into table PurchasesFINAL12312016
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

DROP TABLE IF EXISTS SalesFINAL12312016;
CREATE TABLE SalesFINAL12312016(
    InventoryId VARCHAR(50) NOT NULL,
    Store INT DEFAULT 0,
    Brand INT DEFAULT 0,
    `Description` VARCHAR(255),
    `Size` VARCHAR(20),
    SalesQuantity INT DEFAULT 0,
    SalesDollars DECIMAL(10, 2) DEFAULT 0.00,
    SalesPrice DECIMAL(10, 2) DEFAULT 0.00,
    SalesDate DATE,
    Volume INT DEFAULT 0,
    Classification INT DEFAULT 0,
    ExciseTax DECIMAL(10, 2) DEFAULT 0.00,
    VendorNo INT DEFAULT 0,
    VendorName VARCHAR(150),
    PRIMARY KEY (`InventoryId`, SalesDate, VendorNo)
);

load data local infile './Data/SalesFINAL12312016.csv'
into table SalesFINAL12312016
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

-- user

CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL
);

INSERT INTO users (username,password)
VALUES('admin','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');

-- discussion board

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ALTER TABLE posts DROP INDEX username;

