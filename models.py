"""
Pydantic modelleri — API'nin request/response şemaları.
"""
from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    """Yeni kullanıcı oluştururken gönderilecek veri."""
    name: str
    interest: str


class FeedbackRequest(BaseModel):
    """Kullanıcı bir öneriye 👍/👎 verdiğinde gönderilecek veri."""
    user_name: str
    item_title: str
    feedback: str  # "like" veya "dislike"


class RecommendRequest(BaseModel):
    """Öneri isteyecek kullanıcının bilgisi."""
    interest: str
    history: Optional[list[str]] = []


class ItemDetailRequest(BaseModel):
    """Bir öğe için 3 modelin detaylı yorumunu isterken gönderilecek veri."""
    item_title: str
    interest: Optional[str] = ""
