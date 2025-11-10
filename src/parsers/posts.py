from __future__ import annotations

from typing import Any, Dict, List, Optional

from outputs.schema import (
    Comment,
    ItemType,
    SkoolItem,
    User,
)
from parsers.comments import normalize_comments
from extractors.utils_time import to_iso

def _coerce_user(u: Dict[str, Any]) -> User:
    # Accept multiple casing styles (snake/camel)
    meta = u.get("metadata") or {}
    return User(
        id=str(u.get("id") or u.get("userId") or u.get("user_id") or ""),
        name=str(u.get("name") or u.get("username") or ""),
        metadata={
            "bio": meta.get("bio") or meta.get("Bio") or "",
            "pictureBubble": meta.get("pictureBubble") or meta.get("picture_bubble") or "",
            "pictureProfile": meta.get("pictureProfile") or meta.get("picture_profile") or "",
            "location": meta.get("location") or "",
            "linkWebsite": meta.get("linkWebsite") or meta.get("website") or "",
            "linkYoutube": meta.get("linkYoutube") or meta.get("youtube") or "",
            "actStatus": meta.get("actStatus") or meta.get("status") or "",
        },
        createdAt=to_iso(u.get("createdAt") or u.get("created_at")),
        updatedAt=to_iso(u.get("updatedAt") or u.get("updated_at")),
        firstName=str(u.get("firstName") or u.get("first_name") or ""),
        lastName=str(u.get("lastName") or u.get("last_name") or ""),
    )

def normalize_post(raw: Dict[str, Any]) -> SkoolItem:
    meta = raw.get("metadata") or raw.get("meta") or {}
    # Some Skool payloads nest post under 'post'
    core = raw.get("post") if isinstance(raw.get("post"), dict) else raw
    user_raw = core.get("user") or {}
    comments_raw = core.get("comments") or raw.get("comments") or []

    item = SkoolItem(
        type=ItemType.post,
        id=str(core.get("id") or core.get("post_id") or core.get("uuid") or ""),
        name=str(core.get("name") or core.get("slug") or ""),
        title=str(core.get("title") or meta.get("title") or ""),
        postTitle=str(core.get("postTitle") or core.get("title") or ""),
        content=str(core.get("content") or meta.get("content") or ""),
        url=str(core.get("url") or raw.get("url") or ""),
        urlAjax=str(core.get("urlAjax") or raw.get("urlAjax") or ""),
        metadata={
            "action": meta.get("action", 0),
            "comments": meta.get("comments") or core.get("commentsCount") or 0,
            "upvotes": meta.get("upvotes") or core.get("upvotes") or 0,
            "pinned": meta.get("pinned") or core.get("pinned") or 0,
            "imagePreview": meta.get("imagePreview") or "",
            "imagePreviewSmall": meta.get("imagePreviewSmall") or "",
            "videoLinksData": meta.get("videoLinksData") or "[]",
            "contributors": meta.get("contributors") or "[]",
            "labels": meta.get("labels") or core.get("labelId") or "",
            "hasNewComments": meta.get("hasNewComments") or 0,
            "lastComment": meta.get("lastComment") or 0,
        },
        createdAt=to_iso(core.get("createdAt") or core.get("created_at")),
        updatedAt=to_iso(core.get("updatedAt") or core.get("updated_at")),
        groupId=str(core.get("groupId") or raw.get("groupId") or ""),
        userId=str(core.get("userId") or raw.get("userId") or ""),
        postType=str(core.get("postType") or core.get("type") or "generic"),
        rootId=str(core.get("rootId") or raw.get("rootId") or core.get("id") or ""),
        parentId=str(core.get("parent_id") or ""),
        labelId=str(core.get("labelId") or meta.get("labels") or ""),
        user=_coerce_user(user_raw) if user_raw else None,
        comments=normalize_comments(comments_raw),
        media=[],
        courseMetaDetails=None,
    )
    return item