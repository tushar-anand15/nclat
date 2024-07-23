import nav
from pathlib import Path
from selenium import webdriver
import logging
from pathlib import Path
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import consts
import os
from selenium.webdriver.chrome.options import Options
import json
import time


def create_directories():
    """
    Creates following directories for storing case files and orders.
    - ../DATA/raw_case_files
    - ../DATA/final_orders
    - ../DATA/daily_orders
    
    Returns: None
    
    """
    
    list_of_directories = ['../DATA/raw_case_files',
                           '../DATA/final_orders',
                           '../DATA/daily_orders',
                           '../DATA/logs',
                           '../DATA/case_list_files']
    for directory in list_of_directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    return None


def create_driver(headless_mode=False):
    """
    Creates a selenium webdriver object.
    
    Parameters:
    headless_mode (bool): If True, runs the browser in headless mode.
    
    Returns: 
    driver (selenium.webdriver): A selenium webdriver object.
    
    """
    download_directory = os.path.abspath('../DATA/final_orders')
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": download_directory,  
        "download.prompt_for_download": False,  
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  
    })
    chrome_options.add_argument("--start-maximized")  
    if headless_mode:
        chrome_options.add_argument("--headless") 
    
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver


def create_nav_logger():
    """
    Creates a logger object for navigation functions.
    
    Returns:
    logger (logging.Logger): A logger object.
    
    """
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler('../DATA/logs/nav_logger.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger

def create_case_logger():
    """
    Creates a logger object for case data.
    
    Returns:
    logger (logging.Logger): A logger object.
    
    """
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler('../DATA/logs/case_logger.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger

def create_daily_order_logger():
    """
    Creates a logger object for daily orders.
    
    Returns:
    logger (logging.Logger): A logger object.
    
    """
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler('../DATA/logs/daily_order_logger.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger

def create_final_order_logger():
    """
    Creates a logger object for final orders.
    
    Returns:
    logger (logging.Logger): A logger object.
    
    """
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler('../DATA/logs/final_order_logger.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger


def get_case_list(dr,location, from_date, to_date, nav_logger):
    """
    Navigates to the specified location and date range.
    
    Args:
    dr (WebDriver): The WebDriver instance.
    location (str): The location of the court.
    from_date (str): The start date of the date range.
    to_date (str): The end date of the date range.
    
    Returns:
    int: 1 if successfully navigated to the specified location and date range.
    
    """
    
    try:
        nav.nav_location_daterange(dr, location, from_date, to_date,nav_logger)
    except Exception as e:
        nav_logger.error(f'Exception: {e}')
    else:
        page_source = dr.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        fname = f'../DATA/case_list_files/{location}_{from_date.replace("/","-")}_{to_date.replace("/","-")}.html'
        with open(fname, 'w') as f:
            f.write(soup.prettify())
        return 1


def proc_case_html(case_html):
    """
    Processes the html of each case and returns a formatted dictionary 
    containing the case details.
    
    Args:
        case_html (BeautifulSoup): The BeautifulSoup object representing the HTML of a case.
    
    Returns:
        dict: A dictionary containing the case details with the following keys:
            - 'sl_no': The serial number of the case.
            - 'filing_no': The filing number of the case.
            - 'case_no': The case number.
            - 'case_type': The type of the case.
            - 'case_title': The title of the case.
            - 'bench': The bench where the case is assigned.
            - 'case_status': The status of the case.
            - 'date_of_order': The date of the order.
            - 'judge_name': The name of the judge.
    """
    ths = case_html.find_all('th')
    tds = case_html.find_all('td')
    sl_no = ths[8].text
    filing_no = ths[9].text
    case_no = tds[0].text
    case_type = tds[1].text
    case_title = tds[2].text
    bench = tds[3].text
    case_status = tds[4].text
    date_of_order = tds[7].text
    judge_name = tds[9].text
    case_dict = {'sl_no': sl_no,
                    'filing_no': filing_no,
                    'case_no': case_no,
                    'case_type': case_type,
                    'case_title': case_title,
                    'bench': bench,
                    'case_status': case_status,
                    'date_of_order': date_of_order,
                    'judge_name': judge_name}
    return case_dict



def download_order_each_case(dr, case_element):
    """
    Downloads the order for each case.

    Args:
        dr (WebDriver): The WebDriver instance.
        case_element (WebElement): The element representing the case.

    Returns:
        int: Returns 1 after successfully downloading the PDF for the case.
    """
    
    collapse_toggletab = case_element.find_element(By.XPATH, consts.COLLAPSE_TOGGLETAB_XPATH)
    dr.execute_script("arguments[0].scrollIntoView();", collapse_toggletab)
    print('clicking on the collapse button')
    collapse_toggletab.click()
    print('clicked on the collapse button')
    ##opens PDF in a new window
    print('clicking on the download button')
    wait = WebDriverWait(dr, consts.WAIT_TIME)
    wait.until(EC.element_to_be_clickable((By.XPATH, consts.PDF_DOWNLOAD_BUTTON_XPATH)))
    
    download_button = case_element.find_element(By.XPATH, consts.PDF_DOWNLOAD_BUTTON_XPATH)
    dr.execute_script("arguments[0].scrollIntoView();", download_button)
    download_button.click()
    print(f'clicked on the download button')
    #final_order_logger.log(logging.INFO, 'Downloaded PDF for case: {}'.format(case_dict['filing_no']))
    return 1



def proc_all_cases(dr,location):
    """
    Process all cases on the page and return a list of case data.

    Args:
        dr (WebDriver): The WebDriver instance.

    Returns:
        list: A list of case data dictionaries.

    """
    page_source = dr.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    cases = soup.find_all('div', {'class': consts.ORDER_DETAIL_BOXES_CLASS})
    case_elements = dr.find_elements(By.XPATH, consts.ORDER_DETAIL_BOXES_XPATH)
    for case_html in cases:
        case_dict = proc_case_html(case_html)
        #case_logger.log(logging.INFO, 'Processed case: {}'.format(case_dict['filing_no']))
        #download_order_each_case(dr, case_element)
        #case_data.append(case_dict)
        fname = f'../DATA/raw_case_files/{location}_{case_dict["filing_no"]}.json'
        with open(fname, 'w') as f:
            json.dump(case_dict, f)
    
    for case_element in case_elements:
        download_order_each_case(dr, case_element)
        #time.sleep(0.1)
    
    return 1


# def proc_each_case(dr, case_element, case_html, case_logger):
#     """
#     Processes each case in the case list.
    
    
#     """
#     """
#     For each case:
#     - click on the View button to view the case details
#     - process to a JSON
#     - save the final order PDF file
    
    
#     """
#     view_button = case_element.find_element(By.XPATH, consts.CASE_VIEW_BUTTON_XPATH)
#     view_button.click()
#     #dr.implicitly_wait(consts.WAIT_TIME)
#     case_popup = dr.find_element(By.CLASS_NAME, consts.CASE_POPUP_CLASS)
#     accordion_items = case_popup.find_elements(By.CLASS_NAME, 'accordion-item')

