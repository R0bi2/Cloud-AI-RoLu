"""Ordnet Studierenden-Mails ein und prüft die strukturierte Antwort."""

import json
import sys
from typing import Literal

from pydantic import BaseModel, ValidationError

from llm import MODEL, client

SYSTEM_PROMPT = (
    "Du ordnest Mails von Studierenden an die HTWG Konstanz ein. "
    "Antworte ausschließlich mit JSON. "
    "anliegen ist pruefung, mensa, bibliothek oder sonstiges. "
    "studiengang ist das Kürzel (z. B. AIN, WIN, MSI) oder null. "
    "frist ist die Frist aus der Mail, so wie sie dort steht, oder null."
)


class Anfrage(BaseModel):
    anliegen: Literal["pruefung", "mensa", "bibliothek", "sonstiges"]
    studiengang: str | None
    frist: str | None


def schema_von(modell: type[BaseModel]) -> dict:
    """Verpackt das JSON-Schema für response_format."""
    return {
        "type": "json_schema",
        "json_schema": {
            "name": modell.__name__.lower(),
            "schema": modell.model_json_schema(),
        },
    }


def einordnen(mail: str) -> Anfrage:
    for versuch in range(1, 4):
        antwort = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": mail},
            ],
            # Für die Einordnung wollen wir wenig Streuung statt Kreativität.
            temperature=0,
            response_format=schema_von(Anfrage),
        )
        try:
            return Anfrage.model_validate_json(antwort.choices[0].message.content or "")
        except ValidationError as fehler:
            print(f"Ungültige Antwort (Versuch {versuch}/3): {fehler}")
    raise RuntimeError("Nach drei Versuchen keine gültige Einordnung erhalten.")


def auswerten() -> None:
    with open("mails.json", encoding="utf-8") as datei:
        faelle = json.load(datei)
    richtig = 0
    for fall in faelle:
        ergebnis = einordnen(fall["mail"])
        stimmt = ergebnis.anliegen == fall["erwartet"]["anliegen"]
        richtig += int(stimmt)
        print(f"\n{fall['mail']}")
        print(ergebnis.model_dump_json(indent=2))
        print("Richtig" if stimmt else "Falsch")
    print(f"\n{richtig} von {len(faelle)} Anliegen richtig ({MODEL})")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(einordnen(" ".join(sys.argv[1:])).model_dump_json(indent=2))
    else:
        auswerten()