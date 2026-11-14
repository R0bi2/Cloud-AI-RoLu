# Cloud-AI-RoLu – Übung 3 / P3

**Ein Agent mit Werkzeugen · Cloud-native AI · WS 2026/27**

## Start

Docker Desktop muss laufen. Einmalig im Hauptordner:

```powershell
cd uebung_3/starter
cp .env.example .env
```

Falls das Modell-Volume aus Übung 2 fehlt:

```powershell
docker volume create cnai-ollama-modelle
```

Die lokale `.env`:

```dotenv
LLM_BASE_URL=http://ollama:11434/v1
LLM_MODEL=llama3.2:3b
LLM_API_KEY=nicht-noetig
MCP_URL=http://campus-mcp:8000/mcp
HEUTE=2026-11-03
```

Alle folgenden Befehle laufen in `uebung_3/starter`. `HEUTE` hält das Datum für die Messungen fest.

```powershell
docker compose run --rm --build app werkzeuge.py
docker compose run --rm app mcp_werkzeuge.py
```

Ollama stellt die Modelle bereit; der MCP-Server liefert Raumbelegung und Speiseplan.
Beim ersten Start werden `llama3.2:3b` und `qwen2.5:3b` geladen. Die `.env` bleibt lokal.

## Teil 1 · Die Agent-Schleife

### 1.1 Agent-Schleife umsetzen und drei Fragen testen

TODO 1 in `agent.py` umsetzen. Für jede Frage die Werkzeugaufrufe mit Argumenten und die Antwort bewerten.

```powershell
docker compose run --rm app agent.py "Was gibt es heute in der Mensa?"
docker compose run --rm app agent.py "Ich bin am Tag meiner Klausur krank. Was muss ich tun?"
docker compose run --rm app agent.py "Ist O-108 am Donnerstag um 14 Uhr frei?"
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Die Schleife ist umgesetzt. Test am 14.11.2026 mit `llama3.2:3b`, `agent.v1` und `HEUTE=2026-11-03`; `tage_bis` ist verfügbar. Messstand: vor dem Ergänzen der Raumbuchung aus Teil 2.

| Frage | Werkzeugaufrufe in Reihenfolge | Ergebnis und Bewertung |
|---|---|---|
| Mensa heute | `mensa_speiseplan(datum='heute')` | Datumsfehler. Der Agent meldet fehlende Information, statt den Wert zu korrigieren. Die Frage bleibt unbeantwortet. |
| Krank am Klausurtag | `heute()` → `raeume_auflisten()` → `mensa_speiseplan(datum='2026-11-05')` | Keine passende Wissenssuche. Die Antwort verweist allgemein auf einen Arzt und mögliche Alternativen; das Vorgehen bei Prüfungsunfähigkeit fehlt. |
| O-108 am Donnerstag, 14 Uhr | `raum_frei(raum='O-108', datum='2026-11-04')` | Mittwoch wird abgefragt, die Antwort nennt Donnerstag. „Nicht frei“ stimmt laut Belegungsdatei zufällig auch für Donnerstag; dort ist ein Tutorium. |

| Frage | Werkzeugaufrufe | Modellaufrufe | Eingabe-Tokens gesamt | Dauer |
|---|---:|---:|---:|---:|
| Mensa | 1 | 2 | 1044 | 26,2 s |
| Klausur | 3 | 2 | 1231 | 27,3 s |
| Raum | 1 | 2 | 1102 | 5,9 s |

</div>

### 1.2 Welche Fehlermodi nach Huyen sehen wir?

Die beobachteten Fehler den Fehlermodi aus der Vorlesung zuordnen.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

| Frage oder Testfall | Beobachteter Fehler | Fehlermodus nach Huyen |
|---|---|---|
| Mensa | `datum='heute'` statt eines Datums im Format `JJJJ-MM-TT`. | Falsche Werte |
| Klausur | Raumliste und Speiseplan statt der nötigen Wissenssuche; keine brauchbare Antwort. | Ziel verfehlt; Ineffizienz |
| Raum am Donnerstag | Mittwoch wird abgefragt und als Donnerstag ausgegeben. | Falsche Werte; Ziel verfehlt |
| Prüfungsfrist | `tage_bis` rechnet mit einem geratenen Zieldatum; die Frist wird nicht nachgeschlagen. | Falsche Werte; Ziel verfehlt |
| Kontext- und Limittest (1.4/1.5) | Suche mit `pruefungsanmeldung` findet den Umlauttext nicht; die Berechnung wird mit `datum='heute'` vor der Auswertung der Frist angefordert. | Falsche Werte; Ineffizienz; Ziel verfehlt |
| Buchung | Das benötigte Werkzeug `raum_buchen` fehlt. | Werkzeugfehler |
| Veganes Gericht am Freitag; Buchung | Donnerstag wird statt Freitag abgefragt. | Falsche Werte; Ziel verfehlt |
| Mensa am Samstag; Parken | `raum_frei` wird mit erfundenen Räumen `M-101` bzw. `P-123` aufgerufen. | Falsche Werte; Ziel verfehlt |
| Ersatz-Campuskarte | Nach erfolgloser Suche mit einem zu engen Begriff wird nicht weitergesucht. | Ziel verfehlt |
| F-201; Fachschaftsparty | Aus der Raumliste werden unbelegte Angaben zu Ansprechpartner bzw. Party abgeleitet. | Falsche Reflexion; Ziel verfehlt |
| 17 mal 23 | Ein erfundenes Werkzeug `multipliziere` wird als normaler Text ausgegeben, statt 391 zu antworten. | Ungültiges Werkzeug (nur als Text); Ziel verfehlt |
| Buchungsbestätigung (2.3) | Der Agent gibt die Belegung vom Donnerstag als Freitag aus; nach Ablehnung erklärt er den Buchungsstatus unklar. | Falsche Werte; Ziel verfehlt |

Beim Rechentest erfolgt kein tatsächlicher Werkzeugaufruf. Deshalb zählt die Messung dafür keinen ungültigen Aufruf.

</div>

### 1.3 Erste Messung über 13 Aufgaben

Beide Tabellen aus `messen.py` übernehmen. Die Buchungsaufgabe darf vor Teil 2 noch scheitern.

```powershell
docker compose run --rm app messen.py
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

