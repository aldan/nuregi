# Nuregi
[![Downloads](https://pepy.tech/badge/nuregi)](https://pepy.tech/project/nuregi)
![PyPI](https://img.shields.io/pypi/v/nuregi)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/nuregi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nuregi)
![GitHub](https://img.shields.io/github/license/aldan/nuregi?color=brightgreen)

A basic Python-based API client library for registrar.nu.edu.kz

## Requirements
- Python 3.11+
- Java 8+ is required to use tabula-py

## Installation
Install with [`pip`](https://pypi.org/project/nuregi/):
```
pip install nuregi
```

## Usage
### API
```python
import nuregi

"""
All get_object type functions have object_id and timeout arguments
"""

# Sample for semesters
fall2022_semester = nuregi.get_semester(object_id=642, timeout=10)
all_semesters = nuregi.get_semester(timeout=10)

# Other objects
schools = nuregi.get_school()
academic_levels = nuregi.get_academic_level()
departments = nuregi.get_department()
subjects = nuregi.get_subject()
instructors = nuregi.get_instructor()
breadth = nuregi.get_breadth()  # likely deprecated

course_list = nuregi.get_course_list(
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

### Scraper
```python
import nuregi

scraper = nuregi.Scraper(timeout=10, ignore_ssl=True)

current_semester = scraper.get_last_published_semester()

fall2022_ug_seds_course_schedule = scraper.get_course_schedule(
    semester=642,
    academic_level=1,
    school=13,
)

fall2022_ug_seds_course_requirements = scraper.get_course_requirements(
    semester=642,
    academic_level=1,
    school=13,
)

spring2022_seds_finals = scraper.get_finals_schedule(
    semester=642,
    school=13,
)
```

## Notice
This project is for educational purposes only and should not
be used to interfere with operation of https://registrar.nu.edu.kz/.
