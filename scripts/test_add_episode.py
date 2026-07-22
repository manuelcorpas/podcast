#!/usr/bin/env python3
"""Tests for add_episode.py date resolution."""

from datetime import datetime, timezone
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

import pytest

spec = spec_from_file_location(
    "add_episode", Path(__file__).resolve().parent / "add_episode.py"
)
add_episode = module_from_spec(spec)
spec.loader.exec_module(add_episode)

resolve = add_episode.resolve_pub_datetime

NOW = datetime(2026, 7, 22, 5, 50, 12, tzinfo=timezone.utc)


def test_none_uses_current_time():
    """No --date given: stamp the actual publish moment."""
    assert resolve(None, now=NOW) == NOW


def test_today_uses_current_time_not_noon():
    """--date today: use the real time, never a future noon."""
    assert resolve("2026-07-22", now=NOW) == NOW


def test_past_date_uses_noon():
    """Backfilling an older episode keeps the stable noon convention."""
    assert resolve("2026-07-14", now=NOW) == datetime(
        2026, 7, 14, 12, tzinfo=timezone.utc
    )


def test_future_date_uses_noon():
    """A deliberately scheduled future episode keeps noon."""
    assert resolve("2026-08-01", now=NOW) == datetime(
        2026, 8, 1, 12, tzinfo=timezone.utc
    )


def test_resolved_time_is_never_in_the_future_for_today():
    """The bug we are fixing: today's episode must not be post-dated."""
    assert resolve("2026-07-22", now=NOW) <= NOW


def test_invalid_date_raises():
    with pytest.raises(ValueError):
        resolve("22-07-2026", now=NOW)


ITEM_KWARGS = dict(
    link="https://example.com/post",
    pub_date="Wed, 22 Jul 2026 05:36:58 +0000",
    guid="https://example.com/a.mp3",
    audio_url="https://example.com/a.mp3",
    file_size=123,
    mime_type="audio/mpeg",
    duration=60,
    categories=["AI"],
    image_url="https://example.com/art.jpg",
)


def parse_item(xml: str):
    """A generated item must be parseable on its own, with namespaces bound."""
    import xml.etree.ElementTree as ET

    decls = " ".join(f'xmlns:{p}="{u}"' for p, u in add_episode.NAMESPACES.items())
    return ET.fromstring(f"<rss {decls}>{xml}</rss>")


def test_ampersand_in_description_keeps_feed_well_formed():
    """A bare & in itunes:summary used to break the whole feed."""
    xml = add_episode.make_item_xml(
        title="Ep", description="Cellular & Molecular Pathology", **ITEM_KWARGS
    )
    parse_item(xml)


def test_ampersand_in_title_keeps_feed_well_formed():
    xml = add_episode.make_item_xml(
        title="Genomics, AI & Bioinformatics", description="d", **ITEM_KWARGS
    )
    root = parse_item(xml)
    assert root.find(".//title").text == "Genomics, AI & Bioinformatics"


def test_angle_brackets_are_escaped():
    xml = add_episode.make_item_xml(
        title="Ep", description="a <b> c", **ITEM_KWARGS
    )
    root = parse_item(xml)
    itunes = add_episode.NAMESPACES["itunes"]
    assert root.find(f".//{{{itunes}}}summary").text == "a <b> c"


def test_cdata_description_survives_round_trip():
    """CDATA fields must carry the raw text through unescaped."""
    xml = add_episode.make_item_xml(
        title="Ep", description="Genomics, AI & Bioinformatics", **ITEM_KWARGS
    )
    root = parse_item(xml)
    assert root.find(".//description").text == "Genomics, AI & Bioinformatics"


def test_defaults_to_real_now_when_now_omitted():
    before = datetime.now(timezone.utc)
    resolved = resolve(None)
    after = datetime.now(timezone.utc)
    assert before <= resolved <= after
    assert resolved.tzinfo is not None
