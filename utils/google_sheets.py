import logging
from typing import List, Optional

import gspread


def authenticate_google_sheets(credentials_file: str) -> Optional[gspread.Client]:
    """
    Authenticate with Google Sheets using the provided credentials file.
    """
    try:
        return gspread.service_account(filename=credentials_file)
    except Exception as exc:
        logging.error("Error authenticating with Google Sheets: %s", exc)
        return None


def open_worksheet(
    client: gspread.Client,
    spreadsheet_name: Optional[str],
    spreadsheet_id: Optional[str],
    worksheet_name: Optional[str],
):
    """
    Open a worksheet by name or ID. Defaults to the first worksheet.
    """
    try:
        if spreadsheet_id:
            spreadsheet = client.open_by_key(spreadsheet_id)
        else:
            spreadsheet = client.open(spreadsheet_name)

        if worksheet_name:
            return spreadsheet.worksheet(worksheet_name)
        return spreadsheet.sheet1
    except gspread.SpreadsheetNotFound:
        logging.error("Spreadsheet not found. Double-check the name or ID.")
        return None
    except gspread.WorksheetNotFound:
        logging.error("Worksheet '%s' was not found in the spreadsheet.", worksheet_name)
        return None
    except Exception as exc:
        logging.error("Error opening worksheet: %s", exc)
        return None


def fetch_records(worksheet, limit: Optional[int] = None) -> List[dict]:
    """
    Retrieve rows as dictionaries keyed by header row.
    """
    try:
        records = worksheet.get_all_records()
    except Exception as exc:
        logging.error("Failed to read data from the worksheet: %s", exc)
        return []

    filtered = [row for row in records if any(str(value).strip() for value in row.values())]
    if limit is not None:
        return filtered[:limit]
    return filtered
