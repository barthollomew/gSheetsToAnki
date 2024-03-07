import gspread
import json
import requests
import argparse

def authenticate_google_sheets(credentials_file):
    """Authenticate with Google Sheets"""
    try:
        gc = gspread.service_account(filename=credentials_file)
        return gc
    except Exception as e:
        print(f"Error authenticating with Google Sheets: {e}")
        return None

def open_sheet(gc, sheet_name):
    """Open the Google Sheets."""
    try:
        sheet = gc.open(sheet_name).sheet1
        return sheet
    except Exception as e:
        print(f"Error opening the Google Sheets file: {e}")
        return None

def create_anki_flashcard(front, back, deck_name):
    """Create flashcard."""
    note = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": []
            }
        }
    }
    return note

def send_to_anki(note):
    """Send the flashcard to Anki using AnkiConnect."""
    try:
        response = requests.post('http://localhost:8765', json.dumps(note))
        return response.json()
    except Exception as e:
        print(f"Error sending flashcard to Anki: {e}")
        return None

def main(args):
    # Authenticate and open file
    gc = authenticate_google_sheets(args.credentials)
    if not gc:
        return
    sheet = open_sheet(gc, args.sheet_name)
    if not sheet:
        return

    # Loop through each row and create a flashcard
    for i, row in enumerate(sheet.get_all_records(), start=1):
        front = row['Front']
        back = row['Back']
        note = create_anki_flashcard(front, back, args.deck_name)

        # Send the note to Anki using AnkiConnect
        response = send_to_anki(note)
        if response:
            print(f"Flashcard {i} created successfully.")
        else:
            print(f"Failed to create flashcard {i}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import flashcards from Google Sheets into Anki')
    parser.add_argument('--credentials', type=str, required=True, help='Path to the Google Sheets API credentials file')
    parser.add_argument('--sheet-name', type=str, required=True, help='Name of the Google Sheets file')
    parser.add_argument('--deck-name', type=str, required=True, help='Name of the Anki deck to add the flashcards to')
    args = parser.parse_args()
    main(args)
