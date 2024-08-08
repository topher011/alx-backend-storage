-- Creates a new table called users
CREATE TABLE IF NOT EXISTS `users` (id INT PRIMARY KEY, email STRING(255) UNIQUE, name STRING(255));
