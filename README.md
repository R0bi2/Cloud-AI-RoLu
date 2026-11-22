# Cloud-AI-RoLu – Übung 3 / P3

**Ein Agent mit Werkzeugen · Cloud-native AI · WS 2026/27**

## Abgabestand

- [x] Teil 1–3 umgesetzt, gemessen und dokumentiert.
- [ ] Teil 4 mit den zugehörigen Antworten und Reflexionen ergänzen.

Abgabe: **23.11.2026, 23:59 Uhr** in Moodle mit Repository-Link und Commit-Hash.
Das Repository muss öffentlich oder für `PascalLaube` freigegeben sein.
Bei einem öffentlichen Repository gehören Namen und Matrikelnummern nur in den Moodle-Abgabetext.

## Start

Docker Desktop muss laufen. Einmalig im Hauptordner:

```powershell
cd uebung_3/starter
cp .env.example .env
docker volume create cnai-ollama-modelle   # nur falls das Volume noch fehlt
```

In der lokalen `.env`:

```dotenv
LLM_BASE_URL=http://ollama:11434/v1
LLM_MODEL=llama3.2:3b
LLM_API_KEY=nicht-noetig
MCP_URL=http://campus-mcp:8000/mcp
HEUTE=2026-11-03
```

Alle folgenden Befehle laufen in `uebung_3/starter`. `HEUTE` hält das Datum für die Vergleiche fest.

```powershell
docker compose run --rm --build app werkzeuge.py
docker compose run --rm app mcp_werkzeuge.py
```

Beim ersten Start werden beide Modelle geladen. Buchungen werden mit `docker compose restart campus-mcp` zurückgesetzt.

## Teil 1 · Die Agent-Schleife

### 1.1 Agent-Schleife umsetzen und drei Fragen testen

TODO 1 in `agent.py` umsetzen. Für jede Frage die Werkzeugaufrufe mit Argumenten und die Antwort bewerten.

```powershell
docker compose run --rm app agent.py "Was gibt es heute in der Mensa?"
docker compose run --rm app agent.py "Ich bin am Tag meiner Klausur krank. Was muss ich tun?"
docker compose run --rm app agent.py "Ist O-108 am Donnerstag um 14 Uhr frei?"
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Die Schleife ist umgesetzt. Die folgenden Ergebnisse stammen von `agent.v1` mit `llama3.2:3b`, noch ohne Buchungswerkzeug.

| Frage | Werkzeugaufrufe | Bewertung |
|---|---|---|
| Mensa heute | `mensa_speiseplan(datum='heute')` | Ungültiges Datum. Der Agent korrigiert es nicht und beantwortet die Frage nicht. |
| Krank am Klausurtag | `heute()` → `raeume_auflisten()` → `mensa_speiseplan(datum='2026-11-05')` | Keine passende Wissenssuche. Die Antwort nennt allgemein einen Arzt, erklärt aber nicht das Vorgehen bei Prüfungsunfähigkeit. |
| O-108 am Donnerstag, 14 Uhr | `raum_frei(raum='O-108', datum='2026-11-04')` | Mittwoch statt Donnerstag abgefragt. „Nicht frei“ stimmt nur zufällig auch für Donnerstag. |

Mensa: [Messung](uebung_3/messungen/teil1_1_mensa_2026-11-14.txt) · Klausur: [Messung](uebung_3/messungen/teil1_1_klausur_2026-11-14.txt) · Raum: [Messung](uebung_3/messungen/teil1_1_raum_2026-11-14.txt)

</div>

### 1.2 Welche Fehlermodi nach Huyen sehen wir?

Die beobachteten Fehler den Fehlermodi aus der Vorlesung zuordnen.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

| Beobachtung | Fehlermodus |
|---|---|
| `heute` statt eines Datums, falscher Wochentag oder geratene Prüfungsfrist | Falsche Werte; Ziel verfehlt |
| Raumliste oder Speiseplan bei einer Frage zur Prüfungsunfähigkeit | Ziel verfehlt; Ineffizienz |
| Suche mit zu langem Begriff oder falscher Umlautschreibweise; danach keine weitere Suche | Ziel verfehlt |
| Erfundenen Raum wie M-101 oder P-123 abfragen | Falsche Werte; Ziel verfehlt |
| Buchungswerkzeug fehlt vor Teil 2 | Werkzeugfehler |
| Erfundenes Werkzeug als normale Textantwort ausgeben | Ungültiges Werkzeug (nur als Text); Ziel verfehlt |
| Party oder Speiseplan aus unpassenden Ergebnissen erfinden | Falsche Reflexion; Ziel verfehlt |
| Qwen v1 bucht für den falschen Tag; Qwen v2 behauptet eine Buchung ohne `raum_buchen` | Falsche Werte bzw. falsche Reflexion; Ziel verfehlt |
| Nach Ablehnung bleibt die Erklärung zum Buchungsstatus unklar | Ziel verfehlt |
| Unnötig `tage_bis` für 17 mal 23 aufrufen | Ineffizienz |

Werkzeug-JSON als normale Textantwort zählt in der Messung nicht als tatsächlicher ungültiger Aufruf.

</div>

### 1.3 Erste Messung über 13 Aufgaben

Die Messung ausführen und beide Tabellen übernehmen. Die Buchungsaufgabe darf vor Teil 2 noch scheitern.

```powershell
docker compose run --rm app messen.py
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

