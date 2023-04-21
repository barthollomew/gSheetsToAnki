# Importing Flashcards from Google Sheets into Anki

This is a Python script that reads a Google Sheets file and imports the flashcards into Anki. It uses the `gspread` library to read the Google Sheets file and the `anki-connect` library to create the Anki flashcards.

## Prerequisites

Before you can run this script, you'll need to have the following:

- Anki installed on your computer
- AnkiConnect add-on installed in Anki (can be found in the Anki Add-ons Gallery)
- A Google Cloud Platform (GCP) project
- A service account JSON file for authentication with Google Sheets

You'll also need to install the following Python libraries:

- gspread
- requests

## How it works

The script uses the `gspread` library to read the Google Sheets file, and the `anki-connect` library to create the Anki flashcards. It loops through each row in the sheet, extracts the values from the 'Front' and 'Back' columns, and creates an Anki note using the AnkiConnect API. The note is then sent to Anki using the `requests` library, which communicates with AnkiConnect running on the default port 8765.

## Resources

- [Anki](https://apps.ankiweb.net/)
- [AnkiConnect Add-on](https://ankiweb.net/shared/info/2055492159)
- [gspread Documentation](https://gspread.readthedocs.io/en/latest/)
- [Google Cloud Platform](https://cloud.google.com/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.