from pydantic import BaseModel
from typing import Optional

class MediaCreateDTO(BaseModel):
    alt_text: str
    extension: str
    url: str
    media_type: Optional[str] = "media"

class ImageCreateDTO(BaseModel):
    alt_text: str
    extension: str
    url: str

class VideoCreateDTO(BaseModel):
    alt_text: str
    extension: str
    url: str

class MediaReadDTO(BaseModel):
    id: int
    alt_text: str
    extension: str
    url: str
    media_type: str
    model_config = {"from_attributes": True}
