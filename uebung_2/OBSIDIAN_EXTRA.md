# Obsidian-Extra: Erkenntnisse aus dem Vergleich

Stand: 02.11.2026 · gleicher Laptop · Obsidian 1.13.7 · Ollama `llama3.2:3b`.

## Ziel und Vermutungen

- Ziel: unsere 21 Markdown-Dateien mit Obsidian, Textsuche und RAG vergleichen.
- Vermutungen: Metadaten verbessern Treffer, Links erschließen Zusammenhänge, vorgehaltene Daten sparen Suchzeit.

## Obsidian und die getesteten Erweiterungen

- **Obsidian:** Anwendung zum Bearbeiten und Durchsuchen lokaler Markdown-Notizen, mit Links und Rückverweisen. Im Test kein KI-Plugin; unser Vergleichsskript gibt die gefundenen Texte an dasselbe Ollama-Modell weiter.
- **Grundversion:** normale Textsuche in unveränderten Dateien, ohne ergänzte Eigenschaften oder Verknüpfungen. Für den Vergleich dieselbe Rangfolge wie bei File-based.
- **Metadaten:** zusätzlich hinterlegte Angaben über eine Notiz, etwa Thema, Tags und alternative Namen (Aliasse). Beispiel: Eine Prüfungsnotiz bekommt den Alias „Klausur“. Dadurch kann sie auch unter diesem Begriff gefunden werden.
- **Kennungsfilter:** unser Skript erkennt genaue Kennungen wie `F-201` oder `PA-12` und priorisiert Notizen mit diesem Eintrag in der Eigenschaft `kennungen`. Kein automatisches Bedeutungsverständnis; die Kennungen wurden vorher hinterlegt.
- **Links/Backlinks:** Links verweisen auf andere Notizen; Backlinks zeigen die Notizen, die hierher verweisen. Die letzte Obsidian-Variante nimmt zusätzlich bis zu zwei verknüpfte Nachbarn als Modellkontext auf: ein Schritt, höchstens drei Dateien insgesamt. Exakte Kennungstreffer bleiben erhalten.

## Was gehört zur ursprünglichen Aufgabe?

- **Originalcode:** je Frage `suche()` → `dokumente()` → alle Dateien mit `read_text()` erneut einlesen. Kein eigener Textcache oder Linkindex; Betriebssystem-Caching bleibt möglich.
- **Historischer Originalwert:** Die [Aufgaben-README](README.md) dokumentiert für `datei` **22,1 s Ø insgesamt** (Suche + Modellantwort). Frühere Messreihe, nicht direkt mit den neuen Zeiten vergleichbar.
- **File-based-Zeile unten:** ursprünglicher Suchalgorithmus auf vorgeladenen Texten, keine vollständige Originalausführung. **3,69 s** = Suchbegriff-Erzeugung + Textsuche ohne erneutes Laden; **10,89 s** = Modellantwort. Zusammen **rund 14,6 s**, aus dem kontrollierten FAQ-Zusatztest.
- **Querverweistest:** neue Aufgabe ohne Sprachmodell. „Neu einlesen“ übernimmt das ursprüngliche Ladeprinzip; seine Millisekunden sind keine ursprünglichen FAQ-Zeiten.
- **Neue Kontrollen:** Texte im Speicher und Rückverweisindex. Letzterer speichert vorab Zuordnungen wie `campuskarte.md → [bibliothek.md, drucken.md, …]`, statt sie je Abfrage neu zu suchen.

## FAQ-Vergleich: Qualität und Zeit

- 14 Fragen, gleicher Prompt, Temperatur 0; 98 Antworten. Gleiche v1-Suchbegriffe/Rangfolge für Textsuchen; Ergänzungen nur in Kopien.

| Variante | Richtige Quelle | Antworttreffer | Suche Ø | Modellantwort Ø |
|---|---:|---:|---:|---:|
| File-based: ursprüngliche Suche, Texte vorgeladen | 9/13 | 11/14 | 3,69 s | 10,89 s |
| Obsidian: Grundversion ohne Ergänzungen | 9/13 | 11/14 | 3,78 s | 3,66 s |
| Obsidian: Metadaten + Kennungsfilter | 12/13 | **13/14** | 3,89 s | 4,26 s |
| Obsidian: vorige Variante + Links/Backlinks | 12/13 | 13/14 | 4,17 s | 7,74 s |
| RAG | 12/13 | 13/14 | 0,09 s | 11,13 s |

- Kontrollläufe: File-based + Metadaten **12/14**, RAG + Metadaten **13/14** Antworttreffer.
- Quelle = Dateiname, Antworttreffer = Stichwort; keine vollständige Inhaltsprüfung. Ein Lauf, kein Blindtest; Modellzeiten durch Reihenfolge/Cache beeinflusst.
- **Qualität:** Metadaten/Kennungsfilter helfen; ohne Ergänzungen sind alle 14 Kontexte identisch.
- **Links:** Kein weiterer Antworttreffer, aber 854 statt 765 Eingabe-Tokens, rund 12 % mehr.

## Querverweise: Messung ohne Schnittstellenkosten

