# Nuregi
[![Downloads](https://pepy.tech/badge/nuregi)](https://pepy.tech/project/nuregi)
![PyPI](https://img.shields.io/pypi/v/nuregi)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/nuregi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nuregi)
![GitHub](https://img.shields.io/github/license/aldan/nuregi?color=brightgreen)

A basic Python-based API client library for registrar.nu.edu.kz

## Requirements
- Python 3.11+

## Installation
Install with [`pip`](https://pypi.org/project/nuregi/):
```
pip install nuregi
```
## Example usage
### API
```python
from nuregi.api import RegistrarAPI


api = RegistrarAPI(timeout=30, requests_verify=True)
fall2022_semester = api.get_semester(object_id=642)
all_semesters = api.get_semester()
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
)
```

### Scraper
Unlike API, Scraper returns data in a defined format. See [models.py](nuregi/models.py) for details.
```python
from nuregi.scraper import Scraper


scraper = Scraper(requests_verify="ca.crt")

current_semester = scraper.get_last_published_semester()
schedule_with_reqs = scraper.get_course_schedule_with_requirements(semester_id=current_semester.id)

fall2022_ug_seds_course_schedule = scraper.get_course_schedule(
    semester_id=642,
    academic_level_id=1,
    school_id=13,
)

fall2022_ug_seds_course_requirements = scraper.get_course_requirements(
    semester_id=642,
    academic_level_id=1,
    school_id=13,
)
```

## Notice
This project is for educational purposes only and should not
be used to interfere with operation of https://registrar.nu.edu.kz/.
