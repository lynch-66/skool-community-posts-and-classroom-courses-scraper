from src.parsers.comments import normalize_comments
from src.outputs.schema import Comment

def test_comment_tree_building():
    records = [
        {"post": {"id": "r1", "metadata": {"content": "root"}}},
        {"post": {"id": "r2", "metadata": {"content": "root 2"}}},
        {"post": {"id": "c1", "parent_id": "r1", "metadata": {"content": "child"}}},
        {"post": {"id": "c2", "parent_id": "c1", "metadata": {"content": "grandchild"}}},
    ]
    tree = normalize_comments(records)
    assert len(tree) == 2
    r1 = next(x for x in tree if x.id == "r1")
    assert len(r1.replies) == 1
    assert r1.replies[0].id == "c1"
    assert r1.replies[0].replies[0].id == "c2"