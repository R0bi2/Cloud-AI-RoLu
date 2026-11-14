# Cloud-AI-RoLu – Übung 3 / P3

**Ein Agent mit Werkzeugen · Cloud-native AI · WS 2026/27**

Weitere Dokumentation: [Übung 1](uebung_1.md) · [Übung 2](uebung_2.md) · [Aufgabenblatt Übung 3](Uebung_3_Starter/uebung_3.md) · [Bisherige Notizen und Testausgaben](Uebung_3_Starter/Readme)

Namen und Matrikelnummern werden wegen des öffentlichen Repositorys nur im Abgabetext in Moodle angegeben.

Diese README ist als Vorlage vorbereitet. Antworten und Messtabellen sind noch offen.
Die bisherigen Ergebnisse stehen in den verlinkten Notizen und werden vor dem Übernehmen geprüft.

## Start

Docker Desktop muss laufen. Für die Ersteinrichtung im Hauptordner ausführen:

```powershell
cd Uebung_3_Starter/starter
cp .env.example .env
```

Falls das gemeinsame Modell-Volume aus Übung 2 noch nicht existiert:

```powershell
docker volume create cnai-ollama-modelle
```

Die lokale `.env` enthält für die Messungen:

```dotenv
LLM_BASE_URL=http://ollama:11434/v1
LLM_MODEL=llama3.2:3b
LLM_API_KEY=nicht-noetig
MCP_URL=http://campus-mcp:8000/mcp
HEUTE=2026-11-03
```

Die `.env` bleibt lokal. `HEUTE` legt das Datum für vergleichbare Tests fest.
Alle folgenden Docker-Befehle laufen im Ordner `Uebung_3_Starter/starter`.

```powershell
docker compose run --rm --build app werkzeuge.py
docker compose run --rm app mcp_werkzeuge.py
```

Der erste Start baut die Images und lädt `llama3.2:3b` und `qwen2.5:3b`.
Ollama stellt das Modell bereit. Der eigene MCP-Server liefert die Werkzeuge
für Raumbelegung und Mensa. Die Modelle bleiben im gemeinsamen Volume gespeichert.

## Teil 1 · Die Agent-Schleife

### 1.1 Agent-Schleife umsetzen und mit drei Fragen testen

Lest `app/werkzeuge.py` und den oberen Teil von `app/agent.py`.
Setzt TODO 1 in `agent.py` um: Das Modell wählt Werkzeuge, bekommt deren
Ergebnisse zurück und arbeitet weiter, bis es antwortet oder das Schrittlimit erreicht.

Beschreibt für jede Frage den Ablauf: Welche Werkzeuge werden mit welchen
Argumenten aufgerufen? Was liefern sie zurück, und stimmt die abschließende Antwort?

```powershell
docker compose run --rm app agent.py "Was gibt es heute in der Mensa?"
docker compose run --rm app agent.py "Ich bin am Tag meiner Klausur krank. Was muss ich tun?"
docker compose run --rm app agent.py "Ist O-108 am Donnerstag um 14 Uhr frei?"
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

| Frage | Werkzeuge und Argumente in Reihenfolge | Werkzeugergebnis und Antwort | Stimmt die Antwort? Warum? |
|---|---|---|---|
| Mensa heute | offen | offen | offen |
| Krank am Klausurtag | offen | offen | offen |
| O-108 am Donnerstag um 14 Uhr | offen | offen | offen |

</div>

### 1.2 Welche Fehlermodi nach Huyen sehen wir?

Ordnet jeden beobachteten Fehler einem Fehlermodus aus dem Skript zu
(Abschnitt „Wie Agenten scheitern“). Begründet die Zuordnung kurz am jeweiligen Ablauf.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

| Frage oder Testfall | Beobachteter Fehler | Fehlermodus nach Huyen | Kurze Begründung |
|---|---|---|---|
| offen | offen | offen | offen |

</div>

### 1.3 Wie schneidet der Agent in der ersten Messung ab?

Messt den Ausgangsstand mit den 13 Aufgaben und übernehmt beide Tabellen.
Dass die Buchungsaufgabe vor Teil 2 noch scheitert, ist vorgesehen.

```powershell
docker compose run --rm app messen.py
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Messdatum, Modell und verwendeter Stand: offen.

