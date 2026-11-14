# Übung 1 · Das Modell als Baustein

**Cloud-native AI · WS 2026/27 · Praktikumsabgabe P1**

- **Start:** Übung am Dienstag, 13.10.2026, 11:30, O/201
- **Abgabe:** Montag, 19.10.2026, 23:59, in Moodle
- **Arbeitsform:** einzeln oder zu zweit, wie in der Moodle-Gruppeneinteilung eingetragen
- **Aufwand:** etwa 6 Stunden für den Kern, dazu etwa 2 Stunden für den Zusatz

---

## Worum es geht

In dieser Übung legt ihr das Fundament für euer System im Praktikum: eine kleine Anwendung, die ein Sprachmodell aufruft, ohne zu wissen, welches. Das Modell steckt hinter einer Schnittstelle und wird nur über Konfiguration ausgewählt. Danach macht ihr sichtbar, was in VL 2 Theorie war: Wie stark streuen Antworten bei verschiedenen Temperaturen, was kostet Deutsch im Vergleich zu Englisch, und wie bringt ihr ein Modell dazu, verlässlich Daten statt Fließtext zu liefern?

Am Ende steht der erste Baustein des Campus-Assistenten: Er ordnet Mails von Studierenden strukturiert ein.

Grundlage sind die Skripte zu **VL 1** (Was ist Cloud-native AI?) und **VL 2** (Foundation Models verstehen).

| Teil | Inhalt | Aufwand | |
|---|---|---|---|
| **1** | Setup und erster Modellaufruf | ca. 1 h | Kern |
| **2** | Modell austauschen, nur über Konfiguration | ca. 45 min | Kern |
| **3** | Sampling und Tokens messen | ca. 1 h | Kern |
| **4** | Anfragen strukturiert einordnen | ca. 2,5 h | Kern |
| **5** | README mit Ergebnissen und Reflexion | ca. 45 min | Kern |
| **Z** | Zusatz: Ausgaben inhaltlich absichern | ca. 2 h | Zusatz |

Das Starter-Projekt liegt im Ordner `starter/`.

---

## Teil 1 · Setup und erster Modellaufruf (Kern)

1. **Docker** installieren, falls noch nicht vorhanden (Docker Desktop oder Docker Engine). Test: `docker run --rm hello-world`
2. Ein **eigenes Git-Repository** anlegen und das Starter-Projekt hineinkopieren. Bei Zweiergruppen arbeitet ihr in einem gemeinsamen Repository.
3. `.env.example` nach `.env` kopieren. Die Standardwerte nutzen das lokale Modell, ihr müsst nichts ändern.
4. Starten:

```bash
docker compose up --build app
```

Beim ersten Start lädt der Dienst `modell-laden` zwei Modelle herunter: `llama3.2:3b` (ca. 2 GB) und `qwen2.5:0.5b` (ca. 400 MB). Das dauert einmalig ein paar Minuten. Danach beantwortet die Anwendung eine Standardfrage und gibt Messwerte aus.

Eigene Frage stellen. Der Ordner `app/` ist in den Container eingebunden, Änderungen am Code wirken also sofort ohne neuen Build:

```bash
docker compose run --rm app hallo_llm.py "Wie melde ich mich zu einer Prüfung an?"
```

**Aufgaben:**

1. Lest `compose.yaml`, `app/llm.py` und `app/hallo_llm.py`. Beschreibt im README in drei, vier Sätzen: Welche Container laufen, und wie findet die Anwendung das Modell?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

In compose.yaml wird steht in zeile 2 ollama: mit image ollama/ollama:0.35.1 definiert
der container wird mit Host und entrypoint geladen
in Zeile 23 wird ein zweiter container "app: " definiert.

in llm.py in Zeile 13 wird 
MODEL = os.environ["LLM_MODEL"] gesetzt
"LLM_MODELL" wird dabei aus der .env geholt das gleiche mit der URL

</div>



2. Stellt drei verschiedene Fragen an den Campus-Assistenten. Notiert jeweils **Time to First Token** und **Gesamtdauer**.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">
Frage 1:
    "Wie Studenten gibt es an der HTGW?"
    Modell:              llama3.2:3b @ http://ollama:11434/v1
    Time to First Token: 128 ms
    Gesamtdauer:         9694 ms
    Zeichen Antwort:     538
<br><br>
Frage 2:
    "Wann wurde die HTWG gegründet?"
    Modell:              llama3.2:3b @ http://ollama:11434/v1
    Time to First Token: 566 ms
    Gesamtdauer:         5282 ms
    Zeichen Antwort:     242
