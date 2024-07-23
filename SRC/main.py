import nav
import util_funcs


FROM_DATE = '07/01/2024'
TO_DATE  = '07/10/2024'
LOCATIONS = ['New Delhi', 'Chennai']


def main():
    util_funcs.create_directories()
    nav_logger = util_funcs.create_nav_logger()   
    for location in LOCATIONS:
        dr = util_funcs.create_driver()
        nav.nav_jud_url(dr, nav_logger)
        #print('Navigated to the webpage')
        nav.nav_jud_date_menu(dr, nav_logger)
        util_funcs.get_case_list(dr, location=location, 
                                 from_date=FROM_DATE, 
                                 to_date = TO_DATE, 
                                 nav_logger=nav_logger)
        util_funcs.proc_all_cases(dr,location=location)
        dr.quit()
    

if __name__ == '__main__':
    main()