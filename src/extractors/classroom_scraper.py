from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from typing import Dict, Generator, Iterable, Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@dataclass
class ClassroomScraper:
    include_comments: bool = False
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

    def _extract_module_payloads(self, html: str) -> Iterable[Dict]:
        soup = BeautifulSoup(html, "lxml")
        # Try Next.js payload first
        next_data = soup.find("script", {"id": "__NEXT_DATA__"})
        if next_data and next_data.string:
            try:
                blob = json.loads(next_data.string)
                page_props = blob.get("props", {}).get("pageProps", {})
                # Heuristic keys
                for key in ["classroom", "modules", "courses", "items", "data"]:
                    val = page_props.get(key)
                    if isinstance(val, list):
                        for it in val:
                            if isinstance(it, dict):
                                yield it
                # If a course object contains modules inside
                course = page_props.get("course") or page_props.get("classroom")
                if isinstance(course, dict):
                    for key in ["modules", "lessons", "items"]:
                        arr = course.get(key)
                        if isinstance(arr, list):
                            for it in arr:
                                if isinstance(it, dict):
                                    yield it
            except json.JSONDecodeError:
                pass

        # Fallback: any LD+JSON with '@type': 'Course' / 'CreativeWork'
        for tag in soup.find_all("script", {"type": "application/ld+json"}):
            if not tag.string:
                continue
            try:
                blob = json.loads(tag.string)
            except json.JSONDecodeError:
                continue
            if isinstance(blob, dict):
                if blob.get("@type") in {"Course", "CreativeWork", "LearningResource"}:
                    yield blob
            elif isinstance(blob, list):
                for b in blob:
                    if isinstance(b, dict) and b.get("@type") in {
                        "Course",
                        "CreativeWork",
                        "LearningResource",
                    }:
                        yield b

    def iter_modules(self, url: str) -> Generator[Dict, None, None]:
        html = self._get(url)
        if not html:
            logger.error("Failed to fetch %s", url)
            return
        seen = 0
        for payload in self._extract_module_payloads(html):
            yield payload
            seen += 1
            if self.max_items and seen >= self.max_items:
                return