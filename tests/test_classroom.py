import json
from pathlib import Path

from src.parsers.classroom import normalize_module
from src.outputs.schema import SkoolItem, ItemType, CourseMetaDetails

def test_normalize_module_sample():
    sample_path = Path(__file__).resolve().parents[1] / "data" / "sample_output.json"
    data = json.loads(sample_path.read_text(encoding="utf-8"))
    mod_raw = data[1]
    item = normalize_module(mod_raw)
    assert isinstance(item, SkoolItem)
    assert item.type == ItemType.module
    assert item.id == "unique-module-id"
    assert item.courseMetaDetails is not None
    assert isinstance(item.courseMetaDetails, CourseMetaDetails)
    assert item.media and item.media[0].startswith("https://")

skool-community-posts-and-classroom-courses-scraper/.keep
textPlaceholder to ensure repository root is preserved when exporting selected files.