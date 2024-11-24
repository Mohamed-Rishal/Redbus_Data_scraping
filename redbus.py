import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import time
import re
import traceback


# MySQL Connection Setup
def create_connection():
    """Create a connection to the MySQL database."""
    try:
        print("Creating database connection...")
        engine = create_engine("mysql+pymysql://root:12345678@localhost/redbus_data")
        print("Database connection established successfully.")
        return engine
    except Exception as e:
        print(f"Error creating database connection: {e}")
        return None


def initialize_database():
    """Initialize the database schema if not exists."""
    print("Initializing database schema...")
    engine = create_connection()
    if engine:
        try:
            with engine.connect() as conn:
                conn.execute("""
                CREATE TABLE IF NOT EXISTS bus_routes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    route_name TEXT,
                    bus_name TEXT,
                    bustype TEXT,
                    departing_time TIME,
                    duration TEXT,
                    reaching_time TIME,
                    star_rating FLOAT,
                    price DECIMAL(10, 2),
                    seats_available INT,
                    is_government BOOLEAN
                );
                """)
                print("Database schema initialized successfully.")
        except Exception as e:
            print(f"Error initializing database schema: {e}")


# Web Scraping for Private Buses
def scrape_redbus(source_city, destination_city, travel_date):
    """Scrape private bus data from RedBus."""
    print("Starting private bus scraping...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  # Setup driver
    driver.get("https://www.redbus.in/")  # Open RedBus homepage
    time.sleep(2)

    print(f"Entering source city: {source_city}")
    source = driver.find_element(By.ID, "src")
    source.clear()
    source.send_keys(source_city)
    time.sleep(1)
    source.send_keys(Keys.ENTER)

    print(f"Entering destination city: {destination_city}")
    destination = driver.find_element(By.ID, "dest")
    destination.clear()
    destination.send_keys(destination_city)
    time.sleep(1)
    destination.send_keys(Keys.ENTER)

    # Select the date
    try:
        print(f"Selecting travel date: {travel_date.strftime('%d-%b-%Y')}")
        date_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "onwardCal"))
        )
        date_input.click()
        date_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//td[contains(@class, 'day') and text()='{travel_date.day}']"))
        )
        date_element.click()
    except Exception as e:
        print(f"Error selecting date: {e}")

    # Search buses
    try:
        print("Clicking search button...")
        search_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "search_btn")))
        search_button.click()
    except Exception as e:
        print(f"Error clicking search button: {e}")

    # Scrape bus details
    buses = []
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "bus-item")))
        bus_elements = driver.find_elements(By.CLASS_NAME, "bus-item")

        for bus in bus_elements:
            try:
                price_str = bus.find_element(By.CLASS_NAME, "fare").text.strip()
                price = float(re.sub(r'[^\d.]', '', price_str)) if price_str else None

                buses.append({
                    "route_name": bus.find_element(By.CLASS_NAME, "dp-loc").text,
                    "bus_name": bus.find_element(By.CLASS_NAME, "travels").text,
                    "bustype": bus.find_element(By.CLASS_NAME, "bus-type").text,
                    "departing_time": bus.find_element(By.CLASS_NAME, "dp-time").text,
                    "duration": bus.find_element(By.CLASS_NAME, "dur").text,
                    "reaching_time": bus.find_element(By.CLASS_NAME, "bp-time").text,
                    "star_rating": float(bus.find_element(By.CLASS_NAME, "rating-sec").text or 0),
                    "price": price,
                    "seats_available": int(bus.find_element(By.CLASS_NAME, "seat-left").text.split()[0]),
                    "is_government": False  # Mark as Private Bus
                })
            except Exception as e:
                print(f"Error extracting bus data: {e}")
    except Exception as e:
        print(f"Error scraping private bus data: {e}")

    driver.quit()
    return buses


