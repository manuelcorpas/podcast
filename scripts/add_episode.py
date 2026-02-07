#!/usr/bin/env python3
"""Add a new episode to the Personal Genomics Zone podcast feed.

Usage:
    python3 scripts/add_episode.py \
        --title "Episode Title" \
        --file audio/2026-02-04-episode.mp3 \
        --description "Episode description..." \
        --categories "AI,Technology,Podcast" \
        --link "https://manuelcorpas.com/2026/02/04/post-slug/" \
        --date "2026-02-04" \
        [--guid "http://manuelcorpas.com/?p=NNNN"] \
        [--image "https://...image-url..."]
"""

import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

FEED_PATH = Path(__file__).resolve().parent.parent / "feed.xml"
INDEX_PATH = Path(__file__).resolve().parent.parent / "index.html"
BASE_URL = "https://manuelcorpas.github.io/podcast"
DEFAULT_IMAGE = "https://corpasfoo.files.wordpress.com/2017/06/podcast.jpg?fit=3000%2C3000"

# Register all namespaces so they're preserved on write
NAMESPACES = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wfw": "http://wellformedweb.org/CommentAPI/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "atom": "http://www.w3.org/2005/Atom",
    "sy": "http://purl.org/rss/1.0/modules/syndication/",
    "slash": "http://purl.org/rss/1.0/modules/slash/",
    "georss": "http://www.georss.org/georss",
    "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "googleplay": "http://www.google.com/schemas/play-podcasts/1.0",
    "media": "http://search.yahoo.com/mrss/",
}

for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)


