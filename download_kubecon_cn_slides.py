#!/usr/bin/env python3

# Download slides for KubeCon + CloudNativeCon + OpenInfra Summit + PyTorch Conference China
# from the lfopensource.cn schedule page (sessions with uploaded slides).

import html
import re
import time
import urllib.request
from pathlib import Path

SCHEDULE_URL = (
    "https://www.lfopensource.cn/kubecon-cloudnativecon-openinfra-summit-pytorch-conference-china"
    "/program/schedule/?slides=uploaded"
)
EVENT = "kubecon-cloudnativecon-openinfra-summit-pytorch-conference-china"
BASE_DIR = Path(__file__).resolve().parent / EVENT
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


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
        urls = [
            u for u in re.findall(r'href="(https://sessionize\.com/download/[^"]+)"', part)
            if u not in seen
        ]
        seen.update(urls)
        if urls:
            sessions.append((date_match.group(1), title_match.group(1).strip(), urls))
    return sessions


def main():
    print(f"Fetching schedule: {SCHEDULE_URL}")
    page = fetch(SCHEDULE_URL).decode("utf-8", errors="replace")
    sessions = parse_sessions(page)
    print(f"Found {len(sessions)} sessions with slides")

    downloaded = failed = 0
    for date, title, urls in sessions:
        print(f"\n[{date}] {html.unescape(title)}")
        out_dir = BASE_DIR / date
        out_dir.mkdir(parents=True, exist_ok=True)
        name = sanitize(title)
        for index, url in enumerate(urls):
            filename = url.rsplit("~", 1)[-1]
            ext = filename.rsplit(".", 1)[-1] if "." in filename else "pdf"
            suffix = "" if index == 0 else f"-{index + 1}"
            dest = out_dir / f"{name}{suffix}.{ext}"
            if dest.exists() and dest.stat().st_size > 0:
                print(f"  Skip (exists): {dest.relative_to(BASE_DIR)}")
                continue
            print(f"  Downloading: {dest.relative_to(BASE_DIR)}")
            try:
                dest.write_bytes(fetch(url))
                downloaded += 1
            except Exception as exc:
                failed += 1
                dest.unlink(missing_ok=True)
                print(f"  FAILED: {exc}")
    print(f"Done. {downloaded} downloaded, {failed} failed.")


if __name__ == "__main__":
    main()
