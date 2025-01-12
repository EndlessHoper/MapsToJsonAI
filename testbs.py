import sys
import os
import time
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


def find_chromedriver():
    """Find ChromeDriver in the project root or chromedriver-mac-arm64 directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    possible_dirs = [
        current_dir,  # Current project directory
        os.path.join(current_dir, 'chromedriver-mac-arm64'),  # Specific ARM64 directory
    ]
    possible_names = ['chromedriver', 'chromedriver.exe', 'chromedriver_mac']
    
    for search_dir in possible_dirs:
        for name in possible_names:
            driver_path = os.path.join(search_dir, name)
            if os.path.exists(driver_path):
                print(f"Found ChromeDriver at: {driver_path}")
                return driver_path
    
    print("ChromeDriver not found. Please ensure it's in the project root or chromedriver-mac-arm64 directory.")
    return None


def scroll_and_find_button(driver, timeout=30):
    """
    Scrolls down the page to find the "Alle akzeptieren" button and clicks it.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Try to locate the button
            consent_button = driver.find_element(By.XPATH, "//button//span[contains(text(), 'Alle akzeptieren')]")
            
            # Scroll to the button
            driver.execute_script("arguments[0].scrollIntoView(true);", consent_button)
            time.sleep(1)  # Give the browser time to scroll
            
            # Click the button
            consent_button.click()
            print("Cookie consent accepted.")
            return True
        except Exception as e:
            print(f"Button not found yet. Scrolling... {e}")
            # Scroll down slightly
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)  # Pause before attempting again
    print("Failed to find and click the 'Alle akzeptieren' button within timeout.")
    return False


def extract_google_maps_info(maps_url):
    """
    Navigates to the given Google Maps URL, attempts to accept cookies,
    and then extracts the business name, address, and phone number.
    Returns a dictionary with the extracted information or None on failure.
    """

    # -- 1) Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--window-size=1920,1080")  # Set a specific window size
    chrome_options.add_argument("--verbose")                # Increase logging verbosity

    driver = None
    try:
        # -- 2) Find and launch ChromeDriver
        driver_path = find_chromedriver()
        if not driver_path:
            print("Could not find ChromeDriver. Please ensure it's in the project root or chromedriver-mac-arm64 directory.")
            return None
        
        # Ensure the driver is executable
        os.chmod(driver_path, 0o755)
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        
        print(f"Navigating to URL: {maps_url}")
        driver.get(maps_url)
        
        # -- 3) Scroll and find the "Alle akzeptieren" button
        if not scroll_and_find_button(driver):
            print("Could not accept cookies. Proceeding without it.")
        
        # -- 4) Wait for main content to load
        print("Waiting for main content to load...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'DUwDvf'))
        )
        print("Main content loaded successfully.")
        
        # Pause briefly to allow dynamic content to update
        time.sleep(3)

        # -- 5) Parse the page and extract data
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract business name
        business_name_tag = soup.find('h1', class_='DUwDvf')
        business_name = business_name_tag.get_text(strip=True) if business_name_tag else 'N/A'
        print(f"Business Name: {business_name}")

        # Extract address
        address_tag = soup.find('button', {'data-item-id': 'address'})
        address = address_tag.get_text(strip=True) if address_tag else 'N/A'
        print(f"Address: {address}")

        # Extract phone number
        phone_tag = soup.find('button', {'data-item-id': lambda x: x and x.startswith('phone:')})
        phone_number = phone_tag.get_text(strip=True) if phone_tag else 'N/A'
        print(f"Phone Number: {phone_number}")

        return {
            'business_name': business_name,
            'address': address,
            'phone_number': phone_number
        }

    except Exception as e:
        print("Full error traceback:")
        traceback.print_exc()
        print(f"An unexpected error occurred: {e}")
        return None
    
    finally:
        # -- 6) Clean up by closing the driver
        if driver:
            try:
                driver.quit()
                print("WebDriver closed successfully.")
            except Exception as quit_error:
                print(f"Error closing WebDriver: {quit_error}")


def main():
    # Prompt the user for a URL
    maps_url = input("Please provide a Google Maps URL: ").strip()
    
    # Validate that a URL was actually entered
    if not maps_url:
        print("No URL provided. Exiting.")
        sys.exit(1)
    
    # Call the extraction function
    print(f"Processing URL: {maps_url}")
    result = extract_google_maps_info(maps_url)

    # Print the results if available
    if result:
        print("\nExtracted Information:")
        for key, value in result.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    else:
        print("Failed to extract information from the URL.")


if __name__ == "__main__":
    main()
