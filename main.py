import argparse
import logging
from tqdm import tqdm

from utils.google_sheets import authenticate_google_sheets, open_sheet
from utils.anki import create_anki_flashcard, send_to_anki
from utils.helpers import validate_args

def main(args):
    """
    Main function to handle the import of flashcards from Google Sheets to Anki.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
    """
    logging.basicConfig(level=logging.INFO)
    
    if not validate_args(args):
        return

    gc = authenticate_google_sheets(args.credentials)
    if not gc:
        return
    
    sheet = open_sheet(gc, args.sheet_name)
    if not sheet:
        return

    records = sheet.get_all_records()
    if not records:
        logging.info("No records found in the Google Sheet.")
        return

    logging.info(f"Starting to create flashcards in deck '{args.deck_name}'...")

    for i, row in enumerate(tqdm(records, desc="Creating flashcards", unit="card"), start=1):
        front = row.get('Front')
        back = row.get('Back')

        if not front or not back:
            logging.warning(f"Skipping row {i} due to missing 'Front' or 'Back' fields.")
            continue

        note = create_anki_flashcard(front, back, args.deck_name)
        response = send_to_anki(note)

        if response and response.get('error') is None:
            logging.info(f"Flashcard {i} created successfully.")
        else:
            logging.error(f"Failed to create flashcard {i}. Error: {response.get('error')}")

    logging.info("Flashcard creation process completed.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import flashcards from Google Sheets into Anki')
    parser.add_argument('--credentials', type=str, required=True, help='Path to the Google Sheets API credentials file')
    parser.add_argument('--sheet-name', type=str, required=True, help='Name of the Google Sheets file')
    parser.add_argument('--deck-name', type=str, required=True, help='Name of the Anki deck to add the flashcards to')
    args = parser.parse_args()
    main(args)
