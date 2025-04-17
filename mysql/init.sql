-- Use project_db database
USE project_db;

-- Create ClimateData table
CREATE TABLE IF NOT EXISTS ClimateData (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    record_date DATE NOT NULL,
    temperature FLOAT NOT NULL,
    precipitation FLOAT NOT NULL,
    humidity FLOAT NOT NULL
);

DESCRIBE ClimateData; 