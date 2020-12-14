# Wrapper for PDF scrapers

import pdfscraper.csbs as csbs


def get_csbs_as_json_columns(semester_code=None, academic_level_code=None, school_code=None, timeout=None):
    dataframe = csbs.get_dataframe(semester_code, academic_level_code, school_code, timeout)
    if dataframe is not None:
        return dataframe.to_json()
    return None


def get_csbs_as_json_table(semester_code=None, academic_level_code=None, school_code=None, timeout=None):
    dataframe = csbs.get_dataframe(semester_code, academic_level_code, school_code, timeout)
    if dataframe is not None:
        return dataframe.to_json(orient='table', index=False)
    return None
