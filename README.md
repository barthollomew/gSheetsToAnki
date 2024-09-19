## gSheetsToAnki


gSheetsToAnki is a dead simple Python program that imports flashcards from Google Sheets into Anki. Super useful for mass importing definitions and flashcards.

### Features

- **Google Sheets Integration**: Seamlessly authenticate and retrieve data from your Google Sheets.
- **Bulk Flashcard Creation**: Automatically generate multiple flashcards based on the content of your Google Sheets.
- **Customizable Decks**: Specify the Anki deck where your flashcards will be added, allowing for organized study sessions.
- **Error Handling & Logging**: Comprehensive error management and logging to ensure smooth operation and easy troubleshooting.
- **Progress Tracking**: Monitor the flashcard creation process with a handy progress bar.

### Setup

#### Preparing the Google Sheets API Credentials

1. Obtain your Google Sheets API credentials by following the instructions [here](https://developers.google.com/sheets/api/quickstart/python).
2. Save the credentials JSON file to your local machine.

#### Installing Dependencies

Navigate to the project directory and install the necessary dependencies:

```sh
pip install -r requirements.txt
```

#### Running the Tool

You can run the Google Sheets to Anki Flashcard Importer from the command line with the following command:

```sh
python main.py --credentials /path/to/credentials.json --sheet-name "Your Sheet Name" --deck-name "Your Anki Deck Name"
```

### Command-line Options

- `--credentials`: Path to the Google Sheets API credentials file.
- `--sheet-name`: Name of the Google Sheets file containing your flashcards.
- `--deck-name`: Name of the Anki deck where the flashcards will be added.

#### Example

```sh
python main.py --credentials /path/to/credentials.json --sheet-name "Biology 101" --deck-name "Biology Flashcards"
```

This command will import all flashcards from the "Biology 101" Google Sheets file into the "Biology Flashcards" deck in Anki.