**Messung am 14.11.2026:** `llama3.2:3b`, `agent.v1`, Temperatur 0,
`HEUTE=2026-11-03`, mit `tage_bis`, vor dem Ergänzen der Raumbuchung aus Teil 2.

| Variante | Antwort | Werkz. | ungültig | Fehler | Abbruch | Aufrufe Ø | Tokens Ø | Dauer Ø |
|---|---|---|---|---|---|---|---|---|
| agent.v1.yaml | 2/13 | 8/13 | 0 | 3 | 0 | 1,1 | 1077 | 15,4 s |

| Variante | datum | direkt | wissen | mehrschritt | schreibend | ohne | fehlt |
|---|---|---|---|---|---|---|---|
| agent.v1.yaml | 1/4 | 1/1 | 0/4 | 0/1 | 0/1 | 0/1 | 0/1 |

Die beiden gezählten Treffer sind Raumbelegung und größter Seminarraum.
Bei der Raumfrage stimmt die Endaussage nur zufällig, weil der falsche Tag abgefragt wurde.

[Messprotokoll mit allen 13 Aufgaben](uebung_3/messungen/teil1_3_messung_2026-11-14.txt)

</div>

„Antwort“ prüft Stichwörter, „Werkz.“ die verwendeten Werkzeuge. Die Antwort muss zusätzlich inhaltlich geprüft werden. „Aufrufe Ø“ zählt Werkzeugaufrufe; „Tokens Ø“ summiert die gemeldeten Eingabe-Tokens pro Aufgabe.

### 1.4 Warum steigen die Eingabe-Tokens bei mehreren Modellaufrufen?

Eine Aufgabe mit mehreren Schritten betrachten und die Tokenwerte erklären.