def get_duration_seconds(filepath: str) -> int:
    """Get audio duration in seconds using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                filepath,
            ],
            capture_output=True, text=True, check=True,
        )
        return int(float(result.stdout.strip()))
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        print("Warning: ffprobe failed. Enter duration manually (seconds):", file=sys.stderr)
        return int(input("Duration in seconds: "))


def get_mime_type(filepath: str) -> str:
    """Determine MIME type from file extension."""
    ext = Path(filepath).suffix.lower()
    return {
        ".mp3": "audio/mpeg",
        ".m4a": "audio/mp4",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
    }.get(ext, "audio/mpeg")


def make_item_xml(
    title: str,
    link: str,
    pub_date: str,
    guid: str,
    description: str,
    audio_url: str,
    file_size: int,
    mime_type: str,
    duration: int,
    categories: list[str],
    image_url: str,
) -> str:
    """Generate XML string for a new <item>."""
    cats = "\n    ".join(f"<category><![CDATA[{c.strip()}]]></category>" for c in categories)
    return f"""
  <item>
    <title>{title}</title>
    <link>{link}</link>
    <pubDate>{pub_date}</pubDate>
    <guid isPermaLink="false">{guid}</guid>
    <dc:creator><![CDATA[Manuel Corpas]]></dc:creator>
    {cats}
    <description><![CDATA[{description}]]></description>
    <content:encoded><![CDATA[<p>{description}</p>]]></content:encoded>
    <enclosure url="{audio_url}" length="{file_size}" type="{mime_type}"/>
    <itunes:duration>{duration}</itunes:duration>
    <itunes:author>Manuel Corpas</itunes:author>
    <itunes:explicit>false</itunes:explicit>
    <itunes:summary>{description}</itunes:summary>
    <itunes:image href="{image_url}"/>
    <googleplay:author>Manuel Corpas</googleplay:author>
    <googleplay:explicit>false</googleplay:explicit>
    <googleplay:description>{description}</googleplay:description>
    <googleplay:image href="{image_url}"/>
  </item>"""


MONTHS = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def make_index_html_block(
    title: str,
    link: str,
    date: str,
    duration: int,
    description: str,
    audio_file: str,
    mime_type: str,
) -> str:
    """Generate HTML block for index.html."""
    dt = datetime.strptime(date, "%Y-%m-%d")
    date_str = f"{dt.day} {MONTHS[dt.month]} {dt.year}"
    minutes = duration // 60
    return f"""    <div class="episode">
      <h2><a href="{link}">{title}</a></h2>
      <div class="meta">{date_str} &middot; {minutes} min</div>
      <div class="desc">{description}</div>
      <audio controls preload="none">
        <source src="{audio_file}" type="{mime_type}">
      </audio>
    </div>"""


def main():
    parser = argparse.ArgumentParser(description="Add episode to podcast feed")
    parser.add_argument("--title", required=True, help="Episode title")
    parser.add_argument("--file", required=True, help="Path to audio file (relative to repo root)")
    parser.add_argument("--description", required=True, help="Episode description")
    parser.add_argument("--categories", required=True, help="Comma-separated categories")
    parser.add_argument("--link", required=True, help="Blog post URL")
    parser.add_argument("--date", required=True, help="Publication date (YYYY-MM-DD)")
    parser.add_argument("--guid", default=None, help="GUID (defaults to audio URL)")
    parser.add_argument("--image", default=DEFAULT_IMAGE, help="Episode artwork URL")
    args = parser.parse_args()

    repo_root = FEED_PATH.parent
    audio_path = repo_root / args.file

    if not audio_path.exists():
        print(f"Error: audio file not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    if not FEED_PATH.exists():
        print(f"Error: feed.xml not found: {FEED_PATH}", file=sys.stderr)
        sys.exit(1)

    # Compute metadata
    file_size = os.path.getsize(audio_path)
    duration = get_duration_seconds(str(audio_path))
    mime_type = get_mime_type(str(audio_path))
    audio_url = f"{BASE_URL}/{args.file}"
    guid = args.guid or audio_url

    # Parse date
    dt = datetime.strptime(args.date, "%Y-%m-%d").replace(
        hour=12, tzinfo=timezone.utc
    )
    pub_date = format_datetime(dt)

    categories = [c.strip() for c in args.categories.split(",")]
    if "Podcast" not in categories:
        categories.insert(1, "Podcast")

    # Generate new item XML
    item_xml = make_item_xml(
        title=args.title,
        link=args.link,
        pub_date=pub_date,
        guid=guid,
        description=args.description,
        audio_url=audio_url,
        file_size=file_size,
        mime_type=mime_type,
        duration=duration,
        categories=categories,
        image_url=args.image,
    )

    # Read feed, insert item after opening <channel> metadata (before first <item>)
    feed_text = FEED_PATH.read_text(encoding="utf-8")

    # Update lastBuildDate
    new_build_date = format_datetime(datetime.now(timezone.utc))
    import re
    feed_text = re.sub(
        r"<lastBuildDate>.*?</lastBuildDate>",
        f"<lastBuildDate>{new_build_date}</lastBuildDate>",
        feed_text,
    )

    # Insert before the first <item>
    first_item_pos = feed_text.find("<item>")
    if first_item_pos == -1:
        # No items yet — insert before </channel>
        first_item_pos = feed_text.find("</channel>")

    # Add comment
    # Sanitise title for XML comment (double hyphens are illegal in XML comments)
    safe_title = args.title.replace("--", "-")
    comment = f"\n  <!-- Episode: {safe_title} -->"
    feed_text = feed_text[:first_item_pos] + comment + item_xml + "\n\n  " + feed_text[first_item_pos:]

    FEED_PATH.write_text(feed_text, encoding="utf-8")

    # Update index.html
    index_text = INDEX_PATH.read_text(encoding="utf-8")
    episode_html = make_index_html_block(
        title=args.title,
        link=args.link,
        date=args.date,
        duration=duration,
        description=args.description,
        audio_file=args.file,
        mime_type=mime_type,
    )
    # Insert after <main> tag, before the first episode
    main_tag_pos = index_text.find("<main>")
    if main_tag_pos != -1:
        insert_pos = index_text.find("\n", main_tag_pos) + 1
        index_text = index_text[:insert_pos] + "\n" + episode_html + "\n" + index_text[insert_pos:]
    INDEX_PATH.write_text(index_text, encoding="utf-8")

    print(f"Added: {args.title}")
    print(f"  Audio: {audio_url}")
    print(f"  Size:  {file_size:,} bytes")
    print(f"  Duration: {duration}s ({duration // 60}m {duration % 60}s)")
    print(f"  Date:  {pub_date}")
    print(f"Feed updated: {FEED_PATH}")
    print(f"Index updated: {INDEX_PATH}")


if __name__ == "__main__":
    main()
