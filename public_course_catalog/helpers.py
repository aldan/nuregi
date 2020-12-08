# Do not call methods from this file outside of public_course_catalog package

import requests
import logging

request_url = 'https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json'
request_timeout = 30


def get_data(request_data, sort_key=None):
    try:
        res = requests.post(request_url, data=request_data, timeout=request_timeout)
        logging.info(f'get_data(): status {res.status_code}')
        res.raise_for_status()

    except requests.exceptions.Timeout:
        logging.error(f'get_data(): request timed out ({request_timeout})')
        return None

    except requests.exceptions.RequestException as err:
        logging.error(f'get_data(): exception occurred\n{err.args[0]}')
        return None

    try:
        res_data = res.json()

        try:
            if res_data['status'] == 'error':
                logging.error(f'get_data(): specified params returned error response:{res_data}')
                return None

        except (TypeError, KeyError):
            logging.info('get_data(): response OK')

        if not sort_key:
            logging.info('get_data(): data is not sorted (no sort_key is specified)')
        else:
            try:
                res_data = sorted(res_data, key=lambda x: x[sort_key])
            except KeyError:
                logging.warning(f'get_data(): data is not sorted (sort_key({sort_key}) is invalid)')

        logging.info(f'get_data(): {res_data}')
        return res_data

    except ValueError:
        logging.error(f'get_data(): invalid JSON, could not process data')
        return None


def get_item(item_type, item_code=None):
    items = get_data({'method': f'get{item_type}s'}, 'ID')

    if not items:
        logging.error(f'get_item(): items({item_type}) is null')
        return None

    if item_code == 'all':
        return items

    if isinstance(item_code, int):
        item_code = str(item_code)

    if not item_code:
        logging.warning(f'get_item(): item_code({item_type}) not specified')
        try:
            if item_type.lower() == 'semester':
                return items[-1]
            else:
                return items[0]
        except IndexError:
            logging.error(f'get_item(): items({item_type}) is empty')
            return None

    item = next((sel for sel in items if sel['ID'] == item_code), None)
    logging.info(f'get_item(): {item}')
    return item
