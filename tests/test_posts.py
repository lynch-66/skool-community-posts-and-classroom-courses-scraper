import json
from pathlib import Path

from src.parsers.posts import normalize_post
from src.outputs.schema import SkoolItem, ItemType

def test_normalize_post_sample():
    sample_path = Path(__file__).resolve().parents[1] / "data" / "sample_output.json"
    data = json.loads(sample_path.read_text(encoding="utf-8"))
    post_raw = data[0]
    item = normalize_post(post_raw)
    assert isinstance(item, SkoolItem)
    assert item.type == ItemType.post
    assert item.id == "aab147fa0ea4420d83e8d3a9214f5203"
    assert item.metadata["comments"] == 2
    # Nested comments must be linked
    assert len(item.comments) == 1
    assert item.comments[0].id == "c1"
    assert len(item.comments[0].replies) == 1
    assert item.comments[0].replies[0].parentId == "c1"