```powershell
$frage = "Lies zuerst pruefungsanmeldung.md. Wie viele Tage bleiben von heute bis zum Ende der Pruefungsanmeldung? Hole das heutige Datum und berechne die Tage mit tage_bis."
docker compose run --rm app agent.py --ohne-mcp $frage
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

- Die erste Modellantwort fordert **drei Werkzeuge gleichzeitig an**. Unser Code führt sie nacheinander aus: `suche_wissen(begriff='pruefungsanmeldung')`, `lies_datei(datei='pruefungsanmeldung.md')`, `tage_bis(datum='heute')`.
- Die Suche findet nichts, weil sie im Dateiinhalt nach `pruefungsanmeldung` sucht; dort steht „Prüfungsanmeldung“. Das direkte Lesen der Datei liefert dagegen die Frist. Die Berechnung scheitert, weil `heute` kein gültiges Zieldatum ist. Der Agent korrigiert den Fehler nicht und antwortet „Keine Information.“
- Der Verlauf wächst von **2 auf 6 Nachrichten**: Zu Systemnachricht und Frage kommen eine Modellnachricht mit drei Aufrufen und drei Werkzeugergebnisse hinzu.

| Modellaufruf | Nachrichten im Verlauf | Gemeldete Eingabe-Tokens |
|---|---:|---:|
| 1 | 2 | 600 |
| 2 | 6 | 528 |

Gesamt: **1128 Eingabe-Tokens, 24,1 s**. Normalerweise vergrößern die zusätzlichen
Nachrichten den Eingabekontext. Hier sinkt der Tokenwert trotzdem: Die verwendete
Llama-Vorlage fügt die ausführliche Werkzeugliste nur bei einer abschließenden
Nutzernachricht ein (`if and $.Tools $last`). Beim zweiten Aufruf endet der
Verlauf mit einem Werkzeugergebnis; die Werkzeugliste entfällt in der Vorlage.
Ein größerer Nachrichtenverlauf bedeutet deshalb in diesem Lauf keinen längeren
fertig formatierten Prompt.

[Testprotokoll](uebung_3/messungen/teil1_4_tokens_2026-11-14.txt) · [Ausgelesene Modellvorlage](uebung_3/messungen/llama3_2_vorlage_2026-11-14.txt)

</div>

### 1.5 Was passiert mit `--max-schritte 1`, und warum ist ein Limit nötig?

Eine Frage mit mindestens zwei nötigen Werkzeugen mit einem Modellaufruf testen.

Mit derselben Frage aus 1.4:

```powershell
docker compose run --rm app agent.py --ohne-mcp $frage --max-schritte 1
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

- `--max-schritte 1` erlaubt **einen Modellaufruf**. Dessen Antwort enthält in diesem Test dieselben drei Werkzeuganforderungen wie in 1.4. Die innere Schleife führt alle drei aus; für Werkzeugaufrufe gibt es kein eigenes Limit.
- Danach folgt „Abgebrochen nach 1 Modellaufrufen ohne Antwort.“ Der Agent kann die Ergebnisse nicht mehr auswerten oder den Datumsfehler korrigieren.
- Gemessen: **1 Modellaufruf, 3 Werkzeugaufrufe, 600 Eingabe-Tokens, 4,8 s**. Das Limit zählt Modellaufrufe, nicht einzelne Werkzeuge.
- Ein Schrittlimit verhindert endlose Schleifen und begrenzt Laufzeit und Tokenverbrauch.
- Problem im Test: Das Modell fordert die Berechnung schon an, bevor es die gelesene Frist auswerten kann, und übergibt `heute` als Zieldatum. Nach dem Abbruch ist keine Korrektur mehr möglich.

[Testprotokoll](uebung_3/messungen/teil1_5_limit_2026-11-14.txt)

</div>

## Teil 2 · Eigene Werkzeuge, lokal und als MCP-Server

### 2.1 Ein lokales Werkzeug: Tage bis zur Prüfungsanmeldung

TODO 2 umsetzen: `tage_bis(datum)` mit Beschreibung und JSON-Schema registrieren. `HEUTE`, vergangene und ungültige Daten berücksichtigen. Werkzeugreihenfolge und Antwort prüfen.

```powershell
docker compose run --rm app agent.py "Wie viele Tage habe ich noch, bis die Prüfungsanmeldung endet?"
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

`tage_bis` ist umgesetzt und registriert; Beschreibung und Fehlermeldungen sind korrigiert.

**Direkte Tests am 14.11.2026**, jeweils mit `HEUTE=2026-11-03`:

| Eingabe | Ergebnis |
|---|---|
| `2026-11-20` | 17 Tage |
| `2026-11-03` | 0 Tage |
| `2026-11-01` | 2 Tage in der Vergangenheit |
| `2026-02-30`, `heute`, `20.11.2026` | Jeweils verständliche Fehlermeldung zum Datumsformat |

Alle sechs Tests bestanden.

**Agententest:** Nur `tage_bis(datum='2026-11-05')` wird aufgerufen. Das Werkzeug liefert korrekt 2 Tage zu diesem Datum. Anschließend meldet der Agent, keine genauen Anmeldefristen zu kennen.

- `heute` und die Wissenssuche fehlen; das Zieldatum ist geraten.
- Laut Wissensbasis endet die Anmeldung am 20. November. Richtig wären **17 Tage**.
- Das Werkzeug funktioniert; der Agent löst die mehrschrittige Aufgabe mit v1 noch nicht. Verbesserungen werden in Teil 3 untersucht.

[Werkzeugtests](uebung_3/messungen/teil2_1_werkzeugtests_2026-11-14.txt) · [Agententest](uebung_3/messungen/teil2_1_frist_2026-11-14.txt)

</div>

### 2.2 Ein Werkzeug im MCP-Server: Einen Raum buchen

TODO 3a umsetzen: `raum_buchen(raum, datum, uhrzeit, name)` im MCP-Server ergänzen. Docstring und angebotene Werkzeuge prüfen.

```powershell
docker compose restart campus-mcp
docker compose run --rm app mcp_werkzeuge.py
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

