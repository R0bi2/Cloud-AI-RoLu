Aufgabe 1.1: 
(base) PS D:\Cloud_AI\Uebungen\Uebung_3_Starter\starter> docker compose run --rm app agent.py "Was gibt es heute in der Mensa?"                            
[+] Creating 2/2
 ✔ Container starter-campus-mcp-1  Running                                                           0.0s 
 ✔ Container starter-ollama-1      Running                                                           0.0s 
[+] Running 1/1
 ✔ Container starter-modell-laden-1  Started                                                         0.3s 
Werkzeuge: suche_wissen, lies_datei, heute, raeume_auflisten, raum_frei, mensa_speiseplan

  → mensa_speiseplan(datum='heute')  [wert]
  ← Fehler: 'heute' ist kein Datum im Format JJJJ-MM-TT.

Entschuldigung! Ich habe keine Informationen über den Speiseplan für heute. Dazu habe ich keine Information.

  1 Werkzeugaufrufe · 2 Modellaufrufe · 940 Eingabe-Tokens · 28.1 s · llama3.2:3b



(base) PS D:\Cloud_AI\Uebungen\Uebung_3_Starter\starter> docker compose run --rm app agent.py "Was gibt es heute in der Mensa?"
[+] Creating 2/2
 ✔ Container starter-ollama-1      Running                                                           0.0s 
 ✔ Container starter-campus-mcp-1  Running                                                           0.0s 
[+] Running 1/1
 ✔ Container starter-modell-laden-1  Started                                                         0.2s 
Werkzeuge: suche_wissen, lies_datei, heute, raeume_auflisten, raum_frei, mensa_speiseplan

  → mensa_speiseplan(datum='heute')  [wert]
  ← Fehler: 'heute' ist kein Datum im Format JJJJ-MM-TT.

Entschuldigung! Ich habe keine Informationen über den Speiseplan für heute. Dazu habe ich keine Information.

## kein Datum als eingabe. 

## Falsche Werte heute statt TT-MM-YYYY

                                                         docker compose run --rm app agent.py "Ich bin am Tag meiner Klausur krank. Was muss ich tun?"Eingabe-Tokens · 18.3 s · llama3.2:3b
>> se) PS D:\Cloud_AI\Uebungen\Uebung_3_Starter\starter> 
[+] Creating 2/2
 ✔ Container starter-campus-mcp-1  Running                                                           0.0s 
 ✔ Container starter-ollama-1      Running                                                           0.0s 
[+] Running 1/1
 ✔ Container starter-modell-laden-1  Started                                                         0.2s 
Werkzeuge: suche_wissen, lies_datei, heute, raeume_auflisten, raum_frei, mensa_speiseplan

  → suche_wissen(begriff='Klausur')
  ← pruefungsordnung.md (1 Treffer): § 9 Prüfungsformen. Prüfungen sind Klausuren, mündliche Prüfungen,

Wenn du am Tag deiner Klausur krank bist, solltest du dich von deinem Arzt beraten lassen und eine ärztliche Attestation erhalten. Dann kannst du die Klausur ablegen, wenn du eine ärztliche Attestation vorlegst.

  1 Werkzeugaufrufe · 2 Modellaufrufe · 969 Eingabe-Tokens · 25.5 s · llama3.2:3b

Tool aufruf korekt bekommenen infos lala
## Tool aufuf korrekt (evt. Ziel Verfehlt)




(base) PS D:\Cloud_AI\Uebungen\Uebung_3_Starter\starter> 
 docker compose run --rm app agent.py "Ist O-108 am Donnerstag um 14 Uhr frei?"
[+] Creating 2/2
 ✔ Container starter-campus-mcp-1  Running                                                           0.0s 
 ✔ Container starter-ollama-1      Running                                                           0.0s 
[+] Running 1/1
 ✔ Container starter-modell-laden-1  Started                                                         0.2s 
Werkzeuge: suche_wissen, lies_datei, heute, raeume_auflisten, raum_frei, mensa_speiseplan

  → raum_frei(raum='O-108', datum='2026-11-04')
  ← O-108 am 2026-11-04 (mittwoch): frei um 08:00, 09:45, 11:30, 15:45, 17:30. Belegt: 14:00 (Datenbanken).

O-108 ist am Donnerstag um 14 Uhr nicht frei.

  1 Werkzeugaufrufe · 2 Modellaufrufe · 998 Eingabe-Tokens · 15.7 s · llama3.2:3b

Tool aufruf korrekt aber mit den falschen werten.

## Ziel verfehlt 

Aufgabe 1.2:

Modell: llama3.2:3b · 13 Aufgaben

Variante                  Antwort  Werkz.  ungültig  Fehler  Abbruch  Aufrufe Ø  Tokens Ø  Dauer Ø
agent.v1.yaml               3/13    9/13          0       4        0        1.1       972    25.2s

Richtige Antworten nach Typ:
Variante                       datum      direkt      wissen mehrschritt  schreibend        ohne       fehlt
agent.v1.yaml                    1/4         1/1         1/4         0/1         0/1         0/1         0/1


Aufgabe 1.4:

✗ Buche mir O-108 am Freitag um 9:45 Uhr für die Lerngruppe  3 Aufrufe   43.6 s
  → raeume_auflisten()
  ← O-108: 24 Plätze, Gebäude O, Beamer, Whiteboard O-201: 40 Plätze, Gebäude O, Beamer, Steckdosen an jedem Platz F-012: 12 Plätze, Gebäude F, Erdgeschoss, großer …
  → raum_frei(raum='O-108', datum='2026-11-05T09:45:00')  [wert]
  ← Fehler: '2026-11-05T09:45:00' ist kein Datum im Format JJJJ-MM-TT.
  → mensa_speiseplan(datum='2026-11-05')
  ← Mensa am donnerstag, 2026-11-05: - Gemüsepfanne mit Tofu (vegan), 3,40 Euro - Fisch mit Salzkartoffeln, 3,40 Euro - Pizza Margherita, 3,40 Euro
    Antwort: Entschuldigung, ich habe keine Möglichkeit, eine Lerngruppe zu buchen.

Die ergebnisse der vorherigen tool aufrufe werden gemeinsam mit der ursprünglichen frage wieder in den Modellaufruf gegeben dadurch wächst der Kontext und damit auch die Tokens.


Aufgabe 1.5:
docker compose run --rm app agent.py "Buche mir O-108 am Freitag um 9:45 Uhr für die Lerngruppe" --max-schritte 1

  → raum_frei(raum='O-108', datum='2026-11-05')
  ← O-108 am 2026-11-05 (donnerstag): frei um 11:30, 15:45, 17:30. Belegt: 08:00 (Webapplikationen), 09:45 (Webapplikationen), 14:00 (Tutorium).

Abgebrochen nach 1 Modellaufrufen ohne Antwort.

  1 Werkzeugaufrufe · 1 Modellaufrufe · 739 Eingabe-Tokens · 19.6 s · llama3.2:3b

