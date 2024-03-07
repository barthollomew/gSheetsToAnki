# Bulk import flashcards from Google Sheets into Anki

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

## How to Use

1. Clone the repository or download the script file.
2. Install the required Python libraries using `pip install gspread requests`.
3. Obtain a service account JSON file for authentication with Google Sheets and save it to a secure location.
4. Open a terminal or command prompt and navigate to the directory where the script is located.

6. Run the script using the following command:

`python import_gsheets_to_anki.py --credentials path/to/credentials.json --sheet-name "Sheet Name" --deck-name "Deck Name"`

6. Replace `path/to/credentials.json` with the path to your Google Sheets API credentials file, `"Sheet Name"` with the name of your Google Sheets file, and `"Deck Name"` with the name of the Anki deck you want to add the flashcards to.
7. The script will read the flashcards from the specified Google Sheets file and import them into the specified Anki deck. It will display a progress message for each flashcard created.

## How it works

The script uses the `gspread` library to read the Google Sheets file, and the `anki-connect` library to create the Anki flashcards. It loops through each row in the sheet, extracts the values from the 'Front' and 'Back' columns, and creates an Anki note using the AnkiConnect API. The note is then sent to Anki using the `requests` library, which communicates with AnkiConnect running on the default port 8765.

## Resources

- [Anki](https://apps.ankiweb.net/)
- [AnkiConnect Add-on](https://ankiweb.net/shared/info/2055492159)
- [gspread Documentation](https://gspread.readthedocs.io/en/latest/)
- [Google Cloud Platform](https://cloud.google.com/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
