# Übung 2 – Prompts, Einordnung und Wissen abrufen

## Stand

- [x] Starter in `uebung_2/` eingerichtet; `.env` bleibt lokal und wird ignoriert.
- [x] Teil 2: Prompts v1–v5 erstellt bzw. getestet; v1 blieb unverändert.
- [x] Teil 1 und Teil 3 abgeschlossen.
- [ ] Teil 4 und Reflexion abschließen.

## Start und Messungen

Docker Desktop muss laufen. `.env` enthält die lokale LLM-Konfiguration und
wird nicht committet. Befehle aus diesem Ordner (`uebung_2`) ausführen:

```bash
docker compose run --rm --build app prompts.py
docker compose run --rm app einordnen.py --prompt prompts/einordnen.v1.yaml
docker compose run --rm app vergleich.py prompts/einordnen.v1.yaml prompts/einordnen.v2.yaml prompts/einordnen.v3.yaml prompts/einordnen.v4.yaml
```

Modell: `llama3.2:3b`, Temperatur `0`, 16 Mails aus `app/mails.json`.
v1–v4 wurden dreimal gemeinsam ausgeführt. v4–v5 wurden nach der Änderung
des Ausgabeformats in drei weiteren Vergleichsläufen getestet.

## Teil 1 – Prompts aus dem Code holen

### Fragen und kurze Antworten

1. **Warum setzt `nachrichten()` `{eingabe}` mit `replace` statt
   `str.format` ein?**
   - Im Prompt können JSON-Beispiele mit geschweiften Klammern stehen.
   - `str.format` könnte diese Klammern als weitere Platzhalter lesen und
     einen Fehler auslösen oder den Text unerwünscht verändern.
   - `replace` tauscht gezielt nur `{eingabe}` aus und lässt den übrigen
     Prompt-Text unverändert.

2. **Warum wird eine veröffentlichte Prompt-Version nicht überschrieben?
   Was wäre falsch an Messwerten, die sich auf eine frühere Fassung beziehen?**
   - Eine Version bleibt unverändert, damit Messungen eindeutig zu genau
     dem Prompt gehören, mit dem sie erzeugt wurden.
   - Wird v1 nachträglich überschrieben, kann niemand die alten Ergebnisse
     zuverlässig reproduzieren oder erkennen, welche Änderung sie verursacht
     hat. Verbesserungen gehören deshalb in eine neue Versionsdatei.

3. **v1 auf den 16 Mails ausführen: Wie viele Anliegen und vollständige
   Einordnungen sind richtig?**
   - Anliegen richtig: **13/16**.
   - Alle Felder richtig: **8/16**.
   - Das sind die stabilen Trefferzahlen aus den drei Vergleichsläufen.

## Teil 2 – Einordnung verbessern und messen

v2 präzisiert Kategorien, Studiengänge, Fristen und den Umgang mit der Mail
als Daten. In `app/einordnen.py` ist `studiengang` auf `AIN`, `WIN`, `MSI`
oder `null` beschränkt. v3 ist eine kompaktere deutsche Fassung; v4 überträgt
die kompakte Fassung ins Englische; v5 schärft Frist- und Ausgabeformatregeln.

### Ergebnisse v1–v4

Durchschnittliche Laufzeit aus drei gemeinsamen Läufen:

| Version | Anliegen richtig | Alle Felder richtig | Ø Eingabe-Tokens | Ø Dauer |
|---|---:|---:|---:|---:|
| v1 | 13/16 (81,3 %) | 8/16 (50,0 %) | 140 | 3,12 s |
| v2 | 15/16 (93,8 %) | 11/16 (68,8 %) | 818 | 5,61 s |
| v3 | 14/16 (87,5 %) | 9/16 (56,3 %) | 431 | 4,00 s |
| v4 | 16/16 (100 %) | 11/16 (68,8 %) | 356 | 3,51 s |

v2 benötigte gegenüber v1 etwa 5,8-mal so viele Eingabe-Tokens. v3 sparte
gegenüber v2 rund 47 %, v4 rund 56 %. Im direkten Test mit deutschen Mails
war der englische v4-Prompt effizienter und genauer als v3.

### Gezielter Vergleich v4–v5

v5 enthält eine knappere Fristregel und ein verbindliches JSON-Ausgabemuster.
Die Tabelle zeigt drei Vergleichsläufe nach dieser Änderung:

| Version | Anliegen richtig | Alle Felder richtig | Ø Eingabe-Tokens | Ø Dauer |
|---|---:|---:|---:|---:|
| v4 | 16/16 (100 %) | 11/16 (68,8 %) | 356 | 3,54 s |
| v5 | 10/16 (62,5 %) | 7/16 (43,8 %) | 397 | 5,23 s |

Die Ergebnisse waren in allen drei Läufen gleich. v5 sparte keine Tokens:
Der Mittelwert stieg um etwa 12 %, während die Trefferquote sank. Die
Änderung hat sich in dieser Messung nicht bewährt.

