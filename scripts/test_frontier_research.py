#!/usr/bin/env python3
"""Regression tests for Frontier Agents fail-closed research gate."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("research_checker",HERE/"scripts/check_frontier_research.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
source=HERE/"episodes/2026-10-12-frontier-agents-01"

class ResearchGateTests(unittest.TestCase):
    def test_current_episode_passes(self):
        self.assertEqual(mod.validate(source),[])
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.folder=Path(self.temp.name)
        for name in ("transcript.txt","show-notes.md","evidence-ledger.json","research-review.md"):
            (self.folder/name).write_bytes((source/name).read_bytes())
    def tearDown(self):
        self.temp.cleanup()
    def test_missing_post_february_benchmark_correction_fails(self):
        t=self.folder/"transcript.txt"
        t.write_text(t.read_text().replace("July twenty twenty-six","July last year"))
        failures=mod.validate(self.folder)
        self.assertTrue(any("July 2026 correction" in f for f in failures),failures)
    def test_broken_claim_citation_fails(self):
        p=self.folder/"evidence-ledger.json"
        payload=json.loads(p.read_text())
        payload["claims"][0]["sources"]=["NONEXISTENT_SOURCE"]
        p.write_text(json.dumps(payload))
        failures=mod.validate(self.folder)
        self.assertTrue(any("unknown source" in f for f in failures),failures)
    def test_release_readiness_cannot_be_unapproved(self):
        p=self.folder/"evidence-ledger.json"
        payload=json.loads(p.read_text());payload["release_readiness"]="fail"
        p.write_text(json.dumps(payload))
        failures=mod.validate(self.folder)
        self.assertTrue(any("not pass" in f for f in failures),failures)
if __name__=="__main__":unittest.main()
