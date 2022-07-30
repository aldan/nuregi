# Nuregi

[![Downloads](https://pepy.tech/badge/nuregi)](https://pepy.tech/project/nuregi)
![PyPI](https://img.shields.io/pypi/v/nuregi)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/nuregi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nuregi)
![GitHub](https://img.shields.io/github/license/aldan/nuregi?color=brightgreen)

A basic Python-based API client library for registrar.nu.edu.kz

## Requirements

- Python 3.8+
- `OPTIONAL` Java 8+ is required to use `scraper.pdf` package

## Installation

Install with [`pip`](https://pypi.org/project/nuregi/): 

```
pip install nuregi
```

## Usage
> Refer to function docstrings for complete set of arguments
### `nuregi.api`

```python
from nuregi import api

"""
All get_object type functions have object_id and timeout arguments
"""

# Sample for semesters
fall2022_semester = api.get_semester(object_id=642, timeout=10)
all_semesters = api.get_semester(timeout=10)

# Other objects
schools = api.get_school()
academic_levels = api.get_academic_level()
departments = api.get_department()
subjects = api.get_subject()
instructors = api.get_instructor()
breadth = api.get_breadth()  # likely deprecated

course_list = api.get_course_list(
    limit=10,
    offset=1,
    semester_id=642,
    school_id=13,
    department_id=None,
    level_id=1,
    subject_id=None,
    instructor_id=None,
    breadth_id=None,
    timeout=10,
)
```

### `nuregi.scraper.pdf`

```python
from nuregi.scraper.pdf import *

fall2022_ug_seds_schedule = get_schedule(
    data_format="columns",
    semester=642,
    academic_level=1,
    school=13,
    timeout=15,
)

fall2022_ug_seds_course_requirements = get_requirements(
    data_format="table",
    semester=642,
    academic_level=1,
    school=13,
    timeout=15,
)

spring2022_seds_finals = get_final_schedule(
    data_format="columns",
    semester=642,
    school=13,
    timeout=15
)
```

## Dependencies
- [Requests](https://github.com/psf/requests)
- [Tabula-py](https://github.com/chezou/tabula-py)
- [numpy](https://github.com/numpy/numpy)
- [pandas](https://github.com/pandas-dev/pandas)

## Notice

This project is for educational purposes only and should not 
be used to interfere with operation of https://registrar.nu.edu.kz/.