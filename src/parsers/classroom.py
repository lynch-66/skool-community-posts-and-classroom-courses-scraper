from __future__ import annotations

from typing import Any, Dict, List, Optional

from outputs.schema import (
    ItemType,
    SkoolItem,
    CourseMetaDetails,
)
from extractors.utils_time import to_iso

def _course_meta(raw: Dict[str, Any]) -> Optional[CourseMetaDetails]:
    if not isinstance(raw, dict):
        return None
    return CourseMetaDetails(
        id=str(raw.get("id") or raw.get("@id") or raw.get("courseId") or ""),
        name=str(raw.get("name") or raw.get("slug") or ""),
        title=str(raw.get("title") or raw.get("headline") or raw.get("name") or ""),
        createdAt=to_iso(raw.get("createdAt") or raw.get("dateCreated")),
        updatedAt=to_iso(raw.get("updatedAt") or raw.get("dateModified")),
    )

def normalize_module(raw: Dict[str, Any]) -> SkoolItem:
    # Accept both Skool-like payloads and schema.org Course/LearningResource
    media = []
    for key in ("media", "video", "videos", "mediaLinks", "mediaLink"):
        val = raw.get(key)
        if isinstance(val, list):
            media.extend([str(v) for v in val])
        elif isinstance(val, str) and val:
            media.append(val)

    course_meta = None
    for key in ("courseMetaDetails", "course", "about", "inCourse"):
        maybe = raw.get(key)
        if isinstance(maybe, dict):
            course_meta = _course_meta(maybe)
            break

    return SkoolItem(
        type=ItemType.module,
        id=str(raw.get("id") or raw.get("@id") or ""),
        name=str(raw.get("name") or ""),
        title=str(raw.get("title") or ""),
        postTitle=str(raw.get("postTitle") or raw.get("title") or ""),
        content=str(raw.get("content") or raw.get("description") or ""),
        url=str(raw.get("url") or ""),
        urlAjax=str(raw.get("urlAjax") or ""),
        metadata={},
        createdAt=to_iso(raw.get("createdAt") or raw.get("dateCreated")),
        updatedAt=to_iso(raw.get("updatedAt") or raw.get("dateModified")),
        groupId=str(raw.get("groupId") or ""),
        userId=str(raw.get("userId") or ""),
        postType=str(raw.get("type") or "module"),
        rootId=str(raw.get("rootId") or ""),
        parentId=str(raw.get("parent_id") or ""),
        labelId=str(raw.get("labelId") or ""),
        user=None,
        comments=[],
        media=media,
        courseMetaDetails=course_meta,
    )