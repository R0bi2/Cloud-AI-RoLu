"""Teil 4.5: Kennungen wörtlich suchen, andere Fragen per RAG beantworten."""

import re
import sys
import time

import rag
from wissen import Treffer, antworten, dokumente, zeigen


def abrufen(frage: str) -> tuple[list[Treffer], float]:
    start = time.perf_counter()
    kennungen = re.findall(r"\b(?:[A-Z]-\d{3}|PA-\d{2})\b", frage, re.IGNORECASE)
    muster = [rf"(?<!\w){re.escape(k)}(?!\w)" for k in kennungen]
    for nummer in re.findall(r"(?:§|Paragraph|Paragraf)\s*(\d+)", frage, re.IGNORECASE):
        muster.append(rf"§\s*{nummer}(?!\d)")

    if muster:
        treffer = [
            Treffer(datei, text)
            for datei, text in dokumente().items()
            if any(re.search(m, text, re.IGNORECASE) for m in muster)
        ]
        if treffer:
            return treffer[:3], time.perf_counter() - start

    treffer, _ = rag.abrufen(frage)
    return treffer, time.perf_counter() - start


if __name__ == "__main__":
    frage = " ".join(sys.argv[1:])
    treffer, sekunden = abrufen(frage)
    zeigen(antworten(frage, treffer, sekunden))
