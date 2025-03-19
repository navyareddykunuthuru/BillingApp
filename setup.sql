CREATE DATABASE IF NOT EXISTS billing_system;

USE billing_system;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    address TEXT,
    phone_number VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    amount DECIMAL(10, 2),
    bill_date DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