| Variante | Antwort | Werkz. | ungültig | Fehler | Abbruch | Aufrufe Ø | Tokens Ø | Dauer Ø |
|---|---|---|---|---|---|---|---|---|
| agent.v1.yaml | offen | offen | offen | offen | offen | offen | offen | offen |

| Variante | datum | direkt | wissen | mehrschritt | schreibend | ohne | fehlt |
|---|---|---|---|---|---|---|---|
| agent.v1.yaml | offen | offen | offen | offen | offen | offen | offen |

</div>

„Antwort“ zählt Treffer der erwarteten Stichwörter. „Werkz.“ prüft, ob die
erwarteten Werkzeuge verwendet wurden. Beides ersetzt keine inhaltliche Prüfung.
„Aufrufe Ø“ zählt Werkzeugaufrufe; „Tokens Ø“ die summierten Eingabe-Tokens pro Aufgabe.
„ungültig“ zählt unbekannte Werkzeuge oder falsche Parameter, „Fehler“ die
Fehlerergebnisse und „Abbruch“ erreichte Schrittlimits.

### 1.4 Warum steigen die Eingabe-Tokens bei mehreren Modellaufrufen?

Schaut euch eine Aufgabe mit mehreren Schritten an. Notiert den Ablauf und
die verfügbaren Tokenwerte. Warum wächst der Kontext, obwohl die Frage gleich bleibt?
Die normale Abschlussausgabe zeigt die Summe über alle Modellaufrufe.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Testfrage, Ablauf, Tokenwerte und Erklärung: offen.

</div>

### 1.5 Was passiert mit einem Schrittlimit von 1, und warum brauchen wir ein Limit?

Verwendet `--max-schritte 1` bei einer Frage, für die der Agent mindestens
zwei Werkzeuge braucht. Beschreibt das Ergebnis und erklärt, warum das Limit trotzdem nötig ist.

```powershell
docker compose run --rm app agent.py "Was gibt es heute in der Mensa?" --max-schritte 1
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Beobachteter Ablauf, Abbruch und Begründung: offen.

</div>

## Teil 2 · Eigene Werkzeuge, lokal und als MCP-Server

### 2.1 Ein lokales Werkzeug: Wie viele Tage bleiben bis zur Prüfungsanmeldung?

Setzt TODO 2 in `app/werkzeuge.py` um: `tage_bis(datum)` berechnet die Tage
vom heutigen Datum bis zum Zieldatum. Beachtet den festen Wert aus `HEUTE`.
Vergangene und ungültige Daten sollen verständliche Meldungen liefern.
Tragt das Werkzeug mit Beschreibung und JSON-Schema in `LOKALE_WERKZEUGE` ein.

```powershell
docker compose run --rm app agent.py "Wie viele Tage habe ich noch, bis die Prüfungsanmeldung endet?"
```

Holt sich der Agent das heutige Datum, die Frist aus der Wissensbasis und die
Berechnung? Beschreibt die Reihenfolge und prüft die Antwort.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Werkzeugaufrufe mit Argumenten, Ergebnis und Bewertung: offen.

</div>

### 2.2 Ein Werkzeug im MCP-Server: Einen Raum buchen

Setzt TODO 3a in `campus_mcp/server.py` um:
`raum_buchen(raum, datum, uhrzeit, name)` soll einen Raum buchen.
Der Docstring beschreibt dem Modell das Werkzeug. Die Buchung läuft im MCP-Server.

Startet den Server nach Änderungen neu und prüft die angebotenen Werkzeuge:

```powershell
docker compose restart campus-mcp
docker compose run --rm app mcp_werkzeuge.py
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Angezeigte Beschreibung von `raum_buchen` und Ergebnis des Werkzeugtests: offen.

</div>

### 2.3 Schreibaktionen bestätigen

Setzt TODO 3b in `app/agent.py` um. Schreibende Werkzeuge dürfen erst nach
einer Bestätigung im Terminal ausgeführt werden.

#### 1. Was passiert bei Zustimmung und bei Ablehnung?

