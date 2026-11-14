"""Buchungswerkzeug und Bestätigung prüfen: python pruefen_teil2.py."""

import io
import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import httpx

from agent import fragen, werkzeug_ausfuehren
from mcp_werkzeuge import mcp_werkzeuge
from werkzeuge import Werkzeug


class BestaetigungTest(unittest.TestCase):
    def setUp(self):
        self.funktion = Mock(return_value="Gebucht")
        self.werkzeug = Werkzeug("raum_buchen", "Test", {}, self.funktion, schreibend=True)
        self.aufruf = SimpleNamespace(function=SimpleNamespace(
            name="raum_buchen", arguments=json.dumps({"name": "Kim"})))

    def test_ablehnung_fuehrt_nichts_aus(self):
        schritt = werkzeug_ausfuehren(self.aufruf, {"raum_buchen": self.werkzeug}, lambda *_: False)
        self.assertEqual(schritt.fehler, "abgelehnt")
        self.funktion.assert_not_called()

    def test_zustimmung_fuehrt_einmal_aus(self):
        schritt = werkzeug_ausfuehren(self.aufruf, {"raum_buchen": self.werkzeug}, lambda *_: True)
        self.assertIsNone(schritt.fehler)
        self.funktion.assert_called_once_with(name="Kim")

    def test_lesendes_werkzeug_fragt_nicht(self):
        self.werkzeug.schreibend = False
        bestaetigen = Mock()
        werkzeug_ausfuehren(self.aufruf, {"raum_buchen": self.werkzeug}, bestaetigen)
        bestaetigen.assert_not_called()
        self.funktion.assert_called_once()

    def test_ohne_terminal_keine_zustimmung(self):
        with patch("sys.stdin", io.StringIO("j\n")):
            self.assertFalse(fragen(self.werkzeug, {"name": "Kim"}))


class BuchungMCPTest(unittest.TestCase):
    def setUp(self):
        self.url = os.environ["MCP_URL"].removesuffix("/mcp") + "/zuruecksetzen"
        httpx.post(self.url).raise_for_status()
        self.werkzeuge = {w.name: w for w in mcp_werkzeuge()}
        self.buchen = self.werkzeuge["raum_buchen"].funktion

    def tearDown(self):
        httpx.post(self.url).raise_for_status()

    def test_buchung_sichtbar_und_nicht_ueberschreibbar(self):
        self.assertTrue(self.werkzeuge["raum_buchen"].schreibend)
        self.assertIn("Gebucht:", self.buchen(raum="O-108", datum="2026-11-06", uhrzeit="09:45", name="Kim"))
        self.assertIn("gebucht von Kim", self.werkzeuge["raum_frei"].funktion(raum="O-108", datum="2026-11-06"))
        erneut = self.buchen(raum="O-108", datum="2026-11-06", uhrzeit="09:45", name="Alex")
        self.assertTrue(erneut.startswith("Fehler:"))
        self.assertIn("Freie Zeitfenster:", erneut)
        self.assertIn("gebucht von Kim", erneut)

    def test_belegter_slot_und_ungueltige_eingaben(self):
        basis = dict(raum="O-108", datum="2026-11-06", uhrzeit="09:45", name="Kim")
        for aenderung in [
            {"raum": "X-999"}, {"datum": "heute"}, {"datum": "2026-02-30"},
            {"datum": "2026-11-07"}, {"uhrzeit": "10:00"}, {"name": " "},
            {"datum": "2026-11-05", "uhrzeit": "14:00"},
        ]:
            with self.subTest(eingabe=aenderung):
                self.assertTrue(self.buchen(**(basis | aenderung)).startswith("Fehler:"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
