from datetime import datetime

from edgar._companies import EntityFilings, EntityFiling

def filter_filings(filings: EntityFilings, form: str, year: int) -> EntityFiling:
    """
    Filter filings by form and year.

    :param filings: List of EntityFilings.
    :param form: The form to filter by.
    :param year: The year to filter by.
    :return: The filtered EntityFiling.
    """
    for filing in filings:
        report_date_str = filing.report_date
        if not report_date_str:  # Check if report_date_str is empty
            continue  # Skip this filing if the report date is empty
        report_date = datetime.strptime(report_date_str, "%Y-%m-%d")
        if filing.form == form and report_date.year == year:
            return filing

    raise ValueError(f"No {form} filing found for the year {year}.")