Testet einmal mit `j` und einmal mit `n`. Beschreibt besonders, wie das Modell
nach einer Ablehnung weiterarbeitet und ob es die Buchung tatsächlich unterlässt.

```powershell
docker compose run --rm app agent.py "Buche mir O-108 am Freitag um 9:45 Uhr für die Lerngruppe Kim."
```

Für vergleichbare Tests kann `docker compose restart campus-mcp` die bisherigen
Buchungen löschen. Sie liegen nur im Arbeitsspeicher des Servers.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

| Bestätigung | Werkzeugaufrufe und Ergebnis | Abschließende Antwort und Bewertung |
|---|---|---|
| `j` | offen | offen |
| `n` | offen | offen |

</div>

#### 2. Wie wird ein schreibendes Werkzeug erkannt, und was ist daran schwach?

Schaut in `mcp_werkzeuge.py`: Woran wird eine Schreibaktion erkannt?
Warum ist diese Lösung schwach, und wo sollte die Information eigentlich herkommen?
Bezieht MCP Tool Annotations in die Antwort ein.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Antwort: offen.

</div>

#### 3. Optional: Werkzeuge ohne Modell im MCP Inspector aufrufen

Startet auf dem Rechner `npx @modelcontextprotocol/inspector`.
Wählt den Transport **Streamable HTTP** und die URL `http://localhost:8000/mcp`.
Alternativ kann der Server in Claude Desktop oder Cursor eingebunden werden.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Durchgeführt oder ausgelassen; bei Durchführung getestete Werkzeuge und Ergebnis: offen.

</div>

## Teil 3 · Verbessern und messen

Probiert mindestens zwei der folgenden Ansätze aus und messt jeden einzeln
gegen den fertigen Stand aus Teil 2:

- **Prompt:** `prompts/agent.v2.yaml` mit klaren Werkzeugregeln und ein bis zwei Beispielabläufen schreiben. `agent.v1.yaml` bleibt unverändert.
- **Werkzeug:** `raum_frei`, `raum_buchen` und `mensa_speiseplan` fehlertoleranter machen. Das Datum darf auch `heute`, `morgen` oder ein Wochentag sein; angehängte Uhrzeiten werden ignoriert. Die Beschreibungen anpassen.
- **Workflow:** Den festen Routing-Workflow aus `workflow.py` mit dem Agenten vergleichen.

### 3.1 Welcher Ansatz bringt bei welchem Aufgabentyp am meisten?

Übernehmt für beide Modelle die Gesamttabelle und die Ergebnisse nach Aufgabentyp.
Notiert pro Messstand, was geändert wurde. Falls ihr die Werkzeuge verbessert,
messt diesen Stand separat, damit seine Wirkung erkennbar bleibt.

Die folgenden Befehle setzen voraus, dass `agent.v2.yaml` angelegt wurde:

```powershell
docker compose run --rm -e LLM_MODEL=llama3.2:3b app messen.py prompts/agent.v1.yaml prompts/agent.v2.yaml workflow
docker compose run --rm -e LLM_MODEL=qwen2.5:3b app messen.py prompts/agent.v1.yaml prompts/agent.v2.yaml workflow
```

Schreibaktionen werden von `messen.py` automatisch bestätigt. Die interaktive
Bestätigung wird deshalb zusätzlich in Teil 2.3 geprüft.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Gewählte Ansätze, Messdatum und Änderungen je Messstand: offen.

**Gesamtergebnisse** – je Modell und Messstand ausfüllen:

| Modell | Messstand / Variante | Antwort | Werkz. | ungültig | Fehler | Abbruch | Aufrufe Ø | Tokens Ø | Dauer Ø |
|---|---|---|---|---|---|---|---|---|---|
| llama3.2:3b | offen | offen | offen | offen | offen | offen | offen | offen | offen |
| qwen2.5:3b | offen | offen | offen | offen | offen | offen | offen | offen | offen |

**Richtige Antworten nach Typ** – je Modell und Messstand ausfüllen:

| Modell | Messstand / Variante | datum | direkt | wissen | mehrschritt | schreibend | ohne | fehlt |
|---|---|---|---|---|---|---|---|---|
| llama3.2:3b | offen | offen | offen | offen | offen | offen | offen | offen |
| qwen2.5:3b | offen | offen | offen | offen | offen | offen | offen | offen |