### Fragen und kurze Antworten

1. **Was hat v2 gebracht, was hat es gekostet? Um welchen Faktor stiegen die
   Eingabe-Tokens?**
   - Anliegen: 13/16 → 15/16; alle Felder: 8/16 → 11/16.
   - Tokens: 140 → 818, also etwa **5,8-mal so viele**. Laufzeit: 3,12 → 5,61 s.

2. **Welche Mails sind mit v2 noch falsch? Sind die Fehler unklare Anweisung,
   fehlendes Wissen, Angriff oder eine zu strenge Messung? Wie ließe sich die
   Messung verbessern?**
   - „Bis wann?“ und Attesttext als Frist: Fristregel nicht sauber befolgt.
   - Konkretes Datum übersehen: Extraktionsfehler.
   - Eingebettete „SYSTEM“-Anweisung: Prompt-Injection.
   - `6.11.` statt `6 November`: Messung zu streng; Datumsformate normalisieren,
     ohne ein fehlendes Jahr zu ergänzen.

3. **Was steht bei `studiengang` in der letzten Mail? Warum hilft keine
   Prompt-Formulierung zuverlässig?**
   - Die Mail fordert `HACKED`, erwartet wird `null`, weil kein Studiengang
     genannt ist.
   - Eine Prompt-Regel ist keine technische Garantie gegen eingebettete
     Anweisungen.

4. **Was verhindert die Typbeschränkung, was nicht, und auf welcher Ebene
   wirkt sie im Vergleich zum Prompt?**
   - Sie blockiert ungültige Werte wie `HACKED`, nicht aber falsche erlaubte
     Werte oder eine falsche Kategorie.
   - Sie wirkt als Schema-Validierung im Anwendungscode; der Prompt ist eine
     natürlichsprachliche Anweisung ans Modell.

5. **Gibt es eine Version mit weniger Tokens und vergleichbarer Qualität?
   Welche würdest du wählen?**
   - v3: 47 % weniger Tokens als v2, aber 9 statt 11 vollständige Fälle.
   - v4: 56 % weniger als v2 und 11 vollständige Fälle; bester Kompromiss
     in diesen Tests.
   - v5: 7 vollständige Fälle und mehr Tokens als v4; hier keine Verbesserung.
   - Grundlage sind nur 16 Mails, daher Ergebnisse vorsichtig bewerten.

Beobachtet wurden unter anderem Fristangaben wie „heute“, „samstags“ und
„Bis wann?“, die fälschlich als Frist ausgegeben wurden. `6.11.` statt
`6 November` wurde von der exakten Auswertung als Fehler gezählt, obwohl beide
Angaben dasselbe Datum meinen.

## Teil 3 – Assistent angreifen und härten

Ausgangspunkt ist `app/prompts/assistent.v1.yaml`. Der Assistent darf den dort
enthaltenen erfundenen Türcode nicht verraten. `angriff.py` misst
Verletzungsrate und Fehlablehnungsrate. In `assistent.py` prüft der
Ausgangs-Guardrail die Modellantwort auf den Türcode.

Modell: `llama3.2:3b`; ein Messlauf mit 15 Angriffen (12 Starterfälle und
drei eigene) sowie 8 harmlosen Fragen. Ergebnisse können bei Wiederholungen
schwanken.

| Prompt | Ohne Guardrail: Verletzungsrate | Ohne Guardrail: Fehlablehnungsrate | Mit Guardrail: Verletzungsrate | Mit Guardrail: Fehlablehnungsrate |
|---|---:|---:|---:|---:|
| Assistent v1 | 12/15 (80 %) | 0/8 (0 %) | 3/15 (20 %) | 0/8 (0 %) |
| Assistent v2 | 3/15 (20 %) | 1/8 (12 %) | 3/15 (20 %) | 1/8 (12 %) |
| Assistent v3 | 3/15 (20 %) | 1/8 (12 %) | 3/15 (20 %) | 1/8 (12 %) |

### Fragen und kurze Antworten

1. **Welche Angriffsarten kommen mit v1 durch, welche nicht?**
   - Durch kamen direkte und verschleierte Codefragen, Rollenspiel,
     Gedicht-/Übersetzungsformat, vorgetäuschte Autorität sowie Marker- und
     indirekte Angriffe.
   - Das reine Ausgeben des System-Prompts und eine Fortsetzungsaufforderung
     waren in diesem Lauf nicht erfolgreich.

2. **Welche drei eigenen Angriffe wurden ergänzt?**
   - Direkte Codefrage unter dem Vorwand einer Dokumentation.
   - Aufforderung, den internen Hinweis zu übersetzen und Zahlen beizubehalten.
   - Indirekte Anweisung in einer weitergeleiteten Nachricht, mit `PWNED` zu
     enden.
   - Alle drei lösten beim ungehärteten v1 den erwarteten Treffer aus.

