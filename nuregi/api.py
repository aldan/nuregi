"""Registrar Public Course Catalog API."""

import operator
from enum import Enum
from typing import Any

import requests

from nuregi.exceptions import APIError, ValidationError

BASE_URL_DEFAULT = "https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json"


class RegistrarObject(Enum):
    """Registrar object types."""

    SEMESTER = "semester"
    SCHOOL = "school"
    ACADEMIC_LEVEL = "level"
    DEPARTMENT = "department"
    SUBJECT = "subject"
    INSTRUCTOR = "instructor"
    BREADTH = "breadth"


class RegistrarAPI:
    """Registrar API object."""

    def __init__(
        self,
        base_url: str = BASE_URL_DEFAULT,
        timeout: int | None = None,
        requests_verify: Any = True,  # noqa: ANN401
    ) -> None:
        """Initialize the Registrar API object.

        Args:
            base_url (str, optional): Registrar API base url. Defaults to BASE_URL_DEFAULT.
            timeout (int | None): Timeout in seconds. Defaults to None.
            requests_verify (Any, optional): Whether to verify requests. Defaults to True.
        """
        self.session = requests.Session()
        self.base_url = base_url
        self.timeout = timeout
        self.requests_verify = requests_verify

    def post_request(self, request_data: dict, sort_by: str | None = None) -> list | dict:
        """Get course data from public course catalog.

        Args:
            request_data (dict): Request data.
            sort_by (str, optional): Sort data by key.

        Returns:
            list: List of dicts / dict.

        Raises:
            APIError: Request failed.
            ValidationError: sort_by key invalid.
        """
        response = self.session.post(
            self.base_url,
            data=request_data,
            timeout=self.timeout,
            verify=self.requests_verify,
        )

        response.raise_for_status()
        response_data = response.json()

        if isinstance(response_data, dict) and response_data.get("status") == "error":
            msg = f"Error occurred while processing the request: {response_data}"
            raise APIError(msg)

        if sort_by:
            try:
                response_data = sorted(response_data, key=operator.itemgetter(sort_by))
            except KeyError as error:
                msg = f"Invalid sort_by key: {sort_by}"
                raise ValidationError(msg) from error

        return response_data

    def get_registrar_object(self, object_type: RegistrarObject, object_id: str | int | None = None) -> dict | list:
        """Generic function to get a Registrar object.

        Args:
            object_type (RegistrarObject): Registrar object type.
            object_id (str, optional): Registrar object with specified ID or all. Defaults to None.

        Returns:
            dict: Registrar object(s).

        Raises:
            ValidationError: object_id key invalid.
        """
        objects = self.post_request({"method": f"get{object_type.value}s"}, "ID")

        if object_id is None:
            return objects

        object_id = str(object_id)

        try:
            return next(obj for obj in objects if obj["ID"] == object_id)
        except StopIteration as error:
            msg = f"Invalid object_id: {object_id}"
            raise ValidationError(msg) from error

    def get_semester(self, object_id: str | int | None = None) -> dict | list:
        """Returns semester if ID is specified, otherwise returns all semesters.

        Args:
            object_id (str, optional): Registrar object with specified ID. Defaults to None.

        Returns:
            dict: Registrar object(s).
        """
        return self.get_registrar_object(RegistrarObject.SEMESTER, object_id)

    def get_school(self, object_id: str | int | None = None) -> dict | list:
        """Returns school if ID is specified, otherwise returns all schools.

        Args:
            object_id (str, optional): Registrar object with specified ID. Defaults to None.

        Returns:
            dict: Registrar object(s).
        """
        return self.get_registrar_object(RegistrarObject.SCHOOL, object_id)

    def get_academic_level(self, object_id: str | int | None = None) -> dict | list:
        """Returns academic_level if ID is specified, otherwise returns all academic_levels.

        Args:
            object_id (str, optional): Registrar object with specified ID. Defaults to None.

        Returns:
            dict: Registrar object(s).
        """
        return self.get_registrar_object(RegistrarObject.ACADEMIC_LEVEL, object_id)

    def get_department(self, object_id: str | int | None = None) -> dict | list:
        """Returns department if ID is specified, otherwise returns all departments.

        Args:
            object_id (str, optional): Registrar object with specified ID. Defaults to None.

        Returns:
            dict: Registrar object(s).
        """
        return self.get_registrar_object(RegistrarObject.DEPARTMENT, object_id)

    def get_subject(self, object_id: str | int | None = None) -> dict | list:
        """Returns subject if ID is specified, otherwise returns all subjects.

        Args:
            object_id (str, optional): Registrar object with specified ID. Defaults to None.

        Returns:
            dict: Registrar object(s).
        """
        return self.get_registrar_object(RegistrarObject.SUBJECT, object_id)

    def get_instructor(self, object_id: str | int | None = None) -> dict | list:
        """Returns instructor if ID is specified, otherwise returns all instructors.

        Args:
            object_id (str, optional): Registrar object with specified ID. Defaults to None.

        Returns:
            dict: Registrar object(s).
        """
        return self.get_registrar_object(RegistrarObject.INSTRUCTOR, object_id)

    def get_breadth(self, object_id: str | int | None = None) -> dict | list:
        """Returns breadth if ID is specified, otherwise returns all breadths.

        Args:
            object_id (str, optional): Registrar object with specified ID. Defaults to None.

        Returns:
            dict: Registrar object(s).
        """
        return self.get_registrar_object(RegistrarObject.BREADTH, object_id)

    def get_course_list(  # noqa: PLR0913
        self,
        limit: str | int,
        offset: str | int | None = None,
        semester_id: str | int | None = None,
        school_id: str | int | None = None,
        department_id: str | int | None = None,
        level_id: str | int | None = None,
        subject_id: str | int | None = None,
        instructor_id: str | int | None = None,
        breadth_id: str | int | None = None,
    ) -> list | dict:
        """Looks up search data.

        Args:
            limit (str, optional): Number of results to return. Defaults to None.
            offset (str, optional): Offset of results to return. Defaults to None.
            semester_id (str, optional): Registrar object with specified ID. Defaults to None.
            school_id (str, optional): Registrar object with specified ID. Defaults to None.
            department_id (str, optional): Registrar object with specified ID. Defaults to None.
            level_id (str, optional): Registrar object with specified ID. Defaults to None.
            subject_id (str, optional): Registrar object with specified ID. Defaults to None.
            instructor_id (str, optional): Registrar object with specified ID. Defaults to None.
            breadth_id (str, optional): Registrar object with specified ID. Defaults to None.

        Returns:
            Search data.
        """
        args = list(locals().values())[1:]
        brackets = [""] * len(args)

        if not args[1]:
            args[1] = "1"

        if not args[2]:
            args[2] = "-1"

        for index, arg in enumerate(args):
            if arg:
                brackets[index] = "[]"
            if not arg:
                args[index] = ""
            if isinstance(arg, int):
                args[index] = str(arg)

        request_data = {
            "method": "getSearchData",
            "searchParams[formSimple]": "false",
            "searchParams[limit]": args[0],
            "searchParams[page]": args[1],
            "searchParams[start]": "0",
            "searchParams[quickSearch]": "",
            "searchParams[sortField]": "-1",
            "searchParams[sortDescending]": "-1",
            "searchParams[semester]": args[2],
            f"searchParams[schools]{brackets[3]}": args[3],
            f"searchParams[departments]{brackets[4]}": args[4],
            f"searchParams[levels]{brackets[5]}": args[5],
            f"searchParams[subjects]{brackets[6]}": args[6],
            f"searchParams[instructors]{brackets[7]}": args[7],
            f"searchParams[breadths]{brackets[8]}": args[8],
            "searchParams[abbrNum]": "",
            "searchParams[credit]": "",
        }

        return self.post_request(request_data)
