"""Parser for course schedule with requirements."""

import re
from io import BytesIO

import pandas as pd
from pydantic_core import to_json

from nuregi.models import Course, CourseRequirementsBase, CourseWithRequirements
from nuregi.parsers import parse_course_requirements_pdf, parse_course_schedule_xls
from nuregi.parsers.common import validate_return_as


@validate_return_as(["json", "dataframe", "list"])
def parse_course_schedule_with_requirements(
    schedule_xls: BytesIO,
    requirements_pdf: BytesIO,
    return_as: str = "json",
) -> str | pd.DataFrame | list[CourseWithRequirements]:
    """Parse course schedule with requirements.

    Args:
        schedule_xls: Schedule BytesIO object.
        requirements_pdf: Requirements BytesIO object.
        return_as: output format (dataframe, json, list). Default is "json".

    Returns:
        Course schedule with requirements.
    """
    if return_as == "dataframe":
        schedule: pd.DataFrame = parse_course_schedule_xls(schedule_xls, return_as="dataframe")
        requirements: pd.DataFrame = parse_course_requirements_pdf(requirements_pdf, return_as="dataframe")
        schedule = schedule.rename(columns={"Course Abbr": "Abbr"})
        abbr = schedule["Abbr"]
        schedule["Abbr"] = schedule["Abbr"].str.replace({r"\s+": ""}, regex=True)
        requirements["Abbr"] = requirements["Abbr"].str.replace({r"\s+": ""}, regex=True)
        merged = schedule.merge(requirements, how="left", on="Abbr")
        merged["Abbr"] = abbr
        return merged

    courses: list[Course] = parse_course_schedule_xls(schedule_xls, return_as="list")
    requirements: list[CourseRequirementsBase] = parse_course_requirements_pdf(requirements_pdf, return_as="list")
    courses_with_reqs: list[CourseWithRequirements] = []
    reqs_dict = {re.sub(r"\s+", "", req.code): req for req in requirements}
    for course in courses:
        code = re.sub(r"\s+", "", course.code)
        requirement = reqs_dict[code]
        requirement_dict = requirement.model_dump()
        del requirement_dict["code"]
        courses_with_reqs.append(CourseWithRequirements(**course.model_dump(), **requirement_dict))

    if return_as == "list":
        return courses_with_reqs
    return to_json(courses_with_reqs).decode("utf-8")
