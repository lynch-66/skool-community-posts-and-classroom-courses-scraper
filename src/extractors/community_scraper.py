from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass
from typing import Dict, Generator, Iterable, Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SCRIPT_JSON_SELECTORS = [
    # Common Next.js payload container
    {"name": "__NEXT_DATA__"},
    # Fallback generic LD+JSON
    {"type": "application/ld+json"},
]

@dataclass
class CommunityScraper:
    include_comments: bool = True
    max_items: Optional[int] = None
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
    retries: int = 3
    timeout: int = 20

    def _get(self, url: str) -> Optional[str]:
        for attempt in range(1, self.retries + 1):
            try:
                resp = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=self.timeout)
                if resp.status_code == 200:
                    return resp.text
                logger.warning("GET %s -> %s", url, resp.status_code)
            except requests.RequestException as exc:
                logger.warning("GET error (%s/%s): %s", attempt, self.retries, exc)
                time.sleep(1.5 * attempt)
        return None

    def _extract_json_blobs(self, html: str) -> Iterable[Dict]:
        soup = BeautifulSoup(html, "lxml")
        # Try named script first
        for sel in SCRIPT_JSON_SELECTORS:
            if "name" in sel:
                tag = soup.find("script", {"id": sel["name"]})
                if tag and tag.string:
                    try:
                        yield json.loads(tag.string)
                    except json.JSONDecodeError:
                        pass
            elif "type" in sel:
                for tag in soup.find_all("script", {"type": sel["type"]}):
                    if not tag.string:
                        continue
                    try:
                        yield json.loads(tag.string)
                    except json.JSONDecodeError:
                        continue

        # Generic inline JSON candidates
        for tag in soup.find_all("script"):
            content = tag.string or ""
            if "{" in content and "}" in content:
                # Heuristic: try to find large JSON blocks
                m = re.search(r"(\{.*\})", content, flags=re.DOTALL)
                if m:
                    block = m.group(1)
                    try:
                        yield json.loads(block)
                    except Exception:
                        continue

    def _coerce_post_records(self, blob: Dict) -> Iterable[Dict]:
        """
        Attempts to find post-like records inside the blob.
        Returns dictionaries that parsers.posts.normalize_post can handle.
        """
        # Strategy 1: Next data with pageProps
        page_props = (
            blob.get("props", {})
            .get("pageProps", {})
        )
        if isinstance(page_props, dict):
            # Heuristic containers
            candidates = []
            for key in ["posts", "items", "feed", "data"]:
                val = page_props.get(key)
                if isinstance(val, list):
                    candidates.extend(val)
                elif isinstance(val, dict) and "items" in val and isinstance(val["items"], list):
                    candidates.extend(val["items"])
            for rec in candidates:
                if isinstance(rec, dict):
                    yield rec

        # Strategy 2: top-level list
        if isinstance(blob, list):
            for rec in blob:
                if isinstance(rec, dict):
                    yield rec

        # Strategy 3: nested data keys
        for key in ["data", "payload", "result", "collection"]:
            val = blob.get(key)
            if isinstance(val, list):
                for rec in val:
                    if isinstance(rec, dict):
                        yield rec

    def iter_items(self, url: str) -> Generator[Dict, None, None]:
        """
        Yields raw post dicts discovered on the page. Comment inclusion depends on downstream parser/normalizer.
        """
        html = self._get(url)
        if not html:
            logger.error("Failed to fetch %s", url)
            return

        seen = 0
        for blob in self._extract_json_blobs(html):
            for rec in self._coerce_post_records(blob):
                yield rec
                seen += 1
                if self.max_items and seen >= self.max_items:
                    return