`agent.v1` mit `llama3.2:3b`, noch ohne Buchungswerkzeug:

| Variante | Antwort | Werkz. | ungültig | Fehler | Abbruch | Aufrufe Ø | Tokens Ø | Dauer Ø |
|---|---|---|---|---|---|---|---|---|
| agent.v1.yaml | 2/13 | 8/13 | 0 | 3 | 0 | 1,1 | 1077 | 15,4 s |

| Variante | datum | direkt | wissen | mehrschritt | schreibend | ohne | fehlt |
|---|---|---|---|---|---|---|---|
| agent.v1.yaml | 1/4 | 1/1 | 0/4 | 0/1 | 0/1 | 0/1 | 0/1 |

Gezählt werden die Raumbelegung und der größte Seminarraum. Bei der Raumbelegung wurde allerdings der falsche Tag abgefragt.

„Antwort“ prüft Stichwörter, „Werkz.“ die Werkzeugnamen. „Aufrufe Ø“ zählt Werkzeugaufrufe, „Tokens Ø“ die gesamten Eingabe-Tokens pro Aufgabe.

[Messung](uebung_3/messungen/teil1_3_messung_2026-11-14.txt)

</div>

### 1.4 Warum steigen die Eingabe-Tokens bei mehreren Modellaufrufen?

Eine Aufgabe mit mehreren Schritten betrachten und die Tokenwerte erklären.

```powershell
$frage = "Lies zuerst pruefungsanmeldung.md. Wie viele Tage bleiben von heute bis zum Ende der Pruefungsanmeldung? Hole das heutige Datum und berechne die Tage mit tage_bis."
docker compose run --rm app agent.py --ohne-mcp $frage
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Der Verlauf wächst von zwei auf sechs Nachrichten: Eine Modellnachricht mit drei Werkzeugaufrufen und deren drei Ergebnisse kommen dazu. Normalerweise steigt dadurch die Zahl der Eingabe-Tokens.

| Modellaufruf | Nachrichten | Eingabe-Tokens |
|---|---:|---:|
| 1 | 2 | 600 |
| 2 | 6 | 528 |

Hier sinkt der Wert trotzdem. Die Llama-Vorlage fügt die Werkzeugliste nur ein, wenn die letzte Nachricht von der Person kommt. Beim zweiten Aufruf endet der Verlauf mit einem Werkzeugergebnis, also fehlt diese Liste. Insgesamt sind es 1128 Eingabe-Tokens.

Die Suche scheitert an `pruefungsanmeldung` statt „Prüfungsanmeldung“. Die Datei wird zwar gelesen, aber `tage_bis(datum='heute')` liefert einen Fehler. Der Agent korrigiert ihn nicht.

[Messung](uebung_3/messungen/teil1_4_tokens_2026-11-14.txt) · [Modellvorlage](uebung_3/messungen/llama3_2_vorlage_2026-11-14.txt)

</div>

### 1.5 Was passiert mit `--max-schritte 1`, und warum ist ein Limit nötig?

Die Frage aus 1.4 mit nur einem erlaubten Modellaufruf testen.

```powershell
docker compose run --rm app agent.py --ohne-mcp $frage --max-schritte 1
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Nach einem Modellaufruf wird abgebrochen. Die drei angeforderten Werkzeuge werden noch ausgeführt, ihre Ergebnisse aber nicht mehr ausgewertet. Das Limit zählt Modellaufrufe, nicht einzelne Werkzeuge.

