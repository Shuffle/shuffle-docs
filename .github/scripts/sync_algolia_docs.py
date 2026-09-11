#!/usr/bin/env python3
"""
Sync Markdown documentation to Algolia.
Parses docs/, articles/, and legal/ folders with code-fence awareness,
HTML comment stripping, and anchor slug generation.

Priorities:
  docs (base 1000) > articles (base 500) > legal (base 100)
  + Heading level boost: H1 (+30), H2 (+20), H3 (+10)

Supports atomic index replacement (zero downtime, zero stale records).
"""

import os
import re
import sys
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from algoliasearch.search_client import SearchClient
    from algoliasearch.exceptions import RequestException
except ImportError:
    SearchClient = None
    RequestException = Exception

# Base priority tiers (docs > articles > legal)
FOLDER_PRIORITY = {
    "docs": 1000,
    "articles": 500,
    "legal": 100,
}

HEADING_BOOST = {
    1: 30,
    2: 20,
    3: 10,
    4: 0,
    5: 0,
    6: 0,
}

MAX_RECORD_DATA_BYTES = 7500  # Safe limit well under Algolia's 10KB threshold


def slugify(text: str) -> str:
    """Generate clean kebab-case anchor matching frontend markdown renderers."""
    # Remove HTML tags if present
    cleaned = re.sub(r"<[^>]+>", "", text)
    # Replace symbols with empty string, keep alphanumeric, spaces, and hyphens
    cleaned = re.sub(r"[^\w\s-]", "", cleaned)
    # Collapse whitespace and convert to hyphens
    cleaned = re.sub(r"[\s_]+", "-", cleaned).strip("-").lower()
    return cleaned or "section"


def clean_markdown_text(text: str) -> str:
    """Clean markdown formatting for full-text search indexing."""
    # Remove HTML comments (e.g. <!-- component:... --> or <!-- TODO: ... -->)
    cleaned = re.sub(r"<!--[\s\S]*?-->", " ", text)
    # Remove markdown image tags: ![alt](url)
    cleaned = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", cleaned)
    # Convert markdown links [text](url) to text
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cleaned)
    # Strip inline code formatting backticks
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    # Strip markdown bold/italic
    cleaned = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", cleaned)
    # Strip blockquote markers
    cleaned = re.sub(r"^>\s*", "", cleaned, flags=re.MULTILINE)
    # Normalize excessive whitespace
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{2,}", "\n", cleaned)
    return cleaned.strip()