<br><br>
Frage 3:
    "Ist blau eine Farbe?"
    Modell:              llama3.2:3b @ http://ollama:11434/v1
    Time to First Token: 384 ms
    Gesamtdauer:         2935 ms
    Zeichen Antwort:     122

</div>

## Teil 2 · Modell austauschen (Kern)

Ändert in `.env` nur die Zeile `LLM_MODEL` auf `qwen2.5:0.5b` und stellt dieselben drei Fragen noch einmal. **Am Code ändert ihr nichts.**

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">
Frage 1:
    "Wie viele Studenten gibt es an der HTGW?"
    Modell:              qwen2.5:0.5b @ http://ollama:11434/v1
    Time to First Token: 2265 ms
    Gesamtdauer:         9884 ms
    Zeichen Antwort:     1348
<br><br>
Frage 2:
    "Wann wurde die HTWG gegründet?"
    Modell:              qwen2.5:0.5b @ http://ollama:11434/v1
    Time to First Token: 1645 ms
    Gesamtdauer:         2064 ms
    Zeichen Antwort:     61
<br><br>
Frage 3:
    "Ist blau eine Farbe?"
    Modell:              qwen2.5:0.5b @ http://ollama:11434/v1
    Time to First Token: 139 ms
    Gesamtdauer:         290 ms
    Zeichen Antwort:     24
</div>
---


**Aufgaben:**

1. Füllt im README die Tabelle aus:

| Frage | Modell | TTFT (ms) | Gesamt (ms) | Antwort brauchbar? |
|---|---|---|---|---|
| "Wie viele Studenten gibt es an der HTGW?" | llama3.2:3b | 144 ms | 7575 ms | nein |
| "Wie viele Studenten gibt es an der HTGW?" | qwen2.5:0.5b | 134 ms | 425 ms | nein |

2. Fragt beide Modelle: „Ist die HTWG Konstanz eine private oder eine staatliche Hochschule?“ Was fällt euch auf?
<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">
A: Die Antwort ist in beiden fällen knapp gefasst und klar formuliert. llama3.2 sagt richtig aus, es ist eine staatliche Hochschule, auch bei mehrmaligem Fragen. qwen2.5 ebenfalls.
llama 3.2
Time to First Token: 588 ms
Gesamtdauer:         2511 ms

