import logging
from typing import List, Optional

import requests


class AnkiClient:
    """
    Tiny helper around the AnkiConnect API.
    """

    def __init__(self, base_url: str = "http://localhost:8765", timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, action: str, **params) -> Optional[dict]:
        payload = {"action": action, "version": 6, "params": params}
        try:
            response = self.session.post(self.base_url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as exc:
            logging.error("Could not reach AnkiConnect at %s: %s", self.base_url, exc)
            return None
        except ValueError:
            logging.error("AnkiConnect returned a non-JSON response.")
            return None

        if data.get("error"):
            logging.error("AnkiConnect error on '%s': %s", action, data["error"])
            return None
        return data.get("result")

    def is_available(self) -> bool:
        version = self._request("version")
        if version is None:
            logging.error(
                "AnkiConnect does not seem to be running. Please start Anki with the AnkiConnect add-on enabled."
            )
            return False
        logging.debug("Connected to AnkiConnect version %s", version)
        return True

    def ensure_deck(self, deck_name: str) -> bool:
        decks = self._request("deckNames")
        if decks is None:
            return False

        if deck_name in decks:
            return True

        created = self._request("createDeck", deck=deck_name)
        if created is None:
            logging.error("Could not create deck '%s'.", deck_name)
            return False

        logging.info("Created deck '%s'.", deck_name)
        return True

    def build_note(
        self,
        front: str,
        back: str,
        deck_name: str,
        model_name: str,
        tags: Optional[List[str]],
        front_field: str = "Front",
        back_field: str = "Back",
    ) -> dict:
        return {
            "deckName": deck_name,
            "modelName": model_name,
            "fields": {
                front_field: str(front),
                back_field: str(back),
            },
            "tags": tags or [],
        }

    def can_add_notes(self, notes: List[dict]) -> Optional[List[bool]]:
        return self._request("canAddNotes", notes=notes)

    def add_notes(self, notes: List[dict]) -> Optional[List[int]]:
        return self._request("addNotes", notes=notes)
