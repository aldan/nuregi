# Basic API for Public Course Catalog

import requests
import logging

request_url = 'https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json'
request_timeout = 30


def get_semesters():

    request_data = {
        'method': 'getSemesters'
    }

    try:
        res = requests.post(request_url, data=request_data, timeout=request_timeout)
        logging.info(f'get_semesters(): status {res.status_code}')
        res.raise_for_status()

    except requests.exceptions.Timeout:
        logging.error(f'get_semesters(): request timed out ({request_timeout})')
        return None

    except requests.exceptions.RequestException as Err:
        logging.error(f'get_semesters(): exception occurred\n{Err.args[0]}')
        return None

    try:
        semesters_list = res.json()
        logging.info(f'get_semesters(): {semesters_list}')
        return semesters_list

    except:
        logging.error(f'get_semesters(): could not process data')
        return None


def get_semester(semester_code=None):

    semesters_list = get_semesters()

    if not semesters_list:
        logging.error(f'get_semester(): semesters_list is null')
        return None

    if isinstance(semester_code, int):
        semester_code = str(semester_code)

    if not semester_code:
        logging.warning(f'get_semester(): semester_code not specified')
        try:
            return semesters_list[0]
        except IndexError:
            logging.error(f'get_semester(): semesters_list is empty')
            return None

    semester = next((sem for sem in semesters_list if sem['ID'] == semester_code), None)
    logging.info(f'get_semester(): {semester}')
    return semester
