-- 1. Create the database
CREATE DATABASE redbus_data;

-- 2. Use the newly created database
USE redbus_data;

-- 3. Create the table `bus_routes` with the required columns
CREATE TABLE bus_routes (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- Unique ID for each bus route
    route_name VARCHAR(255),                  -- Name of the bus route (e.g., 'Route A')
    bus_name VARCHAR(255),                    -- Name of the bus (e.g., 'Bus 101')
    bustype VARCHAR(100),                     -- Type of bus (e.g., 'AC', 'Non-AC')
    departing_time VARCHAR(50),               -- Departure time (e.g., '10:30 AM')
    duration VARCHAR(50),                     -- Duration of the journey (e.g., '5 hours')
    reaching_time VARCHAR(50),                -- Time of arrival (e.g., '3:30 PM')
    star_rating DECIMAL(3, 2),                -- Rating of the bus (e.g., 4.50)
    price DECIMAL(10, 2),                     -- Price of the ticket (e.g., 500.00)
    seats_available INT,                      -- Number of seats available (e.g., 15)
    is_government BOOLEAN                     -- Whether the bus is operated by the government (TRUE/FALSE)
);

-- 4. Select all records from the `bus_routes` table (if there are any)
SELECT * FROM bus_routes;

-- 5. Select the first 10 records from the `bus_routes` table (if available)
SELECT * FROM bus_routes LIMIT 10;

-- 6. Clear all data from the `bus_routes` table (without deleting the table structure)
TRUNCATE TABLE bus_routes;
