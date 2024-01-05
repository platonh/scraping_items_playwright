# Introduction

This is a Python project that scrapes data about items from two gadget marketplaces and compares them. 

The goal was to practice data scraping, post-processing, and analysis.

Websites: eldorado.ua, foxtrot.com.ua

Category of items: Apple iPhones

# Project Description


Project performs web scraping and comparison of iPhone data across two popular gadget marketplaces. It aims to provide users with a comprehensive overview of item's data, such as:
- availability 
- pricing
- specifications

## Key Features

-   **Automated Data Scraping:**
    
    -   Utilizes `playwright` for headless browser automation and website interaction.
    -   Implements `playwright-stealth` and `fake-useragent` libraries to disguise the scraper and prevent detection.
    -   Extracts essential data from both websites, including title, price, currency, and availability.
   
-   **Advanced Data Processing:**
    
    -   Uses **regular expressions** to accurately extract detailed iPhone specifications like model, color, memory, and model number.
    -   Uses advanced logic and NLTK's Levenshtein distance algorithm to handle differences in color spelling and word order (e.g., "grey" vs. "gray" or "sierra blue" vs. "blue sierra").
    
-   **Comprehensive Comparison and Output:**
    
    -   Compares iPhone data by model, model number, memory size, and color, taking into account potential spelling variations.
    -   Generates three CSV files for user analysis:
        -   **Common Positions:**  Contains all iphones found on both websites, including their details and respective links.
        -   **Unique Positions (Website 1):**  Lists iPhones exclusive to the first website.
        -   **Unique Positions (Website 2):**  Lists iPhones exclusive to the second website.

## Technologies

- Python - version 3.12
- Playwright - version 1.40.0
- Selectolax - version 0.3.17
- RegEx - version 2023.10.3
- NLTK - version 3.8.1
- Pandas - version 2.1.3


# Project Structure

## Directories And Modules

-   **main.py:** Contains the central logic for scraping, parsing, comparing, and saving data to CSV files.

-   **utils/**: Houses utility functions for various tasks:
    
    -   **extract_playwright.py:** Uses `playwright` to load website's content and extract HTML code. 
    -   **parse.py:** Parses raw attributes from `selectolax` Node instance.
    -   **postprocess.py:** Processes parsed data, including comparison and CSV file generation.
    
-   **classes/**: Contains dataclasses:
    
    -   **item.py:** Defines the `Item` dataclass for representing iPhone data.
    
-   **config/**: Stores configuration files and tools:
    
    -   **tools.py:** Contains functions for generating and reading JSON configs.
    -   **eldorado.json** and **foxtrot.json:** Configuration files with CSS selectors for respective websites.
    -   **logging_config.py:** Implements logging functionality.
    
-   **parsed_data/**: Stores the generated CSV files.
-   **logs/**: Contains log files.
-   **tests/**: Houses Python tests for the `Item` class.

## Key Functions

-   **main.py:**
    
    -   `scrape_and_parse(config_file)`: Performs scraping and parsing for a single website. 
    - `compare_two_websites():` Contains the whole logic for scraping, comparing and saving data to CSV files from two websites.
    
-   **utils/extract_playwright.py:**
    
    -   `extract_html_body(url)`: Extracts HTML content from a given URL using Playwright. Uses `playwright-stealth` and `fake-useragent` to disguise the scraper and prevent detection.
    
-   **utils/parse.py:**
    
    -   `parse_raw_attributes(node: Node, selectors: list)`: Parses raw attributes from `selectolax` Node instance. 
    
-   **utils/postprocess.py:**
    
    -   `get_common_items(list1, list2, check_availability: bool)`: Identifies common items between two lists.
    -   `get_unique_items(list1, list2)`: Finds unique items in each list.
    -   `save_to_file(data, filename)`: Saves items to a CSV file.
    
-   **classes/item.py:**
    
    -   `Item`: Dataclass representing an iPhone.
        
        -   `__post_init__`: Extracts iPhone specifications from the title using regex.
        -   `__eq__`: Implements logic for comparing `Item` instances.
    
-   **config/tools.py:**
    -   `generate_config()`: Generates a blueprint JSON config for a website.
    -   `get_config(filename)`: Reads a JSON config file for a website.

# Setup

1. Clone this repo:

```bash
git clone https://github.com/platonh/scraping_items_playwright.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright Chromium:

```bash
playwright install chromium
```

4. Run the project:

```bash
python main.py
```