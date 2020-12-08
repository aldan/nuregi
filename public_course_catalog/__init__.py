# Wrapper for Public Course Catalog API

import public_course_catalog.helpers as helpers


def get_semester(semester_code=None):
    semester = helpers.get_item('semester', semester_code)
    return semester


def get_school(school_code=None):
    school = helpers.get_item('school', school_code)
    return school


def get_academic_level(level_code=None):
    academic_level = helpers.get_item('level', level_code)
    return academic_level


def get_department(department_code=None):
    department = helpers.get_item('department', department_code)
    return department


def get_subject(subject_code=None):
    subject = helpers.get_item('subject', subject_code)
    return subject


def get_instructor(instructor_code=None):
    instructor = helpers.get_item('instructor', instructor_code)
    return instructor


def get_breadth(breadth_code=None):
    breadth = helpers.get_item('breadth', breadth_code)
    return breadth


def get_course_list(limit, offset=None, semester_code=None, school_code=None, department_code=None,
                    level_code=None, subject_code=None, instructor_code=None, breadth_code=None):
    args = list(locals().values())
    brackets = [''] * 9

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

    course_list = helpers.get_data(request_data)
    return course_list