`raum_buchen` ist im MCP-Server umgesetzt und wird über MCP angeboten.

- Beschreibung: Bucht einen freien Seminarraum für eine Person in einem Zeitfenster. Benötigt Raum, Datum, Uhrzeit und Name; belegte Slots werden nicht überschrieben.
- `O-108`, `2026-11-06`, `09:45`, `Kim`: Buchung erfolgreich und über `raum_frei` sichtbar.
- Eine zweite Buchung desselben Slots wird abgelehnt; freie Alternativen werden genannt.
- Unbekannter Raum, ungültiges Datum, Wochenende, falscher Slot und leerer Name liefern `Fehler:`-Meldungen. Auch ein regulär belegter Slot wird abgelehnt.

Die automatisierte Prüfung läuft mit:

```powershell
docker compose run --rm app pruefen_teil2.py
```

[Prüfprotokoll für Buchung und Bestätigung](uebung_3/messungen/teil2_pruefung_2026-11-14.txt)

</div>

### 2.3 Schreibaktionen bestätigen

TODO 3b umsetzen: Schreibende Werkzeuge erst nach Bestätigung ausführen.

#### 1. Was passiert bei Zustimmung und Ablehnung?

Je einmal mit `j` und `n` testen. Nach Ablehnung darf keine Buchung ausgeführt werden.

```powershell
docker compose run --rm app agent.py "Buche mir O-108 am Freitag um 9:45 Uhr für die Lerngruppe Kim."
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Die Bestätigung ist eingebaut. Getestet wurde die Frage aus dem Aufgabenblatt
mit `HEUTE=2026-11-03`. Zwischen den Fällen wurde der MCP-Server neu gestartet.
Das Modell wählt in beiden Fällen fälschlich Donnerstag, den 05.11., statt Freitag, den 06.11.

| Eingabe | Werkzeugergebnis | Antwort des Modells |
|---|---|---|
| `j` | Der Aufruf wird ausgeführt, aber der gewählte Donnerstag um 09:45 ist belegt. Das Werkzeug lehnt die Buchung ab und nennt freie Slots. | Der Agent behauptet, Freitag sei belegt, und übernimmt die Alternativen vom Donnerstag. Falsches Datum, keine Buchung. |
| `n` | Aufruf als `abgelehnt` zurückgegeben; keine Buchung. Die Nachkontrolle zeigt keine neue Belegung; Freitag ist frei. | „Entschuldigung, ich habe keine Informationen darüber, ob die Raumbuchung erfolgreich war.“ Kein erneuter Versuch, aber eine unklare Erklärung der Ablehnung. |

Ohne interaktives Terminal wird keine Zustimmung angenommen. Lesende Werkzeuge benötigen keine Bestätigung.
`messen.py` bestätigt Testbuchungen automatisch; `j` und `n` wurden deshalb zusätzlich im Terminal geprüft.

Die sechs automatisierten Prüfungen für Buchung und Bestätigung bestehen.
Die falsche Datumswahl ist ein Modellfehler. Die Bestätigung und die Belegungsprüfung verhindern die unerwünschte Buchung.

[Test mit `j`](uebung_3/messungen/teil2_3_zustimmung_2026-11-14.txt) · [Test mit `n` und Nachkontrolle](uebung_3/messungen/teil2_3_ablehnung_2026-11-14.txt)

`messen.py` läuft mit dem fertigen Stand aus Teil 2 über alle 13 Aufgaben durch.
[Abschlussprotokoll als Ausgangspunkt für Teil 3](uebung_3/messungen/teil2_abschluss_messung_2026-11-14.txt)

</div>

#### 2. Wie werden schreibende Werkzeuge erkannt, und was ist daran schwach?

Erkennung in `mcp_werkzeuge.py` erklären und mit MCP Tool Annotations vergleichen.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

`mcp_werkzeuge.py` prüft den Anfang des Werkzeugnamens: `raum_buchen`, `buche`,
`loesche` oder `sende` markieren ein Werkzeug als schreibend.

Das ist fehleranfällig: Eine anders benannte Schreibaktion kann übersehen,
ein lesendes Werkzeug versehentlich markiert werden. Die Information sollte
vom MCP-Server als Tool Annotation kommen, insbesondere über `readOnlyHint`.
Die Bestätigung muss weiterhin vor der Ausführung im Programm geprüft werden.

</div>

#### 3. Optional: MCP Inspector

Nicht bearbeitet.

## Teil 3 · Verbessern und messen

Mindestens zwei Ansätze einzeln gegen den fertigen Stand aus Teil 2 messen:

- **Prompt:** `agent.v2.yaml` mit Werkzeugregeln und ein bis zwei Beispielabläufen; v1 unverändert lassen.
- **Werkzeug:** Datumseingaben in `raum_frei`, `raum_buchen` und `mensa_speiseplan` fehlertoleranter machen (`heute`, `morgen`, Wochentag, angehängte Uhrzeit); Beschreibungen anpassen.
- **Workflow:** Festes Routing aus `workflow.py` mit dem Agenten vergleichen.

### 3.1 Welcher Ansatz hilft bei welchem Aufgabentyp?

Gesamtergebnisse und Ergebnisse nach Typ für beide Modelle eintragen. Änderungen je Messstand nennen.

Nach dem Anlegen von `agent.v2.yaml`:

```powershell
docker compose run --rm -e LLM_MODEL=llama3.2:3b app messen.py prompts/agent.v1.yaml prompts/agent.v2.yaml workflow
docker compose run --rm -e LLM_MODEL=qwen2.5:3b app messen.py prompts/agent.v1.yaml prompts/agent.v2.yaml workflow
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

