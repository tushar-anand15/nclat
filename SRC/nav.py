import consts
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

def nav_jud_url(dr, nav_logger, timeout=consts.TIMEOUT):
    """
    Navigates to the specified URL and logs the navigation status.

    Args:
        dr (WebDriver): The WebDriver instance.
        nav_logger (Logger): The logger instance for logging navigation status.
        timeout (int, optional): The page load timeout in seconds. Defaults to consts.TIMEOUT.

    Returns:
        int: 1 if the navigation is successful, otherwise None.
    """
    dr.set_page_load_timeout(timeout)
    try:
        dr.get(consts.JUD_URL)
    except TimeoutException:
        nav_logger.error('TimeoutException: Page took too long to load.')
    except Exception as e:
        nav_logger.error(f'Exception: {e}')
    else:
        nav_logger.info('Navigated to the webpage')
        return 1

    
def nav_jud_date_menu(dr, nav_logger, timeout=consts.TIMEOUT):
    """
    Navigates to the judgement date menu.

    Args:
        dr: The WebDriver instance.
        nav_logger: The logger object for logging navigation events.
        timeout: The page load timeout in seconds (default: consts.TIMEOUT).

    Returns:
        1 if successfully navigated to the judgement date menu.

    Raises:
        TimeoutException: If the page takes too long to load.
        Exception: If any other exception occurs during navigation.
    """
    
    dr.set_page_load_timeout(timeout)
    try:
        dr.find_element(By.XPATH, consts.JUD_TEXT_XPATH).click()
    except TimeoutException:
        nav_logger.error('TimeoutException: Page took too long to load.')
    except Exception as e:
        nav_logger.error(f'Exception: {e}')
    else:
        nav_logger.info('Navigated to the judgement date menu')
        return 1
    

def nav_location_daterange(dr,location,from_date, to_date, nav_logger,case_type='All'):
    """
    Navigates to the specified location and date range.
    
    Args:
        location (str): The location to select from the dropdown. New Delhi and Chennai are the two options.
        from_date (str): The start date in the format 'mm/dd/yyyy'.
        to_date (str): The end date in the format 'mm/dd/yyyy'.
    
    Returns:
        1: If the navigation is successful.
        None: If the navigation is unsuccessful.
    
    """
    ## assumes that the driver is already on the judgement date menu
    location_select = Select(dr.find_element(By.XPATH, consts.LOCATION_SELECT_XPATH))
    location_select.select_by_visible_text(location)
    nav_logger.info(f'Selected location: {location}')
    
    #time.sleep(consts.SLEEP_TIME)
    
    case_type_select = Select(dr.find_element(By.XPATH, consts.CASE_TYPE_SELECT_XPATH))
    case_type_select.select_by_visible_text(case_type)
    nav_logger.info(f'Selected case type: {case_type}')
    #time.sleep(consts.SLEEP_TIME)
    
    from_date_box = dr.find_element(By.XPATH, consts.FROM_DATE_XPATH)
    dr.execute_script("arguments[0].removeAttribute('readonly')", from_date_box)
    from_date_box.send_keys(from_date)
    #dr.execute_script(f"arguments[0].value = '{from_date}';", from_date_box)
    from_date_box.send_keys(Keys.TAB)
    nav_logger.info(f'Selected from date: {from_date}')
    
    #time.sleep(consts.SLEEP_TIME)
    
    to_date_box = dr.find_element(By.XPATH, consts.TO_DATE_XPATH)
    dr.execute_script("arguments[0].removeAttribute('readonly')", to_date_box)
    #dr.execute_script(f"arguments[0].value = '{to_date}';", to_date_box)
    to_date_box.send_keys(to_date)
    to_date_box.send_keys(Keys.TAB)
    
    nav_logger.info(f'Selected to date: {to_date}')
    time.sleep(consts.SLEEP_TIME)
    #time.sleep(consts.SLEEP_TIME)
    wait = WebDriverWait(dr, consts.WAIT_TIME)
    #wait.until(EC.element_to_be_clickable((By.XPATH, consts.SEARCH_BUTTON_XPATH)))
    search_button = dr.find_element(By.XPATH, consts.SEARCH_BUTTON_XPATH)
    
    dr.execute_script("arguments[0].scrollIntoView(true);", search_button)
    search_button.click()
    nav_logger.info('Clicked on the search button. Waiting for the element to be located.')
    
    wait.until(EC.visibility_of_element_located((By.ID, 'table-container')))
    nav_logger.info('Located the case list table.')
    return 1
    

    