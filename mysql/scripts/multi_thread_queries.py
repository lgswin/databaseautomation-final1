#!/usr/bin/env python3
"""
Multi-threaded Database Query Execution Script

This script executes multiple types of database queries concurrently to test
the database's robustness and performance.
"""

import mysql.connector
import threading
import time
import random
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("db_query_execution.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("db_queries")

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',  # Changed from 127.0.0.1 to localhost
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'project_db'
}

# Number of threads for each query type
NUM_INSERT_THREADS = 5
NUM_SELECT_THREADS = 10
NUM_UPDATE_THREADS = 5

# Number of iterations for each thread
NUM_ITERATIONS = 20

# Lock for thread synchronization
print_lock = threading.Lock()

def get_db_connection():
    """Create and return a database connection."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Error connecting to database: {err}")
        return None

def insert_query(thread_id):
    """Execute insert queries to add new climate data records."""
    connection = get_db_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    # Sample locations
    locations = ['Toronto', 'New York', 'London', 'Tokyo', 'Sydney', 
                'Paris', 'Berlin', 'Moscow', 'Beijing', 'Dubai']
    
    try:
        for i in range(NUM_ITERATIONS):
            # Generate random data
            location = random.choice(locations)
            # Generate a random date in 2023
            random_days = random.randint(0, 364)
            record_date = datetime(2023, 1, 1) + timedelta(days=random_days)
            
            # Generate random weather data
            if location in ['Toronto', 'New York', 'Moscow', 'Berlin']:
                # Colder climates
                temperature = random.uniform(-10, 30)
            elif location in ['London', 'Paris']:
                # Temperate climates
                temperature = random.uniform(0, 25)
            elif location in ['Tokyo', 'Beijing']:
                # Variable climates
                temperature = random.uniform(5, 35)
            elif location in ['Dubai']:
                # Hot climate
                temperature = random.uniform(20, 45)
            else:  # Sydney
                # Southern hemisphere
                if record_date.month in [12, 1, 2]:  # Summer in southern hemisphere
                    temperature = random.uniform(20, 35)
                else:
                    temperature = random.uniform(10, 25)
            
            precipitation = random.uniform(0, 20)
            humidity = random.uniform(40, 90)
            
            # Insert query
            query = """
            INSERT INTO ClimateData (location, record_date, temperature, precipitation, humidity)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (location, record_date, temperature, precipitation, humidity)
            
            start_time = time.time()
            cursor.execute(query, values)
            connection.commit()
            end_time = time.time()
            
            with print_lock:
                logger.info(f"Insert Thread {thread_id}: Added record for {location} on {record_date.date()}, "
                           f"temp={temperature:.1f}°C, precip={precipitation:.1f}mm, humidity={humidity:.1f}% "
                           f"(took {end_time - start_time:.4f}s)")
            
            # Sleep briefly to simulate real-world conditions
            time.sleep(random.uniform(0.1, 0.5))
    
    except mysql.connector.Error as err:
        logger.error(f"Insert Thread {thread_id} error: {err}")
    finally:
        cursor.close()
        connection.close()

def select_query(thread_id):
    """Execute select queries to retrieve climate data records."""
    connection = get_db_connection()
    if not connection:
        return
    
    cursor = connection.cursor(dictionary=True)
    
    # Different select conditions
    conditions = [
        "temperature > 20",
        "temperature < 0",
        "precipitation > 10",
        "humidity > 80",
        "location = 'Tokyo'",
        "record_date BETWEEN '2023-06-01' AND '2023-08-31'",
        "location IN ('London', 'Paris', 'Berlin')",
        "temperature > 25 AND humidity < 60",
        "precipitation = 0 AND temperature > 15",
        "location = 'Sydney' AND record_date BETWEEN '2023-12-01' AND '2023-12-31'"
    ]
    
    try:
        for i in range(NUM_ITERATIONS):
            # Choose a random condition
            condition = random.choice(conditions)
            
            # Select query
            query = f"SELECT * FROM ClimateData WHERE {condition} LIMIT 10"
            
            start_time = time.time()
            cursor.execute(query)
            results = cursor.fetchall()
            end_time = time.time()
            
            with print_lock:
                logger.info(f"Select Thread {thread_id}: Query '{condition}' returned {len(results)} results "
                           f"(took {end_time - start_time:.4f}s)")
            
            # Sleep briefly to simulate real-world conditions
            time.sleep(random.uniform(0.05, 0.2))
    
    except mysql.connector.Error as err:
        logger.error(f"Select Thread {thread_id} error: {err}")
    finally:
        cursor.close()
        connection.close()

def update_query(thread_id):
    """Execute update queries to modify climate data records."""
    connection = get_db_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    # Different update operations
    update_operations = [
        ("humidity", "humidity + 5", "humidity < 70"),
        ("humidity", "humidity - 5", "humidity > 80"),
        ("temperature", "temperature + 1", "temperature < 10"),
        ("temperature", "temperature - 1", "temperature > 30"),
        ("precipitation", "precipitation + 2", "precipitation < 5"),
        ("precipitation", "precipitation - 2", "precipitation > 15")
    ]
    
    try:
        for i in range(NUM_ITERATIONS):
            # Choose a random update operation
            column, operation, condition = random.choice(update_operations)
            
            # Update query
            query = f"UPDATE ClimateData SET {column} = {operation} WHERE {condition}"
            
            start_time = time.time()
            cursor.execute(query)
            connection.commit()
            rows_affected = cursor.rowcount
            end_time = time.time()
            
            with print_lock:
                logger.info(f"Update Thread {thread_id}: Updated {rows_affected} rows with '{column} = {operation}' "
                           f"where '{condition}' (took {end_time - start_time:.4f}s)")
            
            # Sleep briefly to simulate real-world conditions
            time.sleep(random.uniform(0.1, 0.3))
    
    except mysql.connector.Error as err:
        logger.error(f"Update Thread {thread_id} error: {err}")
    finally:
        cursor.close()
        connection.close()

def main():
    """Main function to start all threads."""
    logger.info("Starting concurrent database query execution...")
    
    # Create threads for each query type
    threads = []
    
    # Insert threads
    for i in range(NUM_INSERT_THREADS):
        thread = threading.Thread(target=insert_query, args=(i+1,))
        threads.append(thread)
    
    # Select threads
    for i in range(NUM_SELECT_THREADS):
        thread = threading.Thread(target=select_query, args=(i+1,))
        threads.append(thread)
    
    # Update threads
    for i in range(NUM_UPDATE_THREADS):
        thread = threading.Thread(target=update_query, args=(i+1,))
        threads.append(thread)
    
    # Start all threads
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    logger.info(f"All threads completed. Total execution time: {end_time - start_time:.2f} seconds")
    logger.info(f"Executed {NUM_INSERT_THREADS} insert threads, {NUM_SELECT_THREADS} select threads, "
                f"and {NUM_UPDATE_THREADS} update threads, each with {NUM_ITERATIONS} iterations")

if __name__ == "__main__":
    main() 