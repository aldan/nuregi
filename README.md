# Nuregi

[![Downloads](https://pepy.tech/badge/nuregi)](https://pepy.tech/project/nuregi)
![PyPI](https://img.shields.io/pypi/v/nuregi)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/nuregi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nuregi)
![GitHub](https://img.shields.io/github/license/aldan/nuregi?color=brightgreen)

A basic Python-based API client library for registrar.nu.edu.kz

## Requirements

- Python 3.6+
- `OPTIONAL` Java 8+ is required to use `pdfparser` package

## Installation

Install with [`pip`](https://pypi.org/project/nuregi/): 

```
pip install nuregi
```

## Usage

#### `public_course_catalog`

```python
import public_course_catalog as pcc


spring_2021_semester = pcc.get_semester(semester_code=541, timeout=1)
print(spring_2021_semester)

all_schools = pcc.get_school(school_code='all')
print(all_schools)

undergraduate_level = pcc.get_academic_level(level_code=1, timeout=1)
print(undergraduate_level)

all_departments = pcc.get_department(department_code='all', timeout=1)
print(all_departments)

instructor_with_id1 = pcc.get_instructor()
print(instructor_with_id1)

all_subjects = pcc.get_subject('all')
print(all_subjects)

course_list = pcc.get_course_list(
    limit=10,
    offset=1,
    semester_code=541,
    school_code=13,
    department_code=None,
    level_code=1,
    subject_code=None,
    instructor_code=None,
    breadth_code=None,
    timeout=5
)
print(course_list)
```

#### `pdfscraper`

```python
import pdfscraper


json_data = pdfscraper.get_csbs_as_json_columns(
    semester_code=541,
    academic_level_code=1,
    school_code=13,
    request_timeout=10,
    verify_params=True,
    verification_timeout=3
)

with open('csbs.json', 'w') as output_file:
    output_file.write(str(json_data))
```

## Credits

Used in the project:
- [Requests](https://github.com/psf/requests)
- [Tabula-py](https://github.com/chezou/tabula-py)

## Fair Use Disclaimer

This project is for educational purposes only and should not 
be utilized to interfere with operation of https://registrar.nu.edu.kz/.