Gemessen: ein Modellaufruf, drei Werkzeugaufrufe, 600 Eingabe-Tokens und 4,8 Sekunden. Das Limit verhindert endlose Schleifen und begrenzt Laufzeit und Tokenverbrauch.

[Messung](uebung_3/messungen/teil1_5_limit_2026-11-14.txt)

</div>

## Teil 2 · Eigene Werkzeuge, lokal und als MCP-Server

### 2.1 Ein lokales Werkzeug: Tage bis zur Prüfungsanmeldung

TODO 2 umsetzen: `tage_bis(datum)` mit Beschreibung und JSON-Schema registrieren. Prüfen, ob der Agent Datum, Frist und Berechnung in der richtigen Reihenfolge abruft.

```powershell
docker compose run --rm app agent.py "Wie viele Tage habe ich noch, bis die Prüfungsanmeldung endet?"
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

`tage_bis` ist umgesetzt und registriert. Die direkten Tests ergeben:

| Eingabe | Ergebnis |
|---|---|
| `2026-11-20` | 17 Tage |
| `2026-11-03` | 0 Tage |
| `2026-11-01` | 2 Tage in der Vergangenheit |
| `2026-02-30`, `heute`, `20.11.2026` | Fehlermeldung zum Datumsformat |

Mit `agent.v1` wird nur `tage_bis(datum='2026-11-05')` aufgerufen. Das Werkzeug rechnet korrekt zwei Tage aus, aber der Agent hat die Frist geraten. Die Wissenssuche und `heute` fehlen. Richtig wären 17 Tage bis zum 20. November.

Werkzeug: [Messung](uebung_3/messungen/teil2_1_werkzeugtests_2026-11-14.txt) · Agent: [Messung](uebung_3/messungen/teil2_1_frist_2026-11-14.txt)

</div>

### 2.2 Ein Werkzeug im MCP-Server: Einen Raum buchen

TODO 3a umsetzen: `raum_buchen(raum, datum, uhrzeit, name)` im MCP-Server ergänzen. Docstring und angebotene Werkzeuge prüfen.

```powershell
docker compose restart campus-mcp
docker compose run --rm app mcp_werkzeuge.py
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

`raum_buchen` wird vom MCP-Server angeboten. Die Beschreibung nennt Raum, Datum, Zeitfenster und Name sowie die Änderung der Belegung.

O-108 lässt sich am 06.11. um 09:45 für Kim buchen. Die Buchung ist über `raum_frei` sichtbar. Eine zweite Buchung überschreibt sie nicht. Ungültige Eingaben und belegte Slots werden abgelehnt. Die sechs Buchungs- und Bestätigungstests bestehen.

```powershell
docker compose run --rm app pruefen_teil2.py
```

[Messung](uebung_3/messungen/teil2_pruefung_2026-11-14.txt)

</div>

### 2.3 Schreibaktionen bestätigen

TODO 3b umsetzen: Schreibende Werkzeuge erst nach Bestätigung ausführen.

