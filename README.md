# Cloud-AI-RoLu – Übung 1 / P1

## Namen und Matrikelnummern

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Luis Zink<br>
Robert

</div>

## Start und Container

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Docker Desktop muss laufen. Im Ordner starter einmalig .env.example nach .env
kopieren, falls die Datei noch nicht vorhanden ist.
<br><br>
In der .env steht für die lokale Ausführung:<br>
LLM_BASE_URL=http://ollama:11434/v1<br>
LLM_MODEL=llama3.2:3b<br>
LLM_API_KEY=nicht-noetig
<br><br>
Start im Ordner starter:<br>
docker compose up --build app
<br><br>
Ollama stellt die Modell-API bereit. modell-laden lädt die beiden Modelle
in ein dauerhaftes Volume und beendet sich danach.
Der app-Container führt das Python-Skript aus und erreicht das Modell über
ollama:11434/v1. Welches Modell verwendet wird, kommt aus der .env.

</div>

## Teil 1 · Erster Modellaufruf

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

## Teil 2 · Modell austauschen

In .env wird nur LLM_MODEL auf qwen2.5:0.5b geändert. Am Code wird nichts geändert.

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

Zusätzlich notierter Vergleich:

| Frage | Modell | TTFT (ms) | Gesamt (ms) | Antwort brauchbar? |
|---|---|---|---|---|
| "Wie viele Studenten gibt es an der HTGW?" | llama3.2:3b | 144 ms | 7575 ms | nein |
| "Wie viele Studenten gibt es an der HTGW?" | qwen2.5:0.5b | 134 ms | 425 ms | nein |

### Ist die HTWG Konstanz eine private oder eine staatliche Hochschule?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">
A: Die Antwort ist in beiden fällen knapp gefasst und klar formuliert. llama3.2 sagt richtig aus, es ist eine staatliche Hochschule, auch bei mehrmaligem Fragen. qwen2.5 ebenfalls.
llama 3.2
Time to First Token: 588 ms
Gesamtdauer:         2511 ms

qwen 2.5
Time to First Token: 97 ms
Gesamtdauer:         395 ms
</div>

## Teil 3 · Sampling und Tokens

LLM_MODEL ist wieder auf llama3.2:3b gesetzt.

### Wie viele verschiedene Antworten bekommt ihr bei jeder Temperature?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">
Temperature 0: 1x verschiedene (Sonnenblume)
<br>
Temperature 0.7: 5x verschiedene (4 davon im Zusammenhang mit "Sonne" )
<br>
Temperature 1.2 5x verschiedene (verschiedene Kontexte, teilweise unkorrekte Grammatik)
</div>

### Liefert Temperature 0 wirklich fünfmal dieselbe Antwort?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">
Auch bei mehrfacher Ausführung liefert es 5x die gleiche Antwort
</div>

### Faktenfrage: Welche Fehler kommen vor?

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

### Wie viele Tokens braucht der deutsche Text, wie viele der englische?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">
    Modell: llama3.2:3b
    Deutsch    63 Tokens für 21 Wörter
    Englisch   49 Tokens für 21 Wörter

    Deutsch braucht 14 Tokens mehr (+29%).

    Die Eingabetokens hängen vom Text und Tokenizer ab. Deutsche Wörter können dabei in mehr Tokens aufgeteilt sein. Das Sampling beeinflusst die Anzahl der Eingabetokens nicht.


</div>

### Eigene Frage mit langen zusammengesetzten Wörtern

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

## Teil 4 · Anfragen strukturiert einordnen

### Wie viele der acht Mails werden richtig eingeordnet?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Modell: llama3.2:3b<br>
7 von 8 Anliegen richtig (87,5 %).
<br><br>
Modell: qwen2.5:0.5b<br>
2 von 8 Anliegen richtig (25 %).
<br><br>
Hier wird erstmal nur das Anliegen verglichen, nicht Studiengang und Frist.

</div>

### Ist das Anliegen falsch, oder stimmen Studiengang und Frist nicht?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Bei llama3.2 ist in Mail 7 das Anliegen falsch. Es wird als Prüfung eingeordnet,
obwohl es um den Zugang zur Bibliothek geht.
<br><br>
Die anderen Anliegen stimmen. Trotzdem sind nicht alle Felder richtig:
Bei Mail 4 und 8 steht "null" als Text und bei Mail 5 wird eine Frist erfunden.
<br><br>
qwen2.5 ordnet jede Mail als Prüfung ein. Deshalb sind nur Mail 1 und 5 beim
Anliegen richtig. Bei Mail 1 wird aber "3. Semester" als Frist ausgegeben,
bei Mail 5 steht AIN statt MSI. Auch bei den anderen Mails wird häufig AIN
ausgegeben oder ein Jahr zur Frist ergänzt, das gar nicht in der Mail steht.

</div>

### Text "null" und erfundene Fristen

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

### Was passiert beim Umlenkungsversuch in der letzten Mail?

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

### Was geht ohne response_format schief?

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

## Reflexion

### Warum steht das Modell in .env und nicht im Code?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

So können wir das Modell wechseln, ohne den Code zu ändern.
Es wird nur LLM_MODEL in der .env angepasst. Auch URL und API-Key lassen sich
dadurch passend zum verwendeten Dienst einstellen.

</div>

### Welche Temperature haben wir gewählt, und warum?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Wir verwenden Temperature 0. Bei der Einordnung brauchen wir keine kreativen
Antworten, sondern möglichst wenig Streuung bei den gleichen Eingaben.
Das macht die Antworten aber nicht automatisch inhaltlich richtig.

</div>

### Was garantiert response_format mit Schema, und was nicht?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Das Schema gibt die JSON-Struktur, die Feldtypen und die erlaubten Anliegen vor.
Die erhaltene Antwort wird zusätzlich mit Pydantic geprüft.
Ob die Inhalte stimmen, ist damit nicht garantiert: "null" als Text oder eine
erfundene Frist sind als String trotzdem erlaubt.

</div>

### Wann würden wir ein lokales Modell, wann einen Cloud-Dienst wählen?

<div style="border: 2px solid green; padding: 12px; border-radius: 6px;">

Ein lokales Modell würden wir nehmen, wenn die Mails nicht an einen externen
Modelldienst übertragen werden sollen und wir nach dem Download unabhängig
von dessen Verfügbarkeit arbeiten möchten.
<br><br>
Einen Cloud-Dienst würden wir nehmen, wenn wir ein leistungsfähigeres Modell
benötigen oder die eigene Hardware für das gewünschte Modell nicht ausreicht.

</div>
