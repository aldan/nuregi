"""
PDF scraper for documents from Registrar
"""
from enum import Enum
from io import BytesIO

import pandas as pd
import requests
from requests.exceptions import SSLError
from tabula import read_pdf

from nuregi.exceptions import APIError

PDF_DOWNLOAD_URL = "https://registrar.nu.edu.kz/registrar_downloads/json"
COURSE_SCHEDULES_URL = "https://registrar.nu.edu.kz/course-schedules"


class PdfType(Enum):
    """
    Allowed file types available on Registrar
    """

    SCHEDULE = "school_schedule_by_term"
    FINAL = "final_exams_schedule"
    REQUIREMENTS = "course_requirements"


class Scraper:
    """
    Web scraper for registrar
    """

    def __init__(self, timeout: int = 30, ignore_ssl: bool = False):
        self.timeout = timeout
        self.ignore_ssl = ignore_ssl

    def get_last_published_semester(self):
        """
        Obtains the last semester from the courses schedule page.
        Returns the same object as api.get_semester()
        """
        try:
            response = requests.get(COURSE_SCHEDULES_URL, timeout=self.timeout)
        except SSLError as error:
            if self.ignore_ssl:
                response = requests.get(
                    COURSE_SCHEDULES_URL, timeout=self.timeout, verify=False
                )
            else:
                raise APIError from error

        response.raise_for_status()
        text = response.text
        start = text.index(
            '<a href="https://registrar.nu.edu.kz/registrar_downloads/json?method=printDocument'
        )
        end = text.index("</a>", start)
        element = text[start:end]
        start = element.index("termid=") + 7
        end = element.index('"', start)
        semester_id = element[start:end]
        semester_name = element[end + 2 :]

        return {
            "ID": semester_id,
            "NAME": semester_name,
        }

    def get_pdf(
        self, pdf_type: PdfType, as_json: bool = False, extra_params: dict = None
    ):
        """
        Helper function for parsing tables from a PDF file
        """
        params = {
            "method": "printDocument",
            "name": pdf_type.value,
            **extra_params,
        }
        print(params)

        try:
            response = requests.get(
                PDF_DOWNLOAD_URL, params=params, timeout=self.timeout
            )
        except SSLError as error:
            if self.ignore_ssl:
                response = requests.get(
                    PDF_DOWNLOAD_URL, params=params, timeout=self.timeout, verify=False
                )
            else:
                raise APIError from error

        response.raise_for_status()
        content = BytesIO(response.content)

        if not as_json:
            return content

        try:
            dataframe = read_pdf(
                content, pages="all", lattice=True, pandas_options={"header": None}
            )
        except UnicodeDecodeError:
            # fallback to cp1252 if utf-8 fails
            dataframe = read_pdf(
                content,
                encoding="cp1252",
                pages="all",
                lattice=True,
                pandas_options={"header": None},
            )

        dataframe = pd.concat(dataframe, ignore_index=True).replace(
            r"\r", r" ", regex=True
        )
        return dataframe.to_json(orient="table", index=False)

    def get_course_schedule(self, semester, academic_level=None, school=None):
        """
        Get course schedule in JSON format
        :param semester: semester(term) id
        :param academic_level: academic level id
        :param school: school id
        :return: course schedule in JSON format
        """
        params = {
            "termid": semester,
            "academiclevel": academic_level,
            "schoolid": school,
        }

        return self.get_pdf(PdfType.SCHEDULE, as_json=True, extra_params=params)

    def get_course_requirements(self, semester, academic_level=None, school=None):
        """
        Get course requirements in JSON format
        :param semester: semester(term) id
        :param academic_level: academic level id
        :param school: school id
        :return: course requirements in JSON format
        """
        params = {
            "termid": semester,
            "academiclevel": academic_level,
            "schoolid": school,
        }

        return self.get_pdf(PdfType.REQUIREMENTS, as_json=True, extra_params=params)

    def get_finals_schedule(self, semester, school):
        """
        Get course finals schedule in JSON format
        :param semester: semester(term) id
        :param school: school id
        :return: finals schedule in JSON format
        """
        params = {
            "termid": semester,
            "schoolid": school,
            "type": "pdf",
        }

        return self.get_pdf(PdfType.FINAL, as_json=True, extra_params=params)
