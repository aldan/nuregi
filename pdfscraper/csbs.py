# PDF scraper for Course Schedule By Schools (CSBS) document
import public_course_catalog as pcc

import urllib.error
import urllib.request
from socket import timeout

import logging

import pandas as pd
import tabula
import tabula.errors

request_url = 'http://registrar.nu.edu.kz/registrar_downloads/json'
request_timeout = 60


def get_dataframe(semester_code=None, academic_level_code=None, school_code=None):
    if next((arg for arg in locals().values() if arg == 'all'), None):
        logging.error(f'get_dataframe(): at least one of the specified arguments refers to all')
        return None

    if isinstance(semester_code, int):
        semester_code = str(semester_code)

    if isinstance(academic_level_code, int):
        academic_level_code = str(academic_level_code)

    if isinstance(school_code, int):
        school_code = str(school_code)

    semester = pcc.get_semester(semester_code)
    if not semester:
        logging.error(f'get_dataframe(): semester with code {semester_code} does not exist')
        return None

    academic_level = pcc.get_academic_level(academic_level_code)
    if not academic_level:
        logging.error(f'get_dataframe(): academic_level with code {academic_level_code} does not exist')
        return None

    school = pcc.get_school(school_code)
    if not academic_level:
        logging.error(f'get_dataframe(): school with code {school_code} does not exist')
        return None

    if not semester_code:
        semester_code = semester['ID']
        logging.warning(f'semester_code is a required parameter for processing request')
        logging.info(f'{semester_code} was automatically assigned as parameter')

    request_params = f'?method=printDocument&name=school_schedule_by_term&termid={semester_code}'
    request_params += f'&academiclevel={academic_level_code}' if academic_level_code else ''
    request_params += f'&schoolid={school_code}' if school_code else ''
    logging.error(f'get_dataframe(): request url - {request_url}{request_params}')

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

    except timeout:
        logging.error('get_dataframe(): request timed out')
        return None

    except (FileNotFoundError, ValueError, tabula.errors.CSVParseError, tabula.errors.ParserError) as err:
        logging.error(f'get_dataframe(): bad file\n{err.args[0]}')
        return None

    except tabula.errors.JavaNotFoundError:
        logging.error('get_dataframe(): Java not installed/found')
        return None
