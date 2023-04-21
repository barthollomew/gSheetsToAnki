import gspread
import json
import requests

# Authenticate with Google Sheets
gc = gspread.service_account(filename='credentials.json')

# Open the Google Sheets file
sheet = gc.open('Flashcards').sheet1

# Loop through each row and create a flashcard
for row in sheet.get_all_records():
    # Get the values from the Google Sheets file
    front = row['Front']
    back = row['Back']

    # Create the Anki note
    note = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "My Deck",
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": []
            }
        }
    }

    # Send the note to Anki using AnkiConnect
    response = requests.post('http://localhost:8765', json.dumps(note))

    print(response.json())