- Aufgabe: alle eingehenden Verweise je Notiz finden; live im Obsidian-Prozess, ohne CLI-/Übertragungskosten.
- Sieben Runden × 20 Sätze = **2.940 Abfragen je Verfahren**, wechselnde Reihenfolge; Ergebnismengen vorher/nachher vollständig identisch.

| Verfahren | Median für 21 Abfragen | Einordnung |
|---|---:|---|
| Obsidian: native Backlinks | **2,610 ms** | Vorhandene Metadaten auswerten |
| Dateien je Abfrage neu einlesen | 133,660 ms | Ladeprinzip des Originalcodes; neue Rückverweisaufgabe |
| Dateitexte bereits im Speicher | 0,195 ms | Zusätzliche Kontrolle ohne erneutes Dateieinlesen |
| Eigener Rückverweisindex | 0,010 ms | Neue Kontrolle mit vorbereiteten Zuordnungen |

- **51-mal schneller als erneutes Einlesen**, nicht als die ursprüngliche gesamte FAQ-Anwendung. Vorgehaltene Dateitexte/Linkindex sind nochmals schneller.
- Warmer Zustand; Aufbau, Aktualisierung und Bedienzeit ausgeschlossen. Datei-Kontrollen suchen unseren exakten Wikilink-Aufbau; kleine Speicherzeiten sind Größenordnungen.

## Ist es schneller, und lohnt es sich?

- **Grundversion:** keine besseren Treffer und keine schnellere Suche im FAQ-Test. Kürzere Modellzeiten sind wegen Cache/Reihenfolge kein belastbarer Obsidian-Vorteil.
- **Metadaten/Kennungsfilter:** bessere Auswahl (13 statt 11 Antworttreffer), aber keine gemessene Beschleunigung der Suche (3,89 statt 3,78 s).
- **Links/Backlinks:** kein weiterer Antworttreffer, mehr Kontext. In diesem Test keine sinnvolle Geschwindigkeitsoptimierung.
- **Vorgehaltene Daten:** interne Querverweisabfragen sind schneller als wiederholtes Dateieinlesen. Derselbe Ansatz lässt sich auch File-based umsetzen; eine entsprechend vorbereitete Lösung war hier schneller als Obsidian.
- **Lohnt sich:** wenn Notizen laufend bearbeitet und Navigation, Eigenschaften und Rückverweise ohne eigene Werkzeuge gebraucht werden. Für einen reinen FAQ-Bot ist Obsidian keine Voraussetzung und kein belegter allgemeiner Beschleuniger. Eine menschliche Zeitersparnis wurde nicht gemessen.

<details>
<summary>Rohwerte und ergänzende Messdetails</summary>

- Electron 43.3.0 / Node 24.18.1; `performance.now`, gleicher Prozess. 21 Kopien im Vault mit 43 Markdown-Dateien; Hashes geprüft.
- 62 gerichtete Wikilinks, 82 Nachbarschaftseinträge bei Zusammenfassung beider Richtungen.
- Native Methode: `app.metadataCache.getBacklinksForFile(file).data.keys()`. Alle Verfahren liefern sortierte Quelldateilisten; Längen im Messloop konsumiert.
- Rohwerte je Runde: gemessene Gesamtzeit / 20; Einheit ms je 21 Abfragen.

| Runde | Obsidian | Neu einlesen | Texte im Speicher | Dateiindex |
|---|---:|---:|---:|---:|
| 1 | 2,595 | 134,745 | 0,150 | 0,015 |
| 2 | 2,535 | 121,230 | 0,205 | 0,005 |
| 3 | 2,610 | 141,315 | 0,170 | 0,010 |
| 4 | 2,465 | 132,580 | 0,210 | 0,020 |
| 5 | 2,705 | 133,150 | 0,170 | 0,005 |
| 6 | 2,615 | 137,695 | 0,205 | 0,005 |
| 7 | 2,930 | 133,660 | 0,195 | 0,010 |

- Früherer CLI-Test: Median für 21 Abfragen Obsidian **1,929 s**, `rg` **0,613 s**; fünf Runden, alle 105 Ergebnismengen identisch. Enthält Schnittstellenkosten und ist deshalb kein interner Geschwindigkeitsvergleich.
- CLI-Rohwerte in ms: Obsidian `[1964.307, 1895.836, 1941.433, 1924.615, 1928.920]`; `rg` `[618.342, 598.567, 629.140, 606.830, 613.350]`.

</details>

Belege: [FAQ-Messübersicht](obsidian_extra/zusammenfassung.json), [Antworten](obsidian_extra/ergebnisse.json), [native Suche/Graph](obsidian_extra/obsidian_suche.json), [feste Eingaben](obsidian_extra/vorbereitung.json), [Original-Dateisuche](app/datei_suche.py), [ursprünglicher Dateilader](app/wissen.py).

Funktionsdokumentation: [Backlinks](https://help.obsidian.md/Plugins/Backlinks), [Graph](https://help.obsidian.md/Plugins/Graph+view), [CLI/eval](https://obsidian.md/help/cli).

Hinweis: `run.mjs report` und der Aufruf ohne Phase überschreiben diese redaktionelle Übersicht. FAQ-Test erneut ausführen: Phasen `prepare`, `collect`, `evaluate` einzeln aufrufen.
