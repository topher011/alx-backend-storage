--  a SQL script that creates a table users
CREATE TABLE IF NOT EXISTS users (
id INT PRIMARY KEY AUTO_INCREMENT,
email CHAR(255) UNIQUE NOT NULL,
name CHAR(255),
country ENUM('US', 'CO', 'TN') NOT NULL
);
