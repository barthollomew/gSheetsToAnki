import requests
import logging

def create_anki_flashcard(front, back, deck_name):
    """
    Create a flashcard dictionary structure for Anki.

    Args:
        front (str): The front text of the flashcard.
        back (str): The back text of the flashcard.
        deck_name (str): The name of the Anki deck to add the flashcard to.

    Returns:
        dict: A dictionary representing the flashcard note in Anki's API format.
    """
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
    """
    Send the flashcard note to Anki using AnkiConnect.

    Args:
        note (dict): The flashcard note dictionary.

    Returns:
        dict: The response from the AnkiConnect API.
    """
    try:
        response = requests.post('http://localhost:8765', json=note)
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending flashcard to Anki: {e}")
        return None
