---

# **RedBus Web Scraping and Data Insertion**  
This project scrapes bus data from RedBus for both private and government buses and stores the information in a MySQL database. The data includes details such as bus routes, departure time, price, seats available, and ratings. The project uses Selenium WebDriver for scraping, pandas for data manipulation, and SQLAlchemy for database interaction.

## **Project Overview**
This project provides a simple web scraping solution to extract bus data from RedBus for both private and government buses. The scraped data is stored in a MySQL database for further analysis or reporting. A Streamlit interface is included to allow users to interact with the scraping functionality.

## **Technologies Used**
- **Python 3.x**
- **Streamlit** – A library for building web applications.
- **Selenium** – Web scraping using a browser automation tool.
- **WebDriverManager** – To automatically manage WebDriver binaries.
- **SQLAlchemy** – ORM to interact with the MySQL database.
- **MySQL** – Database for storing the bus data.
- **pandas** – Data handling and manipulation.

## **Prerequisites**
Before running the project, ensure you have the following installed:

- Python 3.6 or above
- MySQL Server installed and running
- Required Python packages:
  ```bash
  pip install streamlit selenium webdriver-manager sqlalchemy pymysql pandas
  ```

## **Setup Instructions**

1. **MySQL Setup:**
   - Make sure MySQL is installed and running.
   - Create a database named `redbus_data` or modify the connection string in the code to match your existing database setup.

2. **Database Schema:**
   - The project will automatically create the required schema (`bus_routes` table) when you first run the scraping functions, if it doesn't already exist.
   
3. **Running the Project:**
   - Open a terminal or command prompt and navigate to the directory containing the Python file.
   - Run the Streamlit interface using:
     ```bash
     streamlit run your_script_name.py
     ```
   - The interface will be available at `http://localhost:8501`, User: `root`, Password: `12345678`.
   - Enter the source city, destination city, and travel date, and then click the "Search" button to scrape bus data.
   - The scraped data will be displayed as a pandas DataFrame.
   - The scraped data will also be stored in the `bus_routes` table of the MySQL database.

## **Functions**

### **1. `create_connection()`**
   - Creates a connection to the MySQL database using SQLAlchemy.
   - Returns the database engine.

### **2. `initialize_database()`**
   - Initializes the database schema (`bus_routes` table) if it doesn't already exist.
   - This table stores the scraped data including bus route, name, type, price, and more.

### **3. `scrape_redbus(source_city, destination_city, travel_date)`**
   - Scrapes private bus data from the RedBus website.
   - Accepts the source city, destination city, and travel date as inputs.
   - Returns a list of dictionaries containing bus details.

### **4. `scrape_government_bus_data(source_city, destination_city, travel_date)`**
   - Scrapes government bus data (e.g., TNSTC) from RedBus RTC Directory.
   - Accepts the source city, destination city, and travel date as inputs.
   - Returns a list of dictionaries containing government bus details.

### **5. `streamlit_interface()`**
   - The main function that provides a Streamlit interface to allow users to interact with the scraping functionality.
   - Users can enter source city, destination city, and travel date, and then scrape private and government bus data.
   - Displays the scraped data as a pandas DataFrame.

## **How It Works**
1. **Web Scraping:**
   - The project uses Selenium to open a Chrome browser and navigate the RedBus website. It interacts with the page by sending keystrokes to the form fields and buttons, selecting the correct travel date, and clicking the "Search" button to get the bus results.
   
2. **Data Extraction:**
   - After searching for buses, the details of each bus are extracted from the page using Selenium’s element locators (e.g., `find_element` and `find_elements`).
   - The data includes:
     - Route Name
     - Bus Name
     - Bus Type (Private/Government)
     - Departing and Reaching Time
     - Duration
     - Price
     - Seats Available
     - Star Rating
   
3. **Database Insertion:**
   - The extracted bus data is stored in the `bus_routes` table of the MySQL database. The table includes fields for bus details like route name, bus name, departure time, price, etc.

4. **Streamlit Interface:**
   - The user can input details such as source city, destination city, and travel date through the Streamlit interface.
   - After clicking the buttons, the app scrapes the bus data and displays it on the web interface as a table.

## **Error Handling**
- **Database Connection Errors:** The code handles errors related to database connectivity and will print appropriate messages if the connection fails.
- **Web Scraping Errors:** The scraping functions include try-except blocks to handle potential errors like elements not being found, timeouts, or failed data extraction.

## **Sample Output (Streamlit Interface)**

When a user enters the source city as "Chennai", destination city as "Bangalore", and a travel date, the following actions occur:
- Private bus data will be scraped and displayed in a tabular format.
- Government bus data will also be scraped and displayed (if available).

### **Private Bus Data Example:**
| Route Name    | Bus Name        | Bus Type    | Departing Time | Duration | Reaching Time | Star Rating | Price  | Seats Available | Is Government |
|---------------|-----------------|-------------|----------------|----------|----------------|-------------|--------|-----------------|---------------|
| Chennai - BLR | ABC Travels     | Private     | 10:00 AM       | 6 hrs    | 4:00 PM        | 4.5         | 600.00 | 30              | False         |

### **Government Bus Data Example:**
| Route Name    | Bus Name        | Bus Type    | Departing Time | Duration | Reaching Time | Star Rating | Price  | Seats Available | Is Government |
|---------------|-----------------|-------------|----------------|----------|----------------|-------------|--------|-----------------|---------------|
| Chennai - BLR | TNSTC Travels   | Government  | 10:30 AM       | 6 hrs    | 4:30 PM        | 4.0         | 450.00 | 40              | True          |

## **Notes**
- **WebDriver Management:** The project uses `webdriver_manager` to automatically handle the installation of the appropriate version of ChromeDriver, making it easier to get started with scraping.
- **Scalability:** The current implementation is tailored for RedBus scraping, but the structure can be adapted for other bus booking websites with minimal modifications.

## **Conclusion**
This project demonstrates how to scrape bus data from RedBus using Selenium and Python, while also storing the data in a MySQL database for easy querying and reporting. The Streamlit interface allows users to interact with the scraper and view the results directly from the web.

---
