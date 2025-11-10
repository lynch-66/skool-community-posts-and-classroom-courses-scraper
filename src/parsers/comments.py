from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from outputs.schema import Comment, User
from extractors.utils_time import to_iso

def _user_from_comment(u: Dict[str, Any]) -> Optional[User]:
    if not isinstance(u, dict):
        return None
    meta = u.get("metadata") or {}
    return User(
        id=str(u.get("id") or u.get("userId") or u.get("user_id") or ""),
        name=str(u.get("name") or ""),
        metadata={
            "bio": meta.get("bio") or "",
            "pictureBubble": meta.get("pictureBubble") or meta.get("picture_bubble") or "",
            "pictureProfile": meta.get("pictureProfile") or meta.get("picture_profile") or "",
        },
        createdAt=to_iso(u.get("createdAt") or u.get("created_at")),
        updatedAt=to_iso(u.get("updatedAt") or u.get("updated_at")),
        firstName=str(u.get("firstName") or u.get("first_name") or ""),
        lastName=str(u.get("lastName") or u.get("last_name") or ""),
    )

def _coerce_comment(rec: Dict[str, Any]) -> Optional[Comment]:
    """
    Accept either a raw record with fields at top-level or nested under 'post'.
    """
    node = rec.get("post") if isinstance(rec.get("post"), dict) else rec
    if not isinstance(node, dict):
        return None

    u = node.get("user") or {}
    meta = node.get("metadata") or {}

    return Comment(
        id=str(node.get("id") or node.get("comment_id") or ""),
        parentId=str(node.get("parent_id") or ""),
        rootId=str(node.get("root_id") or node.get("rootId") or ""),
        content=str(meta.get("content") or node.get("content") or ""),
        upvotes=int(meta.get("upvotes") or node.get("upvotes") or 0),
        createdAt=to_iso(node.get("created_at") or node.get("createdAt")),
        updatedAt=to_iso(node.get("updated_at") or node.get("updatedAt")),
        attachments=str(meta.get("attachments") or ""),
        attachmentsData=str(meta.get("attachments_data") or ""),
        user=_user_from_comment(u),
        replies=[],
    )

def _build_tree(flat: List[Comment]) -> List[Comment]:
    by_id = {c.id: c for c in flat if c and c.id}
    roots: List[Comment] = []
    for c in flat:
        if not c:
            continue
        if c.parentId and c.parentId in by_id:
            by_id[c.parentId].replies.append(c)
        else:
            roots.append(c)
    return roots

def normalize_comments(records: Any) -> List[Comment]:
    """
    Normalize comments payload (list or dict) into a nested tree of Comment objects.
    """
    flat: List[Comment] = []
    if isinstance(records, dict) and "items" in records:
        records = records["items"]
    if isinstance(records, list):
        for rec in records:
            c = _coerce_comment(rec)
            if c:
                flat.append(c)
    return _build_tree(flat)