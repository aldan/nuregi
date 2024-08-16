"""Course schedule parser."""

from datetime import UTC, datetime
from io import BytesIO

import pandas as pd
from pydantic_core import to_json

from nuregi.models import Course, Section, SectionPeriod
from nuregi.parsers.common import validate_return_as

__schedule_columns = [
    "School",
    "Level",
    "Course Abbr",
    "S/T",
    "Course Title",
    "Cr(US)",
    "Cr(ECTS)",
    "Start date",
    "End date",
    "Days",
    "Time",
    "Enr",
    "Cap",
    "Faculty",
    "Room",
]


def __convert_time_to_minutes(weekday_letter: str, time_string: str) -> int:
    """Converts course schedule day & time to minutes.

    Args:
        weekday_letter: weekday letter
        time_string: time string

    Returns:
        Time in minutes (relative to week).
    """
    weekday_minutes = {"M": 0, "T": 1440, "W": 2880, "R": 4320, "F": 5760, "S": 7200}
    time = datetime.strptime(time_string, "%I:%M %p").replace(tzinfo=UTC)
    return weekday_minutes[weekday_letter.strip()] + time.hour * 60 + time.minute


def __get_schedule_as_dataframe(xls: BytesIO) -> pd.DataFrame:
    """Converts schedule excel file to pandas dataframe.

    Args:
        xls (BytesIO): BytesIO object.

    Returns:
        Schedule as a pandas dataframe.
    """
    # ignore xlrd corruption error https://stackoverflow.com/questions/12705527/reading-excel-files-with-xlrd
    return pd.read_excel(xls, header=2, engine="xlrd", engine_kwargs={"ignore_workbook_corruption": True})


@validate_return_as(["json", "dataframe", "list"])
def parse_course_schedule_xls(xls: BytesIO, return_as: str = "json") -> str | pd.DataFrame | list[Course]:
    """Course schedule XLS parser.

    Args:
        xls: BytesIO object.
        return_as: output format (dataframe, json, list). Default is "json".

    Returns:
        Course schedule.

    Raises:
        KeyError: If columns in course schedule excel file are missing.
    """
    dataframe = __get_schedule_as_dataframe(xls)
    if return_as == "dataframe":
        return dataframe

    if not all(column in dataframe.columns for column in __schedule_columns):
        msg = f"Course schedule is missing required columns: {__schedule_columns}"
        raise KeyError(msg)
    dataframe = dataframe.replace({pd.NA: None})
    courses: list[Course] = []
    for _, course in dataframe.groupby("Course Abbr"):
        sections: list[Section] = []
        for _, course_section in course.groupby("S/T"):
            periods: list[SectionPeriod] = []
            for _, period_data in course_section.iterrows():
                is_distant = period_data["Time"] == "Online/Distant"
                if is_distant:
                    periods.append(SectionPeriod(start=None, end=None, room=None, distant=True))
                    continue
                periods.append(
                    SectionPeriod(
                        start=__convert_time_to_minutes(period_data["Days"], period_data["Time"].split("-")[0]),
                        end=__convert_time_to_minutes(period_data["Days"], period_data["Time"].split("-")[1]),
                        room=period_data["Room"],
                        distant=False,
                    ),
                )
            section_data = course_section.iloc(0)[0]
            sections.append(
                Section(
                    code=section_data["S/T"],
                    periods=periods,
                    instructors=section_data["Faculty"],
                ),
            )
        course_data = course.iloc(0)[0]
        courses.append(
            Course(
                school=course_data["School"],
                level=course_data["Level"],
                code=course_data["Course Abbr"],
                title=course_data["Course Title"],
                credits_us=course_data["Cr(US)"],
                credits_eu=course_data["Cr(ECTS)"],
                start_date=datetime.strptime(course_data["Start date"], "%d-%b-%y").replace(tzinfo=UTC),
                end_date=datetime.strptime(course_data["End date"], "%d-%b-%y").replace(tzinfo=UTC),
                enrolled=course_data["Enr"],
                capacity=course_data["Cap"],
                sections=sections,
            ),
        )
    if return_as == "list":
        return courses
    return to_json(courses).decode("utf-8")
