CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL
);

INSERT INTO users (username,password)
VALUES('admin','1234');