# Wrapper for PDF scrapers

import pdfscraper.csbs as csbs


def get_csbs_as_json_columns(semester_code, academic_level_code=None, school_code=None, request_timeout=None,
                             verify_params=None, verification_timeout=None):
    dataframe = csbs.get_dataframe(
        semester_code=semester_code,
        academic_level_code=academic_level_code,
        school_code=school_code,
        req_timeout=request_timeout,
        verify_params=verify_params,
        verification_timeout=verification_timeout
    )
    if dataframe is not None:
        return dataframe.to_json()
    return None


def get_csbs_as_json_table(semester_code, academic_level_code=None, school_code=None, request_timeout=None,
                           verify_params=None, verification_timeout=None):
    dataframe = csbs.get_dataframe(
        semester_code=semester_code,
        academic_level_code=academic_level_code,
        school_code=school_code,
        req_timeout=request_timeout,
        verify_params=verify_params,
        verification_timeout=verification_timeout
    )
    if dataframe is not None:
        return dataframe.to_json(orient='table', index=False)
    return None
