import argparse
import logging
from typing import List, Tuple

from tqdm import tqdm

from utils.anki import AnkiClient
from utils.google_sheets import authenticate_google_sheets, fetch_records, open_worksheet
from utils.helpers import get_value_by_header, normalize_header, normalize_tags, validate_args


def _build_notes(records: List[dict], args, client: AnkiClient) -> Tuple[List[dict], int]:
    """
    Turn Google Sheets rows into Anki notes.
    """
    tags = normalize_tags(args.tags)
    notes: List[dict] = []
    skipped_rows = 0

    for row_index, row in enumerate(records, start=2):  # header row is row 1
        front = get_value_by_header(row, args.front_column)
        back = get_value_by_header(row, args.back_column)

        if not front or not back:
            logging.warning(
                "Skipping row %s due to missing values in '%s' or '%s'.",
                row_index,
                args.front_column,
                args.back_column,
            )
            skipped_rows += 1
            continue

        note = client.build_note(
            front=front,
            back=back,
            deck_name=args.deck_name,
            model_name=args.model_name,
            tags=tags,
            front_field=args.front_field_name,
            back_field=args.back_field_name,
        )
        notes.append(note)

    return notes, skipped_rows


def _preview_notes(notes: List[dict], args) -> None:
    sample = notes[: min(3, len(notes))]
    for idx, note in enumerate(sample, start=1):
        front_value = note["fields"].get(args.front_field_name)
        back_value = note["fields"].get(args.back_field_name)
        logging.info("Card %s preview: %s -> %s", idx, front_value, back_value)


def _import_notes(client: AnkiClient, notes: List[dict]) -> Tuple[int, int]:
    batch_size = 50
    added = 0
    failed = 0

    with tqdm(total=len(notes), desc="Creating flashcards", unit="card") as progress:
        for start in range(0, len(notes), batch_size):
            batch = notes[start : start + batch_size]
            result = client.add_notes(batch)
            if result is None:
                failed += len(batch)
            else:
                successful = sum(1 for note_id in result if note_id)
                added += successful
                failed += len(batch) - successful
            progress.update(len(batch))

    return added, failed


def main(args) -> None:
    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format="%(levelname)s: %(message)s")

    if not validate_args(args):
        return

    sheets_client = authenticate_google_sheets(args.credentials)
    if not sheets_client:
        return

    worksheet = open_worksheet(sheets_client, args.sheet_name, args.spreadsheet_id, args.worksheet)
    if not worksheet:
        return

    records = fetch_records(worksheet, limit=args.limit)
    if not records:
        logging.warning("No records found in the Google Sheet.")
        return

    header_sample = records[0].keys()
    normalized_headers = {normalize_header(header) for header in header_sample}
    missing_columns = []
    for column in (args.front_column, args.back_column):
        if normalize_header(column) not in normalized_headers:
            missing_columns.append(column)
    if missing_columns:
        logging.warning(
            "Columns %s were not found in the sheet headers (%s). Rows missing these columns will be skipped.",
            ", ".join(missing_columns),
            ", ".join(header_sample),
        )

    anki = AnkiClient(base_url=args.anki_url)
    if not anki.is_available():
        return
    if not anki.ensure_deck(args.deck_name):
        return

    notes, skipped_rows = _build_notes(records, args, anki)

    if not notes:
        logging.error("No notes were built from the sheet; nothing to import.")
        return

    logging.info("Prepared %s note(s) for deck '%s'.", len(notes), args.deck_name)
    if args.dry_run:
        logging.info("Dry-run enabled: nothing will be sent to Anki.")
        _preview_notes(notes, args)
        return

    can_add = anki.can_add_notes(notes)
    if can_add is None:
        logging.error("AnkiConnect could not validate whether the notes can be added.")
        return

    valid_notes = [note for note, ok in zip(notes, can_add) if ok]
    rejected = len(notes) - len(valid_notes)
    if rejected:
        logging.warning("Skipping %s note(s) rejected by Anki (duplicates or invalid fields).", rejected)

    if not valid_notes:
        logging.error("No notes accepted by Anki after validation.")
        return

    added, failed = _import_notes(anki, valid_notes)
    logging.info(
        "Import finished. Added %s note(s) to '%s'. Skipped %s empty rows. Rejected %s. Failed to add %s.",
        added,
        args.deck_name,
        skipped_rows,
        rejected,
        failed,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import flashcards from Google Sheets into Anki")
    parser.add_argument("--credentials", type=str, required=True, help="Path to the Google Sheets API credentials file")

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--sheet-name", type=str, help="Name of the Google Sheets file")
    source.add_argument("--spreadsheet-id", type=str, help="Spreadsheet ID from the Google Sheets URL")

    parser.add_argument("--worksheet", type=str, help="Worksheet/tab name (defaults to the first tab)")
    parser.add_argument("--deck-name", type=str, required=True, help="Name of the Anki deck to add the flashcards to")
    parser.add_argument("--model-name", type=str, default="Basic", help="Anki note type / model name")
    parser.add_argument("--front-field-name", type=str, default="Front", help="Anki field name for the card front")
    parser.add_argument("--back-field-name", type=str, default="Back", help="Anki field name for the card back")

    parser.add_argument("--front-column", type=str, default="Front", help="Sheet column header for the card front")
    parser.add_argument("--back-column", type=str, default="Back", help="Sheet column header for the card back")
    parser.add_argument(
        "--tag",
        dest="tags",
        action="append",
        help="Tag to attach to each note (use multiple --tag flags for more than one tag)",
    )
    parser.add_argument("--limit", type=int, help="Only import the first N rows from the sheet")
    parser.add_argument("--dry-run", action="store_true", help="Preview notes without sending them to Anki")
    parser.add_argument("--anki-url", type=str, default="http://localhost:8765", help="AnkiConnect base URL")
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Log verbosity",
    )
    args = parser.parse_args()
    main(args)
