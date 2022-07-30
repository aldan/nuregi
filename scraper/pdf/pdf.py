"""
PDF scraper for documents from Registrar
"""
import logging
from enum import Enum
from io import BytesIO

import pandas as pd
import requests
from tabula import read_pdf

from .exceptions import ValidationError

BASE_URL = "https://registrar.nu.edu.kz/registrar_downloads/json"


class PdfType(Enum):
    """
    Allowed file types available on Registrar
    """
    SCHEDULE = "school_schedule_by_term"
    FINAL = "final_exams_schedule"
    REQUIREMENTS = "course_requirements"


def convert_pdf_to_json(pdf_type: PdfType, data_format, extra_params=None, timeout=None):
    """
    Converts selected PDF file to JSON format
    :param pdf_type: PdfType to convert
    :param data_format: format used to generate JSON. Allowed values are {'table', 'columns'}
    :param extra_params: extra parameters required to generate file
    :param timeout: time to wait for Registrar to respond
    :return: str object in JSON format
    """

    params = {
        "method": "printDocument",
        "name": pdf_type.value,
        **extra_params,
    }

    if data_format not in ("table", "columns"):
        raise ValidationError("data_format must be equal to either 'table' or 'column'.")

    if extra_params is not None and not isinstance(extra_params, dict):
        raise ValidationError("extra_params must be a dict")

    response = requests.get(BASE_URL, params=params, timeout=timeout)
    logging.info(response.url, response.status_code)
    response.raise_for_status()
    content = BytesIO(response.content)

    try:
        # try to read binary file with utf-8 encoding
        dataframe = read_pdf(content, pages='all', lattice=True, pandas_options={'header': None})
    except UnicodeDecodeError:
        # fallback to cp1252
        logging.warning("convert_pdf_to_json(): failed to read data with utf-8 encoding. falling back to cp1252")
        dataframe = read_pdf(content, encoding="cp1252", pages='all', lattice=True, pandas_options={'header': None})

    dataframe = pd.concat(dataframe, ignore_index=True).replace(r'\r', r' ', regex=True)

    return dataframe.to_json(orient=data_format, index=(data_format == "columns"))


def get_schedule(data_format, semester, academic_level=None, school=None, timeout=None):
    """
    Get course schedule in JSON format
    :param data_format: format used to generate JSON. Allowed values are {'table', 'columns'}
    :param semester: semester(term) id
    :param academic_level: academic level id
    :param school: school id
    :param timeout: time to wait for Registrar to respond
    :return: str object in JSON format
    """

    params = {
        "termid": semester,
        "academiclevel": academic_level,
        "schoolid": school,
    }

    return convert_pdf_to_json(PdfType.SCHEDULE, data_format, params, timeout)


def get_final_schedule(data_format, semester, school, timeout=None):
    """
    Get course final schedule in JSON format
    :param data_format: format used to generate JSON. Allowed values are {'table', 'columns'}
    :param semester: semester(term) id
    :param school: school id
    :param timeout: time to wait for Registrar to respond
    :return: str object in JSON format
    """

    params = {
        "termid": semester,
        "schoolid": school,
        "type": "pdf",
    }

    return convert_pdf_to_json(PdfType.FINAL, data_format, params, timeout)


def get_requirements(data_format, semester, academic_level=None, school=None, timeout=None):
    """
    Get course requirements in JSON format
    :param data_format: format used to generate JSON. Allowed values are {'table', 'columns'}
    :param semester: semester(term) id
    :param academic_level: academic level id
    :param school: school id
    :param timeout: time to wait for Registrar to respond
    :return: str object in JSON format
    """

    params = {
        "termid": semester,
        "academiclevel": academic_level,
        "schoolid": school,
    }

    return convert_pdf_to_json(PdfType.REQUIREMENTS, data_format, params, timeout)