#### 1. Was passiert bei Zustimmung und Ablehnung?

Je einmal mit `j` und `n` testen. Was macht das Modell nach der Ablehnung?

```powershell
docker compose run --rm app agent.py "Buche mir O-108 am Freitag um 9:45 Uhr für die Lerngruppe Kim."
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Die Bestätigung ist eingebaut. Mit `agent.v1` wählt das Modell in beiden Fällen Donnerstag, 05.11., statt Freitag, 06.11.

| Eingabe | Ergebnis |
|---|---|
| `j` | Der Aufruf wird ausgeführt, aber der falsche Donnerstag ist belegt. Keine Buchung; die genannten Alternativen gehören ebenfalls zum falschen Tag. |
| `n` | Werkzeug nicht ausgeführt, keine Buchung. Der Agent versucht es nicht erneut, erklärt die Ablehnung aber unklar. |

Ohne interaktives Terminal wird keine Zustimmung angenommen. Lesende Werkzeuge brauchen keine Bestätigung.

Zustimmung: [Messung](uebung_3/messungen/teil2_3_zustimmung_2026-11-14.txt) · Ablehnung: [Messung](uebung_3/messungen/teil2_3_ablehnung_2026-11-14.txt)

</div>

#### 2. Wie werden schreibende Werkzeuge erkannt, und was ist daran schwach?

Die Erkennung in `mcp_werkzeuge.py` erklären und mit MCP Tool Annotations vergleichen.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Namen mit den Präfixen `raum_buchen`, `buche`, `loesche` oder `sende` gelten als schreibend. Das kann anders benannte Schreibaktionen übersehen oder lesende Werkzeuge falsch einordnen.

Die Information sollte vom Server über Tool Annotations wie `readOnlyHint` kommen. Die Bestätigung muss der Code trotzdem vor der Ausführung prüfen.

</div>

## Teil 3 · Verbessern und messen

Mindestens zwei Ansätze aus Prompt, Werkzeug und Workflow einzeln gegen den fertigen Stand aus Teil 2 messen.

### 3.1 Welcher Ansatz hilft bei welchem Aufgabentyp?

Beide Tabellen für beide Modelle übernehmen und die Wirkung nach Aufgabentyp auswerten.

```powershell
docker compose run --rm -e LLM_MODEL=llama3.2:3b app messen.py prompts/agent.v1.yaml prompts/agent.v2.yaml workflow
docker compose run --rm -e LLM_MODEL=qwen2.5:3b app messen.py prompts/agent.v1.yaml prompts/agent.v2.yaml workflow
```

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Wir vergleichen Prompt v2 und den vorhandenen Workflow jeweils mit `agent.v1`. V2 ergänzt Werkzeugregeln und zwei Beispielabläufe. Die Werkzeuge bleiben gleich; alle Varianten nutzen dieselben 13 Aufgaben und Temperatur 0.

**Llama 3.2 3B**

| Variante | Antwort | Werkz. | ungültig | Fehler | Abbruch | Aufrufe Ø | Tokens Ø | Dauer Ø |
|---|---|---|---|---|---|---|---|---|
| agent.v1.yaml | 3/13 | 10/13 | 0 | 5 | 0 | 0,9 | 1287 | 26,8 s |
| agent.v2.yaml | 5/13 | 9/13 | 0 | 3 | 0 | 1,0 | 2546 | 40,8 s |
| workflow | 5/13 | 7/13 | 0 | 3 | 0 | 0,7 | 447 | 12,0 s |

| Variante | datum | direkt | wissen | mehrschritt | schreibend | ohne | fehlt |
|---|---|---|---|---|---|---|---|
| agent.v1.yaml | 1/4 | 1/1 | 1/4 | 0/1 | 0/1 | 0/1 | 0/1 |
| agent.v2.yaml | 3/4 | 1/1 | 0/4 | 0/1 | 0/1 | 1/1 | 0/1 |
| workflow | 2/4 | 0/1 | 1/4 | 0/1 | 0/1 | 1/1 | 1/1 |

[Messung](uebung_3/messungen/teil3_llama3_2_vergleich_2026-11-17.txt)

**Qwen 2.5 3B**

| Variante | Antwort | Werkz. | ungültig | Fehler | Abbruch | Aufrufe Ø | Tokens Ø | Dauer Ø |
|---|---|---|---|---|---|---|---|---|
| agent.v1.yaml | 3/13 | 8/13 | 0 | 0 | 0 | 0,6 | 1728 | 9,2 s |
| agent.v2.yaml | 4/13 | 7/13 | 0 | 1 | 0 | 1,2 | 3767 | 16,2 s |
| workflow | 3/13 | 8/13 | 0 | 0 | 0 | 0,7 | 431 | 7,5 s |

| Variante | datum | direkt | wissen | mehrschritt | schreibend | ohne | fehlt |
|---|---|---|---|---|---|---|---|
| agent.v1.yaml | 0/4 | 1/1 | 0/4 | 0/1 | 1/1 | 0/1 | 1/1 |
| agent.v2.yaml | 2/4 | 1/1 | 0/4 | 0/1 | 1/1 | 0/1 | 0/1 |
| workflow | 1/4 | 1/1 | 0/4 | 0/1 | 0/1 | 0/1 | 1/1 |

[Messung](uebung_3/messungen/teil3_qwen2_5_vergleich_2026-11-17.txt)

- **Datum:** Beide Workflows lösen „Mensa heute“. Die höheren Trefferzahlen von v2 täuschen: Llama erfindet einen „Linsensalat“, Qwen fragt falsche Tage ab. Auch „nicht belegt“ wird als „belegt“ gezählt.
- **Wissen:** Der Llama-Workflow findet den Preis der Ersatzkarte. Die Agenten suchen nicht passend nach; Qwen löst keine der vier Wissensfragen.
- **Direkte Fragen:** Alle Agenten nennen O-201 korrekt. Beim Workflow gelingt das nur Qwen.
- **Mehrschritt und Buchung:** Keine Variante löst die Fristberechnung oder die gewünschte Buchung korrekt. Qwen v1 bucht am falschen Tag; v2 behauptet eine Buchung nach einer bloßen Belegungsabfrage.
- **Ohne Werkzeug und fehlende Information:** Llama v2 und der Llama-Workflow rechnen 17 mal 23 richtig. Beide Workflows und Qwen v1 lehnen die unbekannte Partyfrage passend ab.

Die Stichworttreffer sind also keine vollständige Qualitätsbewertung. Besonders die Datums- und Buchungstreffer müssen am tatsächlichen Aufruf geprüft werden.

</div>

### 3.2 Bei welchen Aufgaben gewinnt der Workflow, bei welchen der Agent?

Die Ergebnisse mit dem Unterschied zwischen festen Pfaden und Werkzeugschleife erklären.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Der Workflow hilft bei klaren Abläufen wie Mensa heute oder Ersatz-Campuskarte. Er holt die Daten in einer festen Reihenfolge. Der Agent könnte nachsuchen oder nach einem Fehler einen anderen Weg wählen, macht das aber oft nicht.

Beim größten Seminarraum lösen beide Llama-Agenten die Frage, während der Llama-Workflow fälschlich die Belegung von O-108 abfragt. Bei Qwen lösen Agent und Workflow diese Frage.

Der Workflow hat keine Pfade für `tage_bis` und `raum_buchen`. Die Agenten könnten diese Schritte verbinden, schaffen aber weder die Fristberechnung noch die gewünschte Buchung korrekt. Ihre größere Freiheit bringt bei diesen Aufgaben noch keinen erfolgreichen Vorteil.

</div>

### 3.3 Welches Modell wählen wir für Agent und Workflow?

Die Auswahl mit Antwortqualität, Tokens und Dauer begründen.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

**Agent: Qwen 2.5 3B mit v1.** Beide v1-Agenten erreichen 3/13, Qwen braucht aber 9,2 statt 26,8 Sekunden. Dafür sind es 1728 statt 1287 Eingabe-Tokens. Qwen gibt bei der unbekannten Party fehlende Information an; Llama erfindet eine Veranstaltung. V2 kostet deutlich mehr Tokens, ohne die Antworten zuverlässig zu verbessern. Datumsangaben und Buchungen bleiben bei beiden Modellen problematisch.

**Workflow: Llama 3.2 3B.** Es erreicht 5/13 statt 3/13 bei Qwen, mit ähnlichem Tokenverbrauch: 447 gegenüber 431. Es dauert mit 12,0 statt 7,5 Sekunden länger, löst dafür die Ersatzkarten- und Rechenfrage korrekt. Qwen findet dagegen den größten Raum. Einer der fünf Llama-Treffer ist eine widersprüchliche Samstagsantwort; wir verlassen uns deshalb nicht nur auf die Trefferzahl.

</div>

## Teil 4 · Orchestrierung, Memory und Supervisor

### 4.1 Speichern und Laden umsetzen.

```powershell
docker compose run --rm app orchestrator.py --sitzung kim "Ist O-108 am Freitag um 14 Uhr frei?"
docker compose run --rm app orchestrator.py --sitzung kim "Und um 9:45?"
docker compose run --rm app orchestrator.py --sitzung kim --verlauf
```

    Sitzung Kim: /app/sitzungen/kim.json

    Aufruf 1:
    → raum_frei(datum='2026-11-05', raum='O-108')
    ← O-108 am 2026-11-05 (donnerstag): frei um 11:30, 15:45, 17:30. Belegt: 08:00 (Webapplikationen), 09:45 (Webapplikationen), 14:00 (Tutorium).

    Leider ist O-108 am Freitag um 14 Uhr nicht frei.

    Sitzung kim · fertig · 9 Nachrichten · 4 Modellaufrufe · 3680 Eingabe-Tokens gesamt · llama3.2:3b

    
    Aufruf 2:
    → raum_frei(raum='O-108', datum='2026-11-05')
    ← O-108 am 2026-11-05 (donnerstag): frei um 11:30, 15:45, 17:30. Belegt: 08:00 (Webapplikationen), 09:45 (Webapplikationen), 14:00 (Tutorium).

    O-108 ist am Freitag um 9:45 Uhr belegt.

    Sitzung kim · fertig · 13 Nachrichten · 6 Modellaufrufe · 5947 Eingabe-Tokens gesamt · llama3.2:3b

    Aufruf 3:
    user      Ist O-108 am Freitag um 14 Uhr frei?
    assistant → raum_frei({"raum":"O-108","datum":"2026-11-05"})
    tool      O-108 am 2026-11-05 (donnerstag): frei um 11:30, 15:45, 17:30. Belegt: 08:00 (Webapplikationen), 09:45 (Webapplikationen), 14:00 (Tutorium).
    assistant Leider ist O-108 am Freitag um 14 Uhr nicht frei.
    user      Ist O-108 am Freitag um 14 Uhr frei?
    assistant → raum_frei({"datum":"2026-11-05","raum":"O-108"})
    tool      O-108 am 2026-11-05 (donnerstag): frei um 11:30, 15:45, 17:30. Belegt: 08:00 (Webapplikationen), 09:45 (Webapplikationen), 14:00 (Tutorium).
    assistant Leider ist O-108 am Freitag um 14 Uhr nicht frei.
    user      Und um 9:45?
    assistant → raum_frei({"raum":"O-108","datum":"2026-11-05"})
    tool      O-108 am 2026-11-05 (donnerstag): frei um 11:30, 15:45, 17:30. Belegt: 08:00 (Webapplikationen), 09:45 (Webapplikationen), 14:00 (Tutorium).
    assistant O-108 ist am Freitag um 9:45 Uhr belegt.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

    in orchestrator.py main:
    sitzung = laden(args.sitzung)
    
    das holt den verlauf aus der JSON

</div>


### 4.1.1 Öffnet app/sitzungen/kim.json . Welche Rollen kommen in welcher Reihenfolge vor? Woran erkennt die API, welches Werkzeugergebnis zu welchem Aufruf gehört?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Rollen (in Reihenfolge ) sytem, user, assistant, tool, assistant

Die API erkennt zu welchem Aufruf das Werkzeugergebnis gehört anhand der id und der tool-call-id

</div>

### 4.1.2 Stellt dieselbe Folgefrage „Und um 9:45?“ an agent.py . Was antwortet er, und warum?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

```powershell
docker compose run --rm app agent.py  "Und um 9:45?"
```

Werkzeuge: suche_wissen, lies_datei, heute, tage_bis, raeume_auflisten, raum_frei, raum_buchen, mensa_speiseplan

  Modellaufruf 1: 1052 Eingabe-Tokens · 2 Nachrichten im Verlauf
  ? Soll ich raum_buchen(name='um 9:45', datum='2026-11-05', uhrzeit='09:45') ausführen? [j/N] N
  → raum_buchen(name='um 9:45', datum='2026-11-05', uhrzeit='09:45')  [abgelehnt]
  ← Abgelehnt: raum_buchen wurde nicht ausgeführt. Die Zustimmung fehlt.

agent.py ruft das Raum-buchen tool auf. Es rät welchen Zweck die Nachricht hat.
Es hat keinen Zugang zu den in JSON gespeicherten Verläufen. agent.py legt eine nachrichten-Liste an die nur innerhalb eines Programmaufrufs bzw. innerhalb eines Ergebnis-Objektes besteht.

</div>

### 4.1.3. Vergleicht die Eingabe-Tokens der ersten und der zweiten Frage. Startet danach eine neue Sitzung mit -- fenster 2 und stellt beide Fragen noch einmal. Was passiert, und warum beginnt kuerzen() das Fenster immer bei einer Nachricht der Person?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

  1. Aufruf
  Frage 1: 3680 Eingabe-Tokens gesamt
  Frage 2: Frage: 5947 Eingabe-Tokens gesamt

  2. Aufruf
  Frage 1:
    → raum_frei(datum='2026-11-05', uhrzeit='14:00', raum='O-108')
    ← O-108 am 2026-11-05 (donnerstag): frei um 11:30, 15:45, 17:30. Belegt: 08:00 (Webapplikationen), 09:45 (Webapplikationen), 14:00 (Tutorium).

    O-108 ist am Freitag um 14 Uhr frei.

    Sitzung kim · fertig · 17 Nachrichten · 8 Modellaufrufe · 8516 Eingabe-Tokens gesamt · llama3.2:3b
  Frage 2:   → raum_frei(datum='2026-11-05', raum='O-108', uhrzeit='09:45')
    ← O-108 am 2026-11-05 (donnerstag): frei um 11:30, 15:45, 17:30. Belegt: 08:00 (Webapplikationen), 09:45 (Webapplikationen), 14:00 (Tutorium).

    O-108 ist am Freitag um 9:45 Uhr belegt.

    Sitzung kim · fertig · 25 Nachrichten · 12 Modellaufrufe · 14258 Eingabe-Tokens gesamt · llama3.2:3b


Die Token-Anzahl nimmt trotz gleicher Fragestellung zu. Das liegt daran dass alte Fragen mit in das Prompt übergeben werden
In orchestrator.py wird die alte Sitzung geladen und in Zeile 88 die neue Frage an ihren Verlauf angehängt. Zeile 97 sendet diesen (durch kuerzen() begrenzten) Verlauf ans Modell, wodurch frühere Nachrichten weitere Eingabe-Tokens verursachen können.

</div>

### 4.1.4. Begründet, wo genau ihr in ausfuehren() speichert. Was geht verloren, wenn der Container zwischen zwei Übergängen abstürzt? 

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

  Wir speichern während die Sitzung läuft, noch bevor der nächste Schritt ausgewählt wird. Verloren geht der nicht gespeicherte nächste Zustand (durch Schritt ausgewählt)

</div>


## 4.2

  in kim.json gibt es jetzt Einträge status. um unvollendete Sitzungen zu finden und fort zu führen.

  ```powershell
  docker compose run --rm app orchestrator.py --sitzung kim "Dann buch mir den Raum von vorhin für
  14 Uhr, für die Lerngruppe Kim."
  docker compose run --rm app orchestrator.py --sitzung kim --bestaetigen
  ```

## 4.2.1 
  Was steht in status und offene_aktion ?
  Stimmen Raum, Datum und Uhrzeit mit dem überein, was die Person gemeint hat? Was sagt euer
  Ergebnis über den Wert einer Bestätigung, die die Argumente anzeigt?

  .., "status": "wartet_auf_bestaetigung",..
  in offene_aktion stehen in JSON die argumente zum ausführen von raum_buchen

  Statt Lerngruppe Kim steht dort "Kim" ansonsten stimmen die Daten überein

  Antwort auf bestaetigen:
    → raum_buchen(uhrzeit='14:00', name='Kim', raum='O-108', datum='2026-11-05')  [wert]
    ← Fehler: O-108 ist am 2026-11-05 um 14:00 belegt (Tutorium). Freie Zeitfenster: 11:30, 15:45, 17:30.

  ```powershell
  docker compose run --rm app orchestrator.py --sitzung kim2 "Dann buch mir den Raum O-108 auf 15:00 Uhr, für die Lerngruppe Kim."
  docker compose run --rm app orchestrator.py --sitzung kim2 --ablehnen
  ```

  ### Was macht das Modell nach der Ablehnung?

  status wird als "fertig" eingetragen
  es gibt einen eintrag "fehler": "abgelehnt"
  und ein ergebnis: was erwähnt dass die Person abgelehnt hat.

```powershell
docker compose run --rm app orchestrator.py --sitzung kim3 "Buch mir den Raum O-108 für 15:45 Uhr, für die Lerngruppe Kim."
docker compose run --rm app orchestrator.py --sitzung kim3 --bestaetigen
docker compose run --rm app orchestrator.py --sitzung kim3 --bestaetigen
```
### 4.2.2 Warum wird nicht doppelt gebucht? Stellt euch vor, der Container stirbt genau während raum_buchen läuft. Welche Eigenschaft muss das Werkzeug dann haben, damit ein erneuter Versuch keinen Schaden anrichtet?

Sitzung kim3 wartet auf keine Bestätigung (Status: fertig).
"offene_aktion": null
Nach einer Bestätigung gilt ein Prozess als beendet.

Es soll eine eindeutige Anfrage-ID haben, die sich von der vorherigen unterscheidet, um durchmischen zu verhindern

### 4.2.4. Nennt zwei Situationen in einem echten Deployment, in denen die blockierende Variante aus Teil 2.3 scheitert und die Unterbrechung mit Checkpoint funktioniert.



| Aufgabe | Umsetzung |
|---|---|
| 4.1 | Sitzung speichern und laden, Checkpoints setzen und Folgefragen über Prozessgrenzen testen. |
| 4.2 | Vor Buchungen unterbrechen und später mit Zustimmung oder Ablehnung fortsetzen. |
| 4.3 | Langzeit-Memory ergänzen und Sitzungen mit und ohne Memory vergleichen. |
| 4.4 | Supervisor mit drei Spezialisten umsetzen, messen und eine Stelle verbessern. |

Für die Doku fehlen dann noch die Antworten zu Teil 4 und je zwei bis vier Sätze zu Frameworks, Memory Poisoning, Supervisoren, Bestätigungen, langen Verläufen und Kubernetes. Sitzungen und `memory.json` gehören nicht ins Repository.

