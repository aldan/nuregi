"""Document scraper."""

import re
from enum import Enum
from io import BytesIO
from typing import Any

import requests

from nuregi.exceptions import ParsingError
from nuregi.models import Semester
from nuregi.parsers import (
    parse_course_requirements_pdf,
    parse_course_schedule_with_requirements,
    parse_course_schedule_xls,
)

BASE_DOWNLOAD_URL = "https://registrar.nu.edu.kz/registrar_downloads/json"
COURSE_SCHEDULES_URL = "https://registrar.nu.edu.kz/course-schedules"


class DocumentType(Enum):
    """Document types available on Registrar."""

    XLS_SCHEDULE = "xls_school_schedule_by_term"
    FINAL = "final_exams_schedule"
    REQUIREMENTS = "course_requirements"


class Scraper:
    """Web scraper for registrar."""

    def __init__(self, timeout: int = 30, requests_verify: Any = True) -> None:  # noqa: ANN401
        """Initialize scraper.

        Args:
            timeout (int, optional): Timeout in seconds. Defaults to 30.
            requests_verify (Any, optional): Whether to verify requests. Defaults to True.
        """
        self.timeout = timeout
        self.requests_verify = requests_verify

    def get_last_published_semester(self) -> Semester:
        """Obtain the last semester from the course schedules page.

        Returns Semester object.

        Raises:
            ParsingError: If no semester was found.
        """
        response = requests.get(COURSE_SCHEDULES_URL, timeout=self.timeout, verify=self.requests_verify)
        response.raise_for_status()
        text = response.text

        try:
            text = text[text.index("Course schedules for ") :]
            semester_id = re.search(r"termid=(\d+)", text)[1]
            semester_name = re.search(r"(Fall|Spring|Summer) \d{4}", text)[0]
        except (TypeError, ValueError) as exc:
            msg = "Failed to retrieve last published semester"
            raise ParsingError(msg) from exc

        return Semester(id=semester_id, name=semester_name)

    def get_document(
        self,
        doctype: DocumentType,
        parse: bool = True,
        extra_params: dict | None = None,
    ) -> str | BytesIO:
        """Helper function to download the document.

        Args:
            doctype (DocumentType): Document type.
            parse (bool, optional): Whether to parse the document. Defaults to True.
            extra_params (dict, optional): Extra parameters for request. Defaults to None.

        Returns:
            Document as string (parsed JSON) or BytesIO (raw file).
        """
        params = {
            "method": "printDocument",
            "name": doctype.value,
            **extra_params,
        }
        response = requests.get(
            BASE_DOWNLOAD_URL,
            params=params,
            timeout=self.timeout,
            verify=self.requests_verify,
        )
        response.raise_for_status()
        document = BytesIO(response.content)

        if not parse:
            return document
        if doctype is DocumentType.XLS_SCHEDULE:
            return parse_course_schedule_xls(document)
        if doctype is DocumentType.REQUIREMENTS:
            return parse_course_requirements_pdf(document)
        msg = f"get_document(parse=True) is not implemented for doctype {DocumentType.FINAL}"
        raise NotImplementedError(msg)

    def get_course_schedule(
        self,
        semester_id: str | int,
        academic_level_id: str | int | None = None,
        school_id: str | int | None = None,
    ) -> str:
        """Get course schedule in JSON format.

        Args:
            semester_id (str): Semester id.
            academic_level_id (str, optional): Academic level id.
            school_id (str, optional): School id.

        Returns:
            Course schedule in JSON format.
        """
        extra_params = {
            "termid": semester_id,
            "academiclevel": academic_level_id,
            "schoolid": school_id,
        }

        return self.get_document(DocumentType.XLS_SCHEDULE, extra_params=extra_params)

    def get_course_requirements(
        self,
        semester_id: str | int,
        academic_level_id: str | int | None = None,
        school_id: str | int | None = None,
    ) -> str:
        """Get course requirements in JSON format.

        Args:
            semester_id (str): Semester id.
            academic_level_id (str, optional): Academic level id.
            school_id (str, optional): School id.

        Returns:
            Course requirements in JSON format.
        """
        extra_params = {
            "termid": semester_id,
            "academiclevel": academic_level_id,
            "schoolid": school_id,
        }

        return self.get_document(DocumentType.REQUIREMENTS, extra_params=extra_params)

    def get_course_schedule_with_requirements(
        self,
        semester_id: str | int,
        academic_level_id: str | int | None = None,
        school_id: str | int | None = None,
    ) -> str:
        """Get course schedule with requirements in JSON format.

        Args:
            semester_id (str): Semester id.
            academic_level_id (str, optional): Academic level id.
            school_id (str, optional): School id.

        Returns:
            Course schedule with requirements in JSON format.
        """
        extra_params = {
            "termid": semester_id,
            "academiclevel": academic_level_id,
            "schoolid": school_id,
        }

        schedule = self.get_document(DocumentType.XLS_SCHEDULE, extra_params=extra_params, parse=False)
        requirements = self.get_document(DocumentType.REQUIREMENTS, extra_params=extra_params, parse=False)
        return parse_course_schedule_with_requirements(schedule, requirements)

    def get_finals_schedule(self, semester_id: str | int, school_id: str | int) -> str:
        """Get course finals schedule in JSON format.

        Args:
            semester_id (str): Semester id.
            school_id (str): School id.
        """
        extra_params = {
            "termid": semester_id,
            "schoolid": school_id,
            "type": "pdf",
        }

        return self.get_document(DocumentType.FINAL, extra_params=extra_params)
