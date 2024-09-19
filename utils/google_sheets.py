import gspread
import logging

def authenticate_google_sheets(credentials_file):
    """
    Authenticate with Google Sheets using the provided credentials file.

    Args:
        credentials_file (str): Path to the Google Sheets API credentials file.

    Returns:
        gspread.Client: Authenticated Google Sheets client object.
    """
    try:
        gc = gspread.service_account(filename=credentials_file)
        return gc
    except Exception as e:
        logging.error(f"Error authenticating with Google Sheets: {e}")
        return None

def open_sheet(gc, sheet_name):
    """
    Open the specified Google Sheets file.

    Args:
        gc (gspread.Client): Authenticated Google Sheets client object.
        sheet_name (str): Name of the Google Sheets file.

    Returns:
        gspread.models.Spreadsheet: Google Sheets worksheet object.
    """
    try:
        sheet = gc.open(sheet_name).sheet1
        return sheet
    except Exception as e:
        logging.error(f"Error opening the Google Sheets file: {e}")
        return None
