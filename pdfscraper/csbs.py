# PDF scraper for Course Schedule By Schools (CSBS) document
import public_course_catalog as pcc

import urllib.error
import urllib.request

import logging

import pandas as pd
import tabula

request_url = 'http://registrar.nu.edu.kz/registrar_downloads/json'
request_timeout = 60


def get_dataframe(semester_code=None, academic_level=None, school_code=None):

    semester = pcc.get_semester(semester_code)
    if not semester:
        logging.error(f'get_dataframe(): semester with code {semester_code} does not exist')
        return None

    if not semester_code:
        semester_code = semester['ID']

    logging.info(f'get_dataframe(): semester name: {semester["NAME"]}, code: {semester_code}')

    # TODO handle academic_level & school_code

    request_params = f'?method=printDocument&name=school_schedule_by_term' +\
                     f'&termid={semester_code}' +\
                     f'&academiclevel=1'

    try:
        with urllib.request.urlopen(f'{request_url}{request_params}', timeout=request_timeout) as csbs_pdf:

            raw_df = tabula.read_pdf(csbs_pdf, pages='all', lattice=True, pandas_options={'header': None})
            raw_df = pd.concat(raw_df, ignore_index=True)
            dataframe = raw_df.replace(r'\r', r' ', regex=True)
            logging.info('get_dataframe(): success [csbs]')
            return dataframe

    except urllib.error.HTTPError as err:
        logging.error(f'get_dataframe(): HTTPError occurred while retrieving CSBS.PDF\n{err}')
        return None

    except urllib.error.URLError as err:
        logging.error(f'get_dataframe(): URLError occurred while retrieving CSBS.PDF\n{err}')
        return None


def get_json():

    dataframe = get_dataframe()
    return dataframe.to_json()


def get_json_as_table():

    dataframe = get_dataframe()
    return dataframe.to_json(orient='table', index=False)
