"""Course requirements parser."""

from io import BytesIO

import pandas as pd
import pdfplumber
from pydantic_core import to_json

from nuregi.models import CourseRequirementsBase, Priorities, Requisites
from nuregi.parsers.common import validate_return_as

__requirements_columns = [
    "Abbr",
    "PreRequisite",
    "CoRequisite",
    "AntiRequisite",
    "1st priority registration",
    "2nd priority registration",
    "3rd priority registration",
    "4th priority registration",
]


def __get_requirements_as_dataframe(pdf: BytesIO) -> pd.DataFrame:
    """Converts requirements pdf file to pandas dataframe.

    Args:
        pdf (BytesIO): BytesIO object.

    Returns:
        Requirements as a pandas dataframe.
    """
    with pdfplumber.open(pdf) as content:
        table = [page.extract_table() for page in content.pages]

    table_flat = [elem for table_frag in table for elem in table_frag]
    dataframe = pd.DataFrame(table_flat)
    dataframe = dataframe.replace({r"^\s+": "", r"\s+$": "", r"\s\s+": " "}, regex=True).replace(r"\n", " ", regex=True)
    dataframe = dataframe[1:]
    return dataframe.dropna(subset=["Abbr"])


@validate_return_as(["json", "dataframe", "list"])
def parse_course_requirements_pdf(
    pdf: BytesIO,
    return_as: str = "json",
) -> str | pd.DataFrame | list[CourseRequirementsBase]:
    """Course requirements PDF parser.

    Args:
        pdf: BytesIO object.
        return_as: output format (dataframe, json). Default is "json".

    Returns:
        Course requirements.
    """
    dataframe = __get_requirements_as_dataframe(pdf)
    if return_as == "dataframe":
        return dataframe
    if not all(column in dataframe.columns for column in __requirements_columns):
        msg = f"Course requirements is missing required columns: {__requirements_columns}"
        raise KeyError(msg)
    dataframe = dataframe[__requirements_columns]
    dataframe = dataframe.replace({pd.NA: None})
    course_requirements = []
    for _, course in dataframe.iterrows():
        requisites = Requisites(
            pre=course["PreRequisite"],
            co=course["CoRequisite"],
            anti=course["AntiRequisite"],
        )
        priorities = Priorities(
            one=course["1st priority registration"],
            two=course["2nd priority registration"],
            three=course["3rd priority registration"],
            four=course["4th priority registration"],
        )
        course_requirement = CourseRequirementsBase(
            code=course["Abbr"],
            requisites=requisites,
            priorities=priorities,
        )
        course_requirements.append(course_requirement)
    if return_as == "list":
        return course_requirements
    return to_json(course_requirements).decode("utf-8")
