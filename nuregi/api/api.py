"""
Tools to interact with Registrar Public Course Catalog API
"""

import logging
from enum import Enum

import requests
from requests.exceptions import SSLError

from nuregi.exceptions import APIError, ValidationError

BASE_URL = "https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json"


class RegistrarObject(Enum):
    SEMESTER = "semester"
    SCHOOL = "school"
    ACADEMIC_LEVEL = "level"
    DEPARTMENT = "department"
    SUBJECT = "subject"
    INSTRUCTOR = "instructor"
    BREADTH = "breadth"


def post_request(request_data, sort_by=None, timeout=None):
    """
    Get course data from public course catalog
    :param request_data: request form data
    :param sort_by: key to sort by if specified
    :param timeout: time to wait for Registrar to respond
    :return: course data in JSON format
    """

    try:
        response = requests.post(BASE_URL, data=request_data, timeout=timeout)
    except SSLError:
        # nu.edu.kz isnt providing full certificate chain so requests raises SSLError
        response = requests.post(BASE_URL, data=request_data, timeout=timeout, verify=False)

    logging.info(response.url, response.status_code)
    response.raise_for_status()

    response_data = response.json()

    if isinstance(response_data, dict) and response_data.get("status") == "error":
        logging.error(response_data)
        raise APIError(f"Error occurred while processing the request: {response_data}")

    if sort_by:
        try:
            response_data = sorted(response_data, key=lambda x: x[sort_by])
        except KeyError:
            raise ValidationError(f"Invalid sort_by key: {sort_by}")

    return response_data


def get_registrar_object(object_type: RegistrarObject, object_id=None, timeout=None):
    """
    Generic function to get Registrar object
    :param object_type: type of RegistrarObject
    :param object_id: object ID
    :param timeout: time to wait for Registrar to respond
    :return:
    """
    objects = post_request({"method": f"get{object_type.value}s"}, "ID", timeout)

    if object_id is None:
        return objects

    object_id = str(object_id)

    try:
        obj = next((obj for obj in objects if obj["ID"] == object_id))
        return obj
    except StopIteration:
        raise ValidationError(f"Invalid object_id: {object_id}")


def get_semester(object_id=None, timeout=None):
    """
    Returns semester if ID is specified, otherwise returns all semesters
    :param object_id: semester ID
    :param timeout: time to wait for Registrar to respond
    :return: semester object(s)
    """
    return get_registrar_object(RegistrarObject.SEMESTER, object_id, timeout=timeout)


def get_school(object_id=None, timeout=None):
    """
    Returns school if ID is specified, otherwise returns all schools
    :param object_id: school ID
    :param timeout: time to wait for Registrar to respond
    :return: school object(s)
    """
    return get_registrar_object(RegistrarObject.SCHOOL, object_id, timeout=timeout)


def get_academic_level(object_id=None, timeout=None):
    """
    Returns academic_level if ID is specified, otherwise returns all academic_levels
    :param object_id: academic_level ID
    :param timeout: time to wait for Registrar to respond
    :return: academic_level object(s)
    """
    return get_registrar_object(RegistrarObject.ACADEMIC_LEVEL, object_id, timeout=timeout)


def get_department(object_id=None, timeout=None):
    """
    Returns department if ID is specified, otherwise returns all departments
    :param object_id: department ID
    :param timeout: time to wait for Registrar to respond
    :return: department object(s)
    """
    return get_registrar_object(RegistrarObject.DEPARTMENT, object_id, timeout=timeout)


def get_subject(object_id=None, timeout=None):
    """
    Returns subject if ID is specified, otherwise returns all subjects
    :param object_id: subject ID
    :param timeout: time to wait for Registrar to respond
    :return: subject object(s)
    """
    get_registrar_object(RegistrarObject.SUBJECT, object_id, timeout=timeout)


def get_instructor(object_id=None, timeout=None):
    """
    Returns instructor if ID is specified, otherwise returns all instructors
    :param object_id: instructor ID
    :param timeout: time to wait for Registrar to respond
    :return: instructor object(s)
    """
    return get_registrar_object(RegistrarObject.INSTRUCTOR, object_id, timeout=timeout)


def get_breadth(object_id=None, timeout=None):
    """
    Returns breadth if ID is specified, otherwise returns all breadths
    :param object_id: breadth ID
    :param timeout: time to wait for Registrar to respond
    :return: breadth object(s)
    """
    return get_registrar_object(RegistrarObject.BREADTH, object_id, timeout=timeout)


def get_course_list(limit, offset=None, semester_id=None, school_id=None, department_id=None,
                    level_id=None, subject_id=None, instructor_id=None, breadth_id=None, timeout=None):
    args = list(locals().values())
    brackets = [''] * len(args)

    if not args[1]:
        args[1] = '1'

    if not args[2]:
        args[2] = '-1'

    for index, arg in enumerate(args):
        if arg:
            brackets[index] = '[]'
        if not arg:
            args[index] = ''
        if isinstance(arg, int):
            args[index] = str(arg)

    request_data = {
        'method': 'getSearchData',
        'searchParams[formSimple]': 'false',
        'searchParams[limit]': args[0],
        'searchParams[page]': args[1],
        'searchParams[start]': '0',
        'searchParams[quickSearch]': '',
        'searchParams[sortField]': '-1',
        'searchParams[sortDescending]': '-1',
        'searchParams[semester]': args[2],
        f'searchParams[schools]{brackets[3]}': args[3],
        f'searchParams[departments]{brackets[4]}': args[4],
        f'searchParams[levels]{brackets[5]}': args[5],
        f'searchParams[subjects]{brackets[6]}': args[6],
        f'searchParams[instructors]{brackets[7]}': args[7],
        f'searchParams[breadths]{brackets[8]}': args[8],
        'searchParams[abbrNum]': '',
        'searchParams[credit]': ''
    }

    course_list = post_request(request_data, timeout=timeout)
    return course_list
