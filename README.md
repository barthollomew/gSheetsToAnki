# gSheetsToAnki

Import cards from Google Sheets straight into Anki via AnkiConnect. It creates decks on the fly, validates rows, lets you map sheet columns to Anki fields, and supports dry runs plus tagging.

## Setup
- Install Python 3.10+ and Anki with the AnkiConnect add-on running (default port 8765).
- Create a Google service account and download its credentials JSON. Share your sheet with that service account email.
- Install deps: `pip install -r requirements.txt`

## Usage
```sh
python main.py \
  --credentials credentials.json \
  --sheet-name "Biology 101" \
  --worksheet Cards \
  --deck-name "Bio::Vocab" \
  --front-column Term \
  --back-column Definition \
  --tag biology --tag vocab
```

You can also pass `--spreadsheet-id <ID>` instead of `--sheet-name` and point to a different AnkiConnect host with `--anki-url`.

### Handy flags
- `--worksheet`: pick a tab (defaults to the first).
- `--front-column` / `--back-column`: sheet headers to use; `--front-field-name` / `--back-field-name` map to custom Anki models.
- `--model-name`: pick a note type; `--tag` is repeatable.
- `--limit`: only import the first N rows.
- `--dry-run`: preview without writing to Anki.

The importer filters empty rows, asks AnkiConnect if notes are valid before sending, and shows a progress bar while adding cards.
