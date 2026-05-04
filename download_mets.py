#!/usr/bin/env python3
"""Download METS XML files listed in a text file.
Call like this:
    python download_manifests.py manifests.txt manifests
"""

from __future__ import annotations

import re
import sys
from hashlib import sha1
from pathlib import Path
from urllib.request import Request, urlopen

ID_RE = re.compile(r".*/([0-9]+)/[^/]*mets[^/]*$", re.IGNORECASE)


def mets_id(url: str) -> str:
    match = ID_RE.match(url)
    if match:
        return match.group(1)
    return sha1(url.encode("utf-8")).hexdigest()[:12]


def iter_urls(list_file: Path):
    for line in list_file.read_text(encoding="utf-8").splitlines():
        url = line.strip()
        if not url or url.startswith("#"):
            continue
        yield url


def looks_like_xml(data: bytes) -> bool:
    # Strip optional UTF-8 BOM and leading whitespace before checking first token.
    stripped = data.lstrip(b"\xef\xbb\xbf\t\n\r ")
    return stripped.startswith(b"<")


def download(url: str, destination: Path) -> None:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=60) as response:
        content = response.read()

    if not looks_like_xml(content):
        raise ValueError(
            f"URL does not return XML/METS: {url}\n"
            "Hint: provide METS XML links in manifests.txt (not IIIF manifest JSON links)."
        )

    destination.write_bytes(content)
    print(f"Saved  {destination.name}")


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python download_manifests.py <mets_list.txt> <output_dir>")
        return 2

    list_file = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])

    if not list_file.exists():
        print(f"Error: list file not found: {list_file}")
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for url in iter_urls(list_file):
        mid = mets_id(url)
        target = out_dir / f"{mid}.xml"
        if target.exists():
            existing = target.read_bytes()
            if looks_like_xml(existing):
                print(f"Skip   {target.name}")
                count += 1
                continue
            print(f"Replace {target.name} (existing file is not XML)")
        print(f"Fetch  {url} -> {target}")
        download(url, target)
        count += 1

    print(f"Done. Processed {count} URL(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    