def parse_markdown_file(file_path: Path, repo_root: Path) -> List[Dict[str, Any]]:
    """
    Parse a single markdown file into section records.
    Aware of fenced code blocks (``` or ~~~) to prevent false headings.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return []

    folder = file_path.parent.name
    filename = file_path.stem
    doc_slug = filename.replace("_", "-").lower()
    base_priority = FOLDER_PRIORITY.get(folder, 100)

    # Determine document title from first H1 or filename
    doc_title = filename.replace("_", " ").title()
    for line in content.splitlines():
        trimmed = line.strip()
        if trimmed.startswith("# ") and not trimmed.startswith("## "):
            doc_title = trimmed[2:].strip()
            break

    lines = content.splitlines()
    records: List[Dict[str, Any]] = []

    in_code_block = False
    current_h2 = ""
    current_h3 = ""

    current_title = doc_title
    current_level = 1
    current_lines: List[str] = []

    def flush_section():
        nonlocal current_lines, current_title, current_level, current_h2, current_h3
        raw_text = "\n".join(current_lines)
        clean_text = clean_markdown_text(raw_text)

        # Skip completely empty sections unless it's the document intro
        if not clean_text and current_level > 1:
            current_lines = []
            return

        anchor = slugify(current_title)
        priority = base_priority + HEADING_BOOST.get(current_level, 0)

        # Unique deterministic objectID
        object_id = f"{folder}_{filename}_{anchor}"

        record_urlpath = f"/{folder}/{filename}#{anchor}" if anchor else f"/{folder}/{filename}"
        record_url = f"https://shuffler.io{record_urlpath}"
        ref_url = f"https://github.com/shuffle/shuffle-docs/blob/master/{folder}/{file_path.name}"

        # If section is very long, chunk it into parts under 7.5KB
        encoded_data = clean_text.encode("utf-8")
        if len(encoded_data) > MAX_RECORD_DATA_BYTES:
            chunks = []
            words = clean_text.split(" ")
            curr_chunk: List[str] = []
            curr_size = 0
            for w in words:
                w_size = len(w.encode("utf-8")) + 1
                if curr_size + w_size > MAX_RECORD_DATA_BYTES:
                    chunks.append(" ".join(curr_chunk))
                    curr_chunk = [w]
                    curr_size = w_size
                else:
                    curr_chunk.append(w)
                    curr_size += w_size
            if curr_chunk:
                chunks.append(" ".join(curr_chunk))

            for idx, chunk in enumerate(chunks):
                sub_id = f"{object_id}-part{idx+1}" if idx > 0 else object_id
                records.append({
                    "objectID": sub_id,
                    "folder": folder,
                    "filename": filename,
                    "doc_slug": doc_slug,
                    "title": current_title if idx == 0 else f"{current_title} (Part {idx+1})",
                    "doc_title": doc_title,
                    "section_h2": current_h2,
                    "section_h3": current_h3,
                    "heading_level": current_level,
                    "data": chunk,
                    "url": record_url,
                    "urlpath": record_urlpath,
                    "ref_url": ref_url,
                    "priority": priority,
                })
        else:
            records.append({
                "objectID": object_id,
                "folder": folder,
                "filename": filename,
                "doc_slug": doc_slug,
                "title": current_title,
                "doc_title": doc_title,
                "section_h2": current_h2,
                "section_h3": current_h3,
                "heading_level": current_level,
                "data": clean_text,
                "url": record_url,
                "urlpath": record_urlpath,
                "ref_url": ref_url,
                "priority": priority,
            })

        current_lines = []

    for line in lines:
        trimmed = line.strip()

        # Check for code fence toggles
        if trimmed.startswith("```") or trimmed.startswith("~~~"):
            in_code_block = not in_code_block
            current_lines.append(line)
            continue

        if not in_code_block and trimmed.startswith("#"):
            match = re.match(r"^(#{1,6})\s+(.*)$", trimmed)
            if match:
                # Flush previous section before starting new one
                flush_section()

                hashes, heading_text = match.groups()
                level = len(hashes)
                clean_heading = heading_text.strip()

                current_title = clean_heading
                current_level = level

                if level == 2:
                    current_h2 = clean_heading
                    current_h3 = ""
                elif level == 3:
                    current_h3 = clean_heading

                continue

        current_lines.append(line)

    # Flush final section on EOF (fixes bug where last section was dropped)
    flush_section()

    return records


def collect_all_records(repo_root: Path) -> List[Dict[str, Any]]:
    """Scan docs, articles, and legal folders and generate all records."""
    all_records: List[Dict[str, Any]] = []
    folders = ["docs", "articles", "legal"]

    for folder_name in folders:
        folder_path = repo_root / folder_name
        if not folder_path.is_dir():
            print(f"Warning: {folder_path} is not a directory, skipping", file=sys.stderr)
            continue

        md_files = sorted(folder_path.glob("*.md"))
        for md_file in md_files:
            # Skip editor temp files or swap files
            if md_file.name.startswith(".") or ".swp" in md_file.name or ".swo" in md_file.name:
                continue
            records = parse_markdown_file(md_file, repo_root)
            all_records.extend(records)

    return all_records


def setup_index_settings(index):
    """Configure search ranking, distinct attributes, and highlights."""
    settings = {
        "searchableAttributes": [
            "unordered(title)",
            "unordered(section_h2)",
            "unordered(section_h3)",
            "unordered(doc_title)",
            "data",
            "filename",
        ],
        "attributesToRetrieve": [
            "title",
            "doc_title",
            "filename",
            "doc_slug",
            "folder",
            "data",
            "urlpath",
            "url",
            "ref_url",
            "priority",
        ],
        "attributesToHighlight": [
            "data",
            "title",
        ],
        "attributesToSnippet": [
            "data:40",
        ],
        "attributeForDistinct": "doc_slug",
        "distinct": 1,
        "customRanking": [
            "desc(priority)",
            "asc(heading_level)",
        ],
    }
    index.set_settings(settings)
    print("Configured Algolia index settings successfully.")


def main():
    parser = argparse.ArgumentParser(description="Sync Shuffle documentation to Algolia")
    parser.add_argument("--dry-run", action="store_true", help="Parse files and validate records without uploading")
    parser.add_argument("--index", default="documentation", help="Algolia index name (default: documentation)")
    parser.add_argument("--verbose", action="store_true", help="Print details of parsed records")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    print(f"Scanning markdown files from: {repo_root}")

    records = collect_all_records(repo_root)
    print(f"Total records generated: {len(records)}")

    # Summary by folder
    counts: Dict[str, int] = {}
    for r in records:
        f = r["folder"]
        counts[f] = counts.get(f, 0) + 1

    for f, count in counts.items():
        print(f"  {f}: {count} records (priority tier: {FOLDER_PRIORITY.get(f, 0)})")

    # Validate record sizes
    oversized = [r for r in records if len(r["data"].encode("utf-8")) > 10000]
    if oversized:
        print(f"ERROR: {len(oversized)} records exceed 10KB!", file=sys.stderr)
        for r in oversized:
            print(f"  {r['objectID']}: {len(r['data'].encode('utf-8'))} bytes", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        for r in records[:5]:
            print(f"[{r['folder']}] {r['objectID']} (P:{r['priority']}) -> {r['urlpath']}")
            print(f"  Title: {r['title']}")
            print(f"  Data snippet: {r['data'][:100]}...\n")

    if args.dry_run:
        print("Dry run completed successfully. Zero network requests made.")
        return

    # Check credentials
    app_id = os.environ.get("ALGOLIA_APP_ID") or os.environ.get("ALGOLIA_CLIENT")
    api_key = os.environ.get("ALGOLIA_API_KEY") or os.environ.get("ALGOLIA_SECRET")

    if not app_id or not api_key:
        print("ERROR: Missing ALGOLIA_APP_ID (or ALGOLIA_CLIENT) and ALGOLIA_API_KEY (or ALGOLIA_SECRET)", file=sys.stderr)
        sys.exit(1)

    if SearchClient is None:
        print("ERROR: algoliasearch package not installed. Run 'pip install algoliasearch'", file=sys.stderr)
        sys.exit(1)

    print(f"Connecting to Algolia (App ID: {app_id}, Index: {args.index})...")
    client = SearchClient.create(app_id, api_key)
    index = client.init_index(args.index)

    # Configure index settings
    try:
        setup_index_settings(index)
    except Exception as e:
        print(f"Warning: Failed to update index settings: {e}", file=sys.stderr)

    # Atomic full index replacement
    print(f"Performing atomic index replacement for {len(records)} records...")
    try:
        # replace_all_objects stages into a temp index and moves atomically
        res = index.replace_all_objects(records, {
            "safe": True,
            "autoGenerateObjectIDIfNotExist": False,
        })
        print(f"Success! Replaced all objects in '{args.index}'.")
    except RequestException as e:
        print(f"ERROR: Algolia request failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected failure during index upload: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
