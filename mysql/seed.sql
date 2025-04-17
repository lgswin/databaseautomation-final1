USE project_db;

-- Insert sample data into ClimateData table
INSERT INTO ClimateData (location, record_date, temperature, precipitation, humidity) VALUES
-- Toronto, Canada (4 seasons data)
('Toronto', '2024-01-15', -5.2, 2.5, 65),
('Toronto', '2024-04-15', 12.8, 15.3, 70),
('Toronto', '2024-07-15', 25.6, 0.0, 55),
('Toronto', '2024-10-15', 15.3, 8.7, 75),

-- Tokyo, Japan (4 seasons data)
('Tokyo', '2024-01-15', 5.8, 12.3, 60),
('Tokyo', '2024-04-15', 16.2, 45.6, 75),
('Tokyo', '2024-07-15', 30.5, 78.9, 85),
('Tokyo', '2024-10-15', 20.1, 35.4, 70),

-- Sydney, Australia (4 seasons data - Southern Hemisphere)
('Sydney', '2024-01-15', 26.5, 0.0, 65),
('Sydney', '2024-04-15', 20.8, 45.2, 75),
('Sydney', '2024-07-15', 15.2, 89.7, 80),
('Sydney', '2024-10-15', 22.3, 25.6, 70),

-- London, UK (4 seasons data)
('London', '2024-01-15', 4.2, 25.6, 85),
('London', '2024-04-15', 12.5, 18.9, 75),
('London', '2024-07-15', 22.8, 5.4, 65),
('London', '2024-10-15', 14.6, 35.7, 80),

-- Dubai, UAE (Desert climate)
('Dubai', '2024-01-15', 20.5, 0.0, 45),
('Dubai', '2024-04-15', 28.7, 0.0, 40),
('Dubai', '2024-07-15', 38.2, 0.0, 35),
('Dubai', '2024-10-15', 32.4, 0.0, 42),

-- Rio de Janeiro, Brazil (Tropical climate)
('Rio de Janeiro', '2024-01-15', 30.2, 45.6, 80),
('Rio de Janeiro', '2024-04-15', 28.5, 35.8, 75),
('Rio de Janeiro', '2024-07-15', 25.8, 15.2, 70),
('Rio de Janeiro', '2024-10-15', 27.4, 25.4, 75),

-- New York, USA (4 seasons data)
('New York', '2024-01-15', -2.5, 15.8, 70),
('New York', '2024-04-15', 14.2, 25.6, 65),
('New York', '2024-07-15', 28.5, 5.4, 60),
('New York', '2024-10-15', 16.8, 35.2, 75),

-- Mumbai, India (Monsoon climate)
('Mumbai', '2024-01-15', 25.6, 0.0, 65),
('Mumbai', '2024-04-15', 32.4, 0.0, 60),
('Mumbai', '2024-07-15', 28.9, 89.7, 85),
('Mumbai', '2024-10-15', 30.2, 45.6, 75); 