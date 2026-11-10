#!/usr/bin/env python3

# Download slides from a Linux Foundation event schedule page that lists
# sessions with uploaded slides (sessionize download links).
#
# Layout: <event>/<YYYY-MM-DD>/<sanitized-title>.<ext>

import argparse
import html
import re
import time
import urllib.request
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
SESSIONIZE_LINK = re.compile(r'href="(https://sessionize\.com/download/[^"]+)"')


def normalize_schedule_url(url):
    """Accept an event root or a schedule page, preserving other filters."""
    parts = urlsplit(url)
    path = parts.path.rstrip("/")
    slug = path.rsplit("/", 1)[-1].lower()
    # LF uses both /program/schedule/ and named co-located *-schedule/ pages.
    if slug != "schedule" and not slug.endswith("-schedule"):
        path += "/program/schedule"
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if key != "slides"]
    query.append(("slides", "uploaded"))
    return urlunsplit((parts.scheme, parts.netloc, path + "/", urlencode(query), ""))


def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.read()
        except Exception as exc:
            if attempt == retries - 1:
                raise
            print(f"  retrying after error: {exc}")
            time.sleep(3)


def sanitize(title):
    title = html.unescape(re.sub(r"<[^>]+>", "", title))
    title = re.sub(r"[^\w\s-]", "", title, flags=re.UNICODE)
    title = re.sub(r"\s+", "-", title.strip())
    return title[:100].strip("-")


def parse_sessions(page):
    # The page embeds a JSON blob after the session blocks that repeats every
    # slide URL, so only match links inside href attributes.
    sessions = []
    seen = set()
    for part in page.split("sess-wrap")[1:]:
        title_match = re.search(r'sess__title">(.*?)</div>', part, re.S)
        date_match = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})T', part)
        if not title_match or not date_match:
            continue
        urls = [u for u in SESSIONIZE_LINK.findall(part) if u not in seen]
        seen.update(urls)
        if urls:
            sessions.append((date_match.group(1), title_match.group(1).strip(), urls))
    return sessions


def download_event(event, schedule_url, base_dir=None):
    base_dir = Path(event) if not base_dir else Path(base_dir)
    print(f"Fetching schedule: {schedule_url}")
    sessions = parse_sessions(fetch(schedule_url).decode("utf-8", errors="replace"))
    print(f"Found {len(sessions)} sessions with slides")

    downloaded = skipped = failed = 0
    for date, title, urls in sessions:
        print(f"\n[{date}] {html.unescape(title)}")
        out_dir = base_dir / date
        out_dir.mkdir(parents=True, exist_ok=True)
        name = sanitize(title)
        for index, url in enumerate(urls):
            filename = url.rsplit("~", 1)[-1]
            ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "pdf"
            if not ext.isalnum():
                ext = "pdf"
            suffix = "" if index == 0 else f"-{index + 1}"
            dest = out_dir / f"{name}{suffix}.{ext}"
            shown = dest.relative_to(Path.cwd()) if dest.is_relative_to(Path.cwd()) else dest
            if dest.exists() and dest.stat().st_size > 0:
                print(f"  Skip (exists): {shown}")
                skipped += 1
                continue
            print(f"  Downloading: {shown}")
            try:
                dest.write_bytes(fetch(url))
                downloaded += 1
            except Exception as exc:
                failed += 1
                dest.unlink(missing_ok=True)
                print(f"  FAILED: {exc}")
    print(f"\nDone. {downloaded} downloaded, {skipped} skipped, {failed} failed.")
    return 1 if failed else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="event home page or full schedule URL, e.g. https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/")
    parser.add_argument("--output-dir", help="output directory (default: last path segment of the URL)")
    args = parser.parse_args()
    schedule_url = normalize_schedule_url(args.url)
    event = args.output_dir or urlsplit(args.url).path.rstrip("/").rsplit("/", 1)[-1]
    raise SystemExit(download_event(event, schedule_url, args.output_dir))


if __name__ == "__main__":
    main()
