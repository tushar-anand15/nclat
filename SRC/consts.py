JUD_URL = 'https://nclat.nic.in/display-board/judge'
TIMEOUT=300
JUD_TEXT_XPATH = "//*[@onclick=\"fn_judge_dfr_type('order_date_wise')\"]"
LOCATION_SELECT_XPATH = '//*[@id="location"]'
CASE_TYPE_SELECT_XPATH = '//*[@id="case_type"]'
FROM_DATE_XPATH = '//*[@id="from_date"]'
TO_DATE_XPATH = '//*[@id="to_date"]'
SEARCH_BUTTON_XPATH = '//*[@type="submit"]'
SLEEP_TIME = 2
CASE_LIST_TABLE_CLASS = 'table table-hover table-bordered'   
CASE_LIST_DIV_TABLE_ID = 'table-container'
ORDER_DETAIL_BOXES_CLASS = 'order-detail-boxes'
WAIT_TIME = 60
ORDER_DETAIL_BOXES_XPATH = "//div[@class='order-detail-boxes']"
CASE_VIEW_BUTTON_XPATH = ".//button[contains(@class, 'btn') and contains(@class, 'btn-success') and contains(@class, 'btn-sm') and contains(@class, 'm-b-0-0') and contains(@class, 'waves-effect') and contains(@class, 'waves-light') and contains(@class, 'pop_data')]"

CASE_POPUP_CLASS = 'modal-content'

COLLAPSE_TOGGLETAB_XPATH = '//*[@id="Toggletab"]'
PDF_DOWNLOAD_BUTTON_XPATH = '//button[@class="btn btn-success"]'