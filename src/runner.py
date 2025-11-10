import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

from tqdm import tqdm

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from extractors.community_scraper import CommunityScraper
from extractors.classroom_scraper import ClassroomScraper
from outputs.exporters import Exporter
from outputs.schema import ItemType, SkoolItem
from parsers.posts import normalize_post
from parsers.classroom import normalize_module

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def run(
    urls: List[str],
    mode: str,
    output_dir: str,
    include_comments: bool,
    offline: bool,
    max_items: Optional[int] = None,
    sample_path: Optional[str] = None,
) -> int:
    ensure_dir(output_dir)
    exporter = Exporter(output_dir)

    if offline:
        # Use sample file (provided) or embedded example
        if sample_path and os.path.exists(sample_path):
            sample = load_json(sample_path)
        else:
            builtin = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "data", "sample_output.json"
            )
            sample = load_json(builtin)

        written = 0
        for raw in tqdm(sample, desc="Writing sample items"):
            if raw.get("type") == "module":
                item = normalize_module(raw)
            else:
                item = normalize_post(raw)
            exporter.write(item)
            written += 1
            if max_items and written >= max_items:
                break

        exporter.finalize()
        print(f"Offline run complete. Wrote {written} items to {output_dir}")
        return 0

    # Online scraping
    items: List[SkoolItem] = []
    if mode == "community":
        scraper = CommunityScraper(include_comments=include_comments, max_items=max_items)
        for url in urls:
            for raw in scraper.iter_items(url):
                items.append(normalize_post(raw))
    elif mode == "classroom":
        scraper = ClassroomScraper(include_comments=include_comments, max_items=max_items)
        for url in urls:
            for raw in scraper.iter_modules(url):
                items.append(normalize_module(raw))
    elif mode == "both":
        comm = CommunityScraper(include_comments=include_comments, max_items=max_items)
        clas = ClassroomScraper(include_comments=include_comments, max_items=max_items)
        for url in urls:
            for raw in comm.iter_items(url):
                items.append(normalize_post(raw))
            for raw in clas.iter_modules(url):
                items.append(normalize_module(raw))
    else:
        raise SystemExit(f"Unknown mode: {mode}")

    for item in tqdm(items, desc="Exporting"):
        exporter.write(item)
    exporter.finalize()
    print(f"Wrote {len(items)} items to {output_dir}")
    return 0

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Skool Community & Classroom Scraper Runner"
    )
    ap.add_argument(
        "--inputs",
        type=str,
        default=os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "inputs.sample.json"
        ),
        help="Path to inputs JSON file (array or object with 'urls').",
    )
    ap.add_argument(
        "--mode",
        choices=["community", "classroom", "both"],
        default="both",
        help="Which surfaces to scrape.",
    )
    ap.add_argument(
        "--output",
        type=str,
        default=os.path.join(os.getcwd(), "out"),
        help="Directory for JSON/CSV outputs.",
    )
    ap.add_argument(
        "--include-comments",
        action="store_true",
        help="Include nested comments where applicable.",
    )
    ap.add_argument(
        "--offline",
        action="store_true",
        help="Run without network: emit bundled sample_output.json.",
    )
    ap.add_argument(
        "--max-items",
        type=int,
        default=None,
        help="Max items to export.",
    )
    ap.add_argument(
        "--sample",
        type=str,
        default=None,
        help="Optional path to a sample JSON to use in --offline mode.",
    )
    return ap.parse_args()

if __name__ == "__main__":
    args = parse_args()
    inputs_raw = load_json(args.inputs)
    if isinstance(inputs_raw, dict) and "urls" in inputs_raw:
        urls = inputs_raw["urls"]
    elif isinstance(inputs_raw, list):
        urls = inputs_raw
    else:
        raise SystemExit("Invalid inputs JSON. Provide list or { 'urls': [...] }.")

    t0 = time.time()
    code = run(
        urls=urls,
        mode=args.mode,
        output_dir=args.output,
        include_comments=args.include_comments,
        offline=args.offline,
        max_items=args.max_items,
        sample_path=args.sample,
    )
    dt = time.time() - t0
    print(f"Done in {dt:.2f}s")
    raise SystemExit(code)