**TODO:** Zwei Ansätze umsetzen und einzeln messen. Beide Tabellen je Modell und Messstand einfügen; Wirkung nach Aufgabentyp kurz auswerten.

</div>

### 3.2 Bei welchen Aufgaben gewinnt der Workflow, bei welchen der Agent?

Ergebnisse mit festen Pfaden und Werkzeugschleife erklären.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

**TODO:** Mit Beispielen aus den Messungen beantworten.

</div>

### 3.3 Welches Modell wählen wir für Agent und Workflow?

Auswahl mit Antwortqualität, Tokens und Dauer begründen.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

**TODO:** Nach den Messungen beantworten.

</div>

### 3.4 Academic Cloud: größeres Modell

Nicht bearbeitet (optionaler Vergleich).

## Teil 4 und 5 · Ergänzung aus VL 6

**TODO:** Ergänztes Aufgabenblatt für Orchestrierung, Memory und Multi-Agent-Setup besorgen und Aufgaben nachtragen.

## Zusatz · ReAct ohne Function Calling

Nicht bearbeitet. Laut Aufgabenblatt entfällt der Zusatz bei mindestens 80 % nachgewiesener Anwesenheit.

**TODO:** Anwesenheitsnachweis vor der Abgabe prüfen. Ohne ausreichenden Nachweis ist der Zusatz erforderlich: `react.py` umsetzen, mit denselben Aufgaben messen und Robustheit, Aufwand sowie zwei Fehler der Textvariante vergleichen.

## Abgabe

In Moodle unter „Übung 3 (P3)“ Repository-Link und Commit-Hash angeben. Frist laut Moodle. Das Repository muss öffentlich oder für `PascalLaube` freigegeben sein.

- [ ] Start mit dokumentierter `.env` geprüft; keine Secrets eingecheckt.
- [x] Abhängigkeiten gepinnt.
- [x] TODO 1, 2, 3a und 3b umgesetzt; `messen.py` läuft durch.
- [x] `raum_buchen` läuft im MCP-Server; Zustimmung und Ablehnung getestet.
- [ ] Abläufe, Fehlermodi und Messtabellen vollständig.
- [ ] Aufgaben aus VL 6 und Anwesenheitsnachweis berücksichtigt.

Buchungen sind flüchtig; `docker compose restart campus-mcp` setzt sie zurück. Bei Serverproblemen: `docker compose logs campus-mcp`.