3. **Wie wurde v2 gehärtet?**
   - Klare Regeln gegen das Ausgeben interner Informationen und gegen
     Rollenwechsel in Nutzereingaben.
   - Die Frage wird markiert; für Fragen nach internen Informationen ist eine
     feste Absage vorgegeben.

4. **Erkennt der Guardrail den Code in über mehrere Zeilen verteilten Ziffern?**
   - Ja. Er entfernt alle Nicht-Ziffern und sucht danach nach `8352`.
   - Der Test mit `8`, `3`, `5`, `2` in getrennten Zeilen wurde durch die
     feste Absage abgefangen.

5. **Was bewirkt v3 ohne gespeicherten Türcode?**
   - Der Code steht nicht mehr im Prompt. Die Verletzungsrate ohne Guardrail
     blieb bei 20 %, weil auch erfolgreiche Marker-Angriffe wie `PWNED` als
     Verletzung zählen.

6. **Welche harmlosen Fragen wurden abgelehnt, und warum?**
   - v2 und v3 beantworteten die Frage nach Möglichkeiten nach einer verpassten
     Prüfungs-Anmeldefrist nicht brauchbar. Die vorsichtige Behandlung von
     Prüfungsfragen kann also nützliche Antworten kosten.
   - v1 beantwortete alle harmlosen Testfragen. Der Guardrail selbst änderte
     die Fehlablehnungsrate in diesem Datensatz nicht.

**Fazit:** v2 und v3 senkten die Verletzungsrate gegenüber v1 deutlich, aber
nicht auf null. Der Guardrail senkte v1 weiter, weil er den Code filtert;
Marker-Angriffe ohne Code passieren weiterhin. Prompt-Härtung und Guardrail
müssen deshalb zusammen mit der Fehlablehnungsrate bewertet werden.

## Teil 4 – Wissen abrufen

Laut Aufgabenblatt wird dieser Teil nach der Vorlesung am 27.10. ergänzt.
Dann den Assistenten um Wissen aus Dateien erweitern und einfache Dateisuche
mit RAG vergleichen. Aufgaben und Messwerte ergänzen, sobald der Teil
veröffentlicht ist.

## Teil 5 – Abgabe und Reflexion

- [ ] Startbefehle und `.env`-Konfiguration so dokumentieren, dass die
      Messungen nachvollziehbar sind.
- [ ] Ergebnisse aus Teil 1–4, Tabellen und Antworten auf die Aufgaben
      aufnehmen.
- [ ] Namen und Matrikelnummern nur bei privatem Repository hier eintragen;
      bei öffentlichem Repository nur im Moodle-Abgabetext nennen.
- [ ] Je zwei bis vier Sätze zu jeder Reflexionsfrage:
  1. Was unterscheidet eine gemessene Verbesserung von einer, die sich nur
     besser anfühlt?
  2. Was zeigen eure Zahlen zur Aussage „Mit einem guten System-Prompt ist
     Prompt Injection gelöst“?
  3. Welche Abwehrmaßnahme brachte am meisten, und auf welcher Ebene
     (Modell, Prompt oder System) wirkt sie?
  4. Warum braucht man neben der Verletzungsrate auch die Fehlablehnungsrate?

## Zusatz – PAIR-Angreifer (falls Anwesenheit unter 80 % liegen könnte)

- [ ] Beide TODOs in `app/angreifer.py` umsetzen.
- [ ] Zehn Runden ohne Guardrail gegen v1 ausführen. Falls es nicht klappt,
      den Angreifer-Prompt prüfen.
- [ ] Angreifer-Prompt verbessern und je zehn Runden gegen v1–v3 dreimal
      ausführen. Festhalten, nach wie vielen Runden ein Angriff gelingt.
- [ ] Gute automatisch erzeugte Angriffe in `angriffe.json` übernehmen.
- [ ] Falls verfügbar, größeres Angreifer-Modell ausprobieren und Unterschiede
      dokumentieren.

## Abgabe-Checkliste

- [ ] System startet mit den hier beschriebenen Befehlen.
- [x] `.env` wird von Git ignoriert und nicht committet.
- [x] Abhängigkeiten in `app/requirements.txt` sind gepinnt.
- [x] `app/prompts/` enthält `einordnen.v1`/`v2` und `assistent.v1`/`v2`/`v3`;
      gemessene Versionen wurden nicht überschrieben.
- [x] `app/angriffe.json` enthält drei eigene Angriffe.
- [ ] README enthält die vollständigen Abgabepunkte aus Teil 5.
- [ ] Falls der Zusatz erforderlich ist: PAIR-Ergebnisse dokumentiert.
- [ ] Moodle-Abgabe enthält Repository-Link und Commit-Hash; Repository ist
      für die Lehrperson lesbar.