Kurze Auswertung je Aufgabentyp; auffällige Schwankungen bei Wiederholungen: offen.

</div>

### 3.2 Bei welchen Aufgaben gewinnt der Workflow, bei welchen der Agent?

Begründet den Unterschied anhand eurer Ergebnisse und des Ablaufs:
feste Pfade beim Workflow und eine Werkzeugschleife beim Agenten.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Antwort mit Beispielen aus der Messung: offen.

</div>

### 3.3 Welches Modell würden wir für den Agenten und welches für den Workflow nehmen?

Begründet die Auswahl mit euren Zahlen zu Antwortqualität, Tokens und Dauer.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Auswahl und Begründung: offen.

</div>

### 3.4 Mit Academic-Cloud-Zugang: Was verändert ein größeres Modell?

Messt `qwen3-30b-a3b-instruct-2507` mit `agent.v1`, falls ihr Zugang habt.
Was ändert sich an den beobachteten Fehlermodi? Zugangsdaten bleiben lokal.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Durchgeführt oder mangels Zugang ausgelassen; Messwerte und Vergleich: offen.

</div>

## Teil 4 und 5 · Ergänzung aus VL 6

Das vorhandene Aufgabenblatt kündigt Orchestrierung mit einem Framework,
Memory, ein kleines Multi-Agent-Setup und weitere README-Anforderungen an.
Die konkreten Aufgaben werden nachgetragen, sobald die Ergänzung vorliegt.

## Zusatz · ReAct ohne Function Calling

Laut Aufgabenblatt entfällt der Zusatz bei mindestens 80 % nachgewiesener
Anwesenheit am Semesterende. Wer nicht sicher ist, gibt ihn mit ab;
Zusatzteile sind nicht nachreichbar.

### Z.1 Eine ReAct-Schleife mit Textausgabe umsetzen

Schreibt `react.py`. Beschreibt die Werkzeuge im System-Prompt und verlangt
das Format `Thought: … Action: werkzeug({"param": "wert"})` oder `Final Answer: …`.
Lest die Aktion mit einem regulären Ausdruck aus, führt sie aus und hängt das
Ergebnis als `Observation: …` an.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Entfällt mit Nachweis oder Umsetzung und Testablauf: offen.

</div>

### Z.2 ReAct mit denselben Aufgaben gegen den Agenten messen

Ergänzt in `messen.py` eine Variante `react` und messt beide Ansätze mit denselben Aufgaben.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Messtabellen je Modell: offen.

</div>

### Z.3 Was ist robuster, was ist billiger, und bei welchem Modell?

Vergleicht die Ergebnisse und beschreibt zwei Fehler, die nur bei der Textvariante auftreten.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Auswertung und zwei beobachtete Fehler: offen.

</div>

## Abgabe

In Moodle unter „Übung 3 (P3)“ werden der Repository-Link und der Commit-Hash
des Abgabestands angegeben. Die Frist für Termin A oder B steht in Moodle.
Das Repository muss öffentlich oder für den GitHub-Account `PascalLaube` freigegeben sein.

Vor der Abgabe prüfen:

- [ ] Die Startbefehle funktionieren mit der beschriebenen `.env`.
- [ ] Keine Secrets oder lokale `.env` sind eingecheckt.
- [ ] Die Abhängigkeiten sind gepinnt.
- [ ] TODO 1, 2, 3a und 3b sind umgesetzt; `messen.py` läuft durch.
- [ ] `raum_buchen` läuft im MCP-Server.
- [ ] Die drei Abläufe aus Teil 1 und die Messtabellen aus Teil 3 sind eingetragen und geprüft.
- [ ] Alle Antwortfelder sind ausgefüllt oder begründet als entfallen markiert.
- [ ] Die Ergänzungen aus VL 6 und die Entscheidung zum Zusatz sind berücksichtigt.
- [ ] Wir können unseren Code und die Werkzeugbeschreibungen erklären.

Bei Serverproblemen hilft `docker compose logs campus-mcp`.