qwen 2.5
Time to First Token: 97 ms
Gesamtdauer:         395 ms
</div>
**Optional, wenn die Academic Cloud erreichbar ist:** Mit einem API-Key über [KISSKI](https://kisski.gwdg.de/en/leistungen/2-02-llm-service/) tragt ihr Variante B aus `.env.example` ein und nutzt `qwen3-30b-a3b-instruct-2507` als drittes Modell im Vergleich. Wer keinen Key hat oder wenn der Dienst nicht läuft, verliert dadurch nichts. Alle Teile funktionieren komplett lokal.

---

## Teil 3 · Sampling und Tokens messen (Kern)

Stellt `LLM_MODEL` zurück auf `llama3.2:3b`.

### Sampling

```bash
docker compose run --rm app sampling.py
```

Das Skript stellt dieselbe Frage je fünfmal bei Temperature 0, 0,7 und 1,2 und zählt die verschiedenen Antworten.

1. Wie viele verschiedene Antworten bekommt ihr bei jeder Temperature?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">
Temperature 0: 1x verschiedene (Sonnenblume)
<br>
Temperature 0.7: 5x verschiedene (4 davon im Zusammenhang mit "Sonne" )
<br>
Temperature 1.2 5x verschiedene (verschiedene Kontexte, teilweise unkorrekte Grammatik)
</div>

2. Liefert Temperature 0 wirklich fünfmal dieselbe Antwort? Wenn nicht: Woran könnte das liegen? (Skript VL 2, Abschnitt „Inkonsistenz)
<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">
Auch bei mehrfacher Ausführung liefert es 5x die gleiche Antwort
</div>

3. Startet das Skript mit einer Faktenfrage, z. B. `docker compose run --rm app sampling.py "Ist die HTWG Konstanz eine private oder staatliche Hochschule? Antworte mit einem Satz."`. Achtet nicht nur auf „privat oder staatlich“, sondern auf jedes Detail, etwa wofür die Abkürzung HTWG steht. Welche Fehler kommen schon bei Temperature 0 vor, welche erst bei höheren Werten? Was sagt das über die Ursache (Sampling oder Trainingsdaten)?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

    Bei Temperatur 0 bleibt die Antwort 5x gleich. Es wird richtigerweise gesagt die HTWG sei eine staatliche hochschule. Es fehlt in der Ausformulierung von HTWG das "und Gestaltung"
  
    Bei Temperatur 0.7 Gibt es 3 unterschiedliche Antworten.
    staatlich bleibt korrekt.
    Er lässt er die Ausschreibung entweder ganz aus, vergisst wieder das "und Gestaltung", oder erfindet eine Ausschreibung (Technologie statt Technik).

    Bei Temperatur 1.2 gibt es 5x verschiedene Antworten
    staatlich ist korrekt.
    Er denkt sich die Ausschreibung jedes mal (-falsch-) neu aus

    Es sagt aus das kreativeres sampling fehlende Trainingsdaten nicht ersetzen kann.
    Man sollte Temperatur nur bei nicht Fakten erhöhen können
</div>

### Tokens

```bash
docker compose run --rm app tokens.py
```

1. Wie viele Tokens braucht der deutsche Text, wie viele der englische? Um wie viel Prozent ist Deutsch teurer?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">
    Modell: llama3.2:3b
    Deutsch    63 Tokens für 21 Wörter
    Englisch   49 Tokens für 21 Wörter

    Deutsch braucht 14 Tokens mehr (+29%).

    Wir vermuten im englischen prompt ist das sampling zielgerichteter weil z.B. erst mathematics als wort fällt ausserdem ist es naheliegend dass deutsche Wörter in mehr Tokens aufgeteilt sind

    registration + deadline < |Anmelde|frist|
</div>
<br>
2. Ersetzt in `tokens.py` die Texte durch eine eigene Frage mit langen zusammengesetzten Wörtern (z. B. „Prüfungsanmeldungsfrist“). Wird der Unterschied größer?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">
Modell: llama3.2:3b

Deutsch    75 Tokens für 21 Wörter
Englisch   49 Tokens für 21 Wörter

Deutsch braucht 26 Tokens mehr (+53%).
<br><br><br>
Modell: llama3.2:3b

Deutsch    81 Tokens für 23 Wörter
Englisch   49 Tokens für 21 Wörter

Deutsch braucht 32 Tokens mehr (+65%).

mit längeren wörtern verdoppelt sich der Token Mehraufwand schon. Mit zusätzlichen Wörtern noch stärker.
</div>

---

## Teil 4 · Anfragen strukturiert einordnen (Kern)

Der Campus-Assistent soll jede Mail zuerst einordnen: Um welches **Anliegen** geht es (Prüfung, Mensa, Bibliothek, Sonstiges), welcher **Studiengang**, welche **Frist**? Das Ergebnis verarbeitet ein Programm weiter. Es muss also immer dieselbe Form haben.

Öffnet `app/einordnen.py`. Die Klasse `Anfrage` und die Hilfsfunktion `schema_von` sind vorgegeben. Eure Aufgaben stehen an den `TODO`-Kommentaren:

1. **TODO 1:** Ruft das Modell mit `response_format=schema_von(Anfrage)` auf. Wählt eine passende Temperature und begründet sie im Code mit einem Kommentar.
2. **TODO 2:** Prüft die Antwort mit `Anfrage.model_validate_json(...)`.
3. **TODO 3:** Ist die Antwort ungültig, versucht es erneut, höchstens dreimal. Danach soll das Programm mit einem klaren Fehler abbrechen, statt mit kaputten Daten weiterzuarbeiten.
4. **TODO 4:** Wertet alle Test-Mails aus `mails.json` aus und zählt, wie viele Anliegen richtig erkannt sind.

```bash
docker compose run --rm app einordnen.py
docker compose run --rm app einordnen.py "Eure eigene Mail"
```

**Aufgaben zur Auswertung:**

1. Wie viele der acht Mails ordnen `llama3.2:3b` und `qwen2.5:0.5b` jeweils richtig ein?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Modell: llama3.2:3b<br>
7 von 8 Anliegen richtig (87,5 %).
<br><br>
Modell: qwen2.5:0.5b<br>
2 von 8 Anliegen richtig (25 %).
<br><br>
Hier wird erstmal nur das Anliegen verglichen, nicht Studiengang und Frist.

</div>

2. Schaut euch die Fehler an. Ist das Anliegen falsch, oder stimmen Studiengang und Frist nicht?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Bei llama3.2 ist in Mail 7 das Anliegen falsch. Es wird als Prüfung eingeordnet,
obwohl es um den Zugang zu IEEE Xplore über die Bibliothek geht.
<br><br>
Die anderen Anliegen stimmen. Trotzdem sind nicht alle Felder richtig:
Bei Mail 4 und 8 steht "null" als Text und bei Mail 5 wird eine Frist erfunden.
<br><br>
qwen2.5 ordnet jede Mail als Prüfung ein. Deshalb sind nur Mail 1 und 5 beim
Anliegen richtig. Bei Mail 1 wird aber "3. Semester" als Frist ausgegeben,
bei Mail 5 steht AIN statt MSI. Auch bei den anderen Mails wird häufig AIN
ausgegeben oder ein Jahr zur Frist ergänzt, das gar nicht in der Mail steht.

</div>

3. Schaut auch bei den „richtigen“ Fällen genau hin: Steht bei `studiengang` manchmal der **Text** `"null"` statt eines echten leeren Werts? Nennt das Modell eine **Frist, die gar nicht in der Mail steht**? Warum lässt das Schema beides durch?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Ja. llama3.2 gibt bei Mail 4 und 8 für Studiengang und Frist den Text "null" aus.
Das ist ein String und nicht der leere Wert null.
Bei Mail 5 wird "bis zum 15.04.2024" als Frist genannt, obwohl keine Frist
in der Mail steht.
<br><br>
Bei qwen2.5 steht z.B. in Mail 3 "30.10.2023", obwohl nur "30.10." vorgegeben ist.
<br><br>
Das Schema erlaubt für studiengang und frist einen String oder null.
"null" ist auch ein gültiger String. Ob eine Frist wirklich in der Mail steht
und ob ein Studiengang stimmt, wird dabei nicht geprüft.

</div>

4. Die letzte Mail in `mails.json` versucht, das Modell umzulenken. Was passiert? (Darum geht es in VL 3.)

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

llama3.2 bleibt bei der Einordnung und gibt sonstiges aus.
studiengang und frist werden aber wieder als Text "null" ausgegeben.
<br><br>
qwen2.5 gibt ebenfalls eine JSON-Antwort aus, ordnet die Mail aber als Prüfung
ein und setzt AIN als Studiengang.
<br><br>
Keines der beiden Modelle schreibt in diesem Durchlauf das verlangte Gedicht.
Die Umlenkung hat hier also nicht zum Gedicht geführt, trotzdem ist die
inhaltliche Einordnung bei qwen falsch. Ein einzelner Test zeigt nicht,
dass solche Umlenkungsversuche grundsätzlich abgefangen werden.

</div>

5. Entfernt testweise `response_format` und verlasst euch nur auf den System-Prompt. Gebt die Rohantwort des Modells mit `print` aus. Was geht schief? Warum bringt euer erneuter Versuch bei Temperature 0 nichts, und was könntet ihr ändern? Stellt `response_format` danach wieder her.

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Getestet wurde mit der eigenen Mail:
"Ich studiere AIN und möchte mich bis 20.10. von einer Prüfung abmelden."
<br><br>
Ohne response_format geben beide Modelle die Antwort in einem Markdown-Codeblock
aus. Pydantic erwartet direkt JSON und kann das so nicht einlesen.
llama3.2 schreibt außerdem "prüfung" statt "pruefung" und "studienengang"
statt "studiengang". qwen2.5 verwendet andere Felder wie "status" und "antwort"
und ergänzt bei der Frist wieder das Jahr 2023.
<br><br>
Bei Temperature 0 kommt bei allen drei Versuchen je Modell dieselbe falsche
Antwort zurück. Nur die gleiche Anfrage zu wiederholen behebt den Fehler hier nicht.
Man könnte den Prompt genauer machen oder beim nächsten Versuch den
Validierungsfehler mitgeben. Eine höhere Temperature könnte die Antwort ändern,
garantiert aber keine richtige Struktur.
<br><br>
Mit Schema wird die eigene Mail als pruefung, AIN und 20.10. erkannt
(getestet mit llama3.2). response_format ist im Code wieder eingeschaltet.

</div>


---

## Teil 5 · README (Kern)

4. **Reflexion**, je zwei bis vier Sätze:
    1. Warum steht das Modell in `.env` und nicht im Code?

        <div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

        So können wir das Modell wechseln, ohne den Code zu ändern.
        Es wird nur LLM_MODEL in der .env angepasst. Auch URL und API-Key lassen sich
        dadurch passend zum verwendeten Dienst einstellen.

        </div>

    2. Welche Temperature habt ihr in `einordnen.py` gewählt, und warum?

        <div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

        Wir verwenden Temperature 0. Bei der Einordnung brauchen wir keine kreativen
        Antworten, sondern möglichst wenig Streuung bei den gleichen Eingaben.
        Das macht die Antworten aber nicht automatisch inhaltlich richtig.

        </div>

    3. Was garantiert `response_format` mit Schema, und was nicht?

        <div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

        Das Schema gibt die JSON-Struktur, die Feldtypen und die erlaubten Anliegen vor.
        Die erhaltene Antwort wird zusätzlich mit Pydantic geprüft.
        Ob die Inhalte stimmen, ist damit nicht garantiert: "null" als Text oder eine
        erfundene Frist sind als String trotzdem erlaubt.

        </div>

    4. Wann würdet ihr ein lokales Modell, wann einen Cloud-Dienst wählen? Nennt je zwei Gründe.

        <div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

        Ein lokales Modell würden wir nehmen, wenn die Mails nicht an einen externen
        Modelldienst übertragen werden sollen und wir nach dem Download unabhängig
        von dessen Verfügbarkeit arbeiten möchten.
        <br><br>
        Einen Cloud-Dienst würden wir nehmen, wenn wir ein leistungsfähigeres Modell
        benötigen oder die eigene Hardware für das gewünschte Modell nicht ausreicht.

        </div>


---

## Zusatz · Ausgaben inhaltlich absichern

Dieser Teil **entfällt**, wenn ihr am Semesterende mindestens 80 % Anwesenheit nachweist. Wer nicht sicher ist, gibt ihn mit ab. Zusatzteile sind nicht nachreichbar.

Das Schema garantiert die Form, nicht den Inhalt. In Teil 4 habt ihr gesehen, dass das Modell trotzdem `"null"` als Text schreibt oder Fristen erfindet. Fangt das ab:

1. Ergänzt `Anfrage` um **Pydantic-Validatoren** (`field_validator`):
    - Der Text `"null"`, `"None"` oder eine leere Zeichenkette wird zu einem echten `None`.
    - `studiengang` ist nur gültig, wenn es ein Kürzel aus einer festen Liste ist (z. B. AIN, WIN, MSI, und weitere, die ihr für sinnvoll haltet). Alles andere wird zu `None`.
2. Prüft **im Code, nicht im Modell**, ob die erkannte Frist tatsächlich in der Mail vorkommt. Findet ihr sie nicht, setzt ihr sie auf `None` und gebt eine Warnung aus.
3. Messt die Wirkung: Wie viele der acht Mails haben vorher und nachher **alle drei Felder** richtig? Anliegen und Studiengang vergleicht ihr exakt. Eine Frist zählt als richtig, wenn die erwartete Frist im Ergebnis enthalten ist, „Freitag, 16.10.“ passt also zu „16.10.“. Tragt beide Zahlen ins README ein.

---

## Was ihr abgebt

**In Moodle**, Aufgabe „Übung 1 (P1)“: den **Link zu eurem Repository** und den Commit-Hash eures Abgabestands. Das Repository muss für mich lesbar sein: öffentlich, oder ihr ladet meinen GitHub-Account `PascalLaube` als Collaborator ein.

**Harte Kriterien**, ohne die die Abgabe nicht bestanden ist:

- [ ] Das System startet mit `docker compose up --build app` nach einer im README beschriebenen `.env`.
- [ ] Keine Secrets im Repository. `.env` steht in `.gitignore` und ist nicht committet. Prüft es mit `git status`.
- [ ] Abhängigkeiten sind gepinnt (`requirements.txt` mit festen Versionen, feste Image-Tags).
- [ ] `einordnen.py` läuft durch und gibt die Trefferquote aus.
- [ ] Das README enthält alle Punkte aus Teil 5.
- [ ] Wer unter 80 % Anwesenheit landen könnte: Zusatzteil im README dokumentiert.

---

## Tipps

- **Modelle vorab laden:** Die Modelle sind zusammen etwa 2,4 GB groß. Startet `docker compose up --build app` am besten schon **vor der Übung** zu Hause, sonst teilen sich alle im Raum das WLAN. `docker compose logs modell-laden` zeigt den Fortschritt.
- **Hohe TTFT direkt nach einem Modellwechsel?** Ollama lädt das Modell beim ersten Aufruf in den Speicher. Messt deshalb erst ab dem zweiten Aufruf.
- **Wenig Speicher auf dem Laptop?** Arbeitet mit `qwen2.5:0.5b` und gebt `llama3.2:3b` an, wo ihr es nicht ausführen konntet. Schreibt das ins README.
- **Kein Docker möglich?** Meldet euch bis Donnerstag per Mail, dann finden wir eine Lösung.
- **KI-Werkzeuge** dürft ihr nutzen. Ihr müsst jede Zeile eures Codes erklären können.
