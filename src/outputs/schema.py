from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

class ItemType(str, Enum):
    post = "post"
    module = "module"

class User(BaseModel):
    id: str = ""
    name: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    firstName: str = ""
    lastName: str = ""

class Comment(BaseModel):
    id: str
    parentId: str = ""
    rootId: str = ""
    content: str = ""
    upvotes: int = 0
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    attachments: str = ""
    attachmentsData: str = ""
    user: Optional[User] = None
    replies: List["Comment"] = Field(default_factory=list)

Comment.model_rebuild()

class CourseMetaDetails(BaseModel):
    id: str = ""
    name: str = ""
    title: str = ""
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

class SkoolItem(BaseModel):
    type: ItemType
    id: str
    name: str = ""
    title: str = ""
    postTitle: str = ""
    content: str = ""
    url: str = ""
    urlAjax: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    groupId: str = ""
    userId: str = ""
    postType: str = ""
    rootId: str = ""
    parentId: str = ""
    labelId: str = ""
    user: Optional[User] = None
    comments: List[Comment] = Field(default_factory=list)
    media: List[str] = Field(default_factory=list)
    courseMetaDetails: Optional[CourseMetaDetails] = None