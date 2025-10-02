from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import Column, String
from typing import Optional, List
from src.database import get_db
from src.strategies.media_strategy import get_processor

router = APIRouter()

class Media(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    alt_text: str
    extension: str
    url: str
    media_type: str = Field(default="media", sa_column=Column(String, nullable=False))

# Non-table models used for request validation (strategy/input)
class Image(SQLModel):
    alt_text: str
    extension: str
    url: str

class Video(SQLModel):
    alt_text: str
    extension: str
    url: str

@router.post("/media/", status_code=201)
def create_media(media: Media, session: Session = Depends(get_db)):
    session.add(media)
    session.commit()
    session.refresh(media)
    return media

@router.get("/media/", response_model=List[Media])
def get_media(session: Session = Depends(get_db)):
    medias = session.exec(select(Media)).all()
    return medias

@router.post("/images/", status_code=201)
def create_image(image: Image, session: Session = Depends(get_db)):
    m = Media(alt_text=image.alt_text, extension=image.extension, url=image.url, media_type="image")
    processor = get_processor("image")
    if processor:
        processor.process(m)
    session.add(m)
    session.commit()
    session.refresh(m)
    return m

@router.post("/videos/", status_code=201)
def create_video(video: Video, session: Session = Depends(get_db)):
    m = Media(alt_text=video.alt_text, extension=video.extension, url=video.url, media_type="video")
    processor = get_processor("video")
    if processor:
        processor.process(m)
    session.add(m)
    session.commit()
    session.refresh(m)
    return m