# Web Scraping for Government Buses
def scrape_government_bus_data(source_city, destination_city, travel_date):
    """Scrape government bus data (e.g., TNSTC) from RedBus RTC Directory."""
    print("Starting government bus scraping...")
    buses = []  # Initialize buses list

    try:
        # Start Chrome WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://www.redbus.in/online-booking/rtc-directory")
        time.sleep(3)  # Allow initial page load

        # Locate and click the TNSTC region
        print("Looking for TNSTC region...")
        region_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'D113_ul_rtc')]//a")
        tnstc_region = None
        for region in region_elements:
            print(f"Found region: {region.text}")
            if "TNSTC" in region.text.upper():
                tnstc_region = region
                break

        if not tnstc_region:
            print("TNSTC region not found!")
            driver.quit()
            return buses  # Return empty list if TNSTC is not found

        print("TNSTC region found, clicking...")
        tnstc_region.click()
        time.sleep(3)  # Allow time for the TNSTC page to load

        # Wait for and fill in source and destination input fields
        print(f"Entering source city: {source_city}")
        source = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtSource"))
        )
        source.clear()
        source.send_keys(source_city)
        time.sleep(1)
        source.send_keys(Keys.ENTER)

        print(f"Entering destination city: {destination_city}")
        destination = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtDestination"))
        )
        destination.clear()
        destination.send_keys(destination_city)
        time.sleep(1)
        destination.send_keys(Keys.ENTER)

        # Select the travel date
        print(f"Selecting travel date: {travel_date.strftime('%d-%b-%Y')}")
        date_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "txtOnwardCalendar"))
        )
        date_input.click()
        time.sleep(1)  # Allow calendar to appear
        date_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//td[contains(@class, 'day') and text()='{travel_date.day}']"))
        )
        date_element.click()

        # Click search button
        print("Clicking search button...")
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "D120_search_btn_v2"))
        )
        search_button.click()
        time.sleep(3)  # Allow results to load

        # Scrape bus details
        print("Scraping government bus details...")
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "bus-item")))
            bus_elements = driver.find_elements(By.CLASS_NAME, "bus-item")

            if not bus_elements:
                print("No government buses found!")
                return buses

            for bus in bus_elements:
                try:
                    price_str = bus.find_element(By.CLASS_NAME, "fare").text.strip()
                    price = float(re.sub(r'[^\d.]', '', price_str)) if price_str else None

                    buses.append({
                        "route_name": bus.find_element(By.CLASS_NAME, "dp-loc").text,
                        "bus_name": bus.find_element(By.CLASS_NAME, "travels").text,
                        "bustype": bus.find_element(By.CLASS_NAME, "bus-type").text,
                        "departing_time": bus.find_element(By.CLASS_NAME, "dp-time").text,
                        "duration": bus.find_element(By.CLASS_NAME, "dur").text,
                        "reaching_time": bus.find_element(By.CLASS_NAME, "bp-time").text,
                        "star_rating": float(bus.find_element(By.CLASS_NAME, "rating-sec").text or 0),
                        "price": price,
                        "seats_available": int(bus.find_element(By.CLASS_NAME, "seat-left").text.split()[0]),
                        "is_government": True  # Mark as Government Bus
                    })
                except Exception as e:
                    print(f"Error extracting government bus data: {e}")
        except Exception as e:
            print(f"Error scraping government bus data: {e}")
    except Exception as e:
        print(f"Error during government bus scraping: {e}")
    
    driver.quit()
    return buses


# Main function to combine both scraping and saving
# Streamlit Interface
def streamlit_interface():
    st.title("RedBus Web Scraping - Private and Government Buses")
    st.write("Enter the details to scrape bus data from RedBus:")

    source_city = st.text_input("Source City", "Chennai")
    destination_city = st.text_input("Destination City", "Bangalore")
    travel_date = st.date_input("Travel Date", value=pd.to_datetime("2024-11-25"))

    if st.button("Scrape Private Bus Data"):
        st.write("Initializing database...")
        initialize_database()

        st.write("Scraping private bus data... Please wait.")
        private_buses = scrape_redbus(source_city, destination_city, travel_date)

        if private_buses:
            st.write("Private Bus Data:")
            st.write(pd.DataFrame(private_buses))
        else:
            st.write("No private bus data found.")

    if st.button("Scrape Government Bus Data"):
        st.write("Scraping government bus data... Please wait.")
        government_buses = scrape_government_bus_data(source_city, destination_city, travel_date)

        if government_buses:
            st.write("Government Bus Data:")
            st.write(pd.DataFrame(government_buses))
        else:
            st.write("No government bus data found.")


# Run Streamlit Interface
if __name__ == "__main__":
    streamlit_interface()