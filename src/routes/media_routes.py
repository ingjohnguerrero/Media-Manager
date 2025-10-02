from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import Column, String
from typing import Optional, List
from src.database import get_db
from src.strategies.media_strategy import get_processor
from src.dto.media_dto import MediaCreateDTO, ImageCreateDTO, VideoCreateDTO, MediaReadDTO
import os

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

@router.post("/media/", status_code=201, response_model=MediaReadDTO)
def create_media(
    alt_text: str = Form(...),
    extension: str = Form(...),
    media_type: str = Form("media"),
    file: UploadFile = None,
    session: Session = Depends(get_db)
):
    # Save uploaded file if present
    if file:
        os.makedirs("uploads", exist_ok=True)
        file_location = f"uploads/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        url = file_location
    else:
        url = ""
    media = Media(alt_text=alt_text, extension=extension, url=url, media_type=media_type)
    session.add(media)
    session.commit()
    session.refresh(media)
    return MediaReadDTO.from_orm(media)

@router.get("/media/", response_model=List[MediaReadDTO])
def get_media(session: Session = Depends(get_db)):
    medias = session.exec(select(Media)).all()
    return [MediaReadDTO.from_orm(m) for m in medias]

@router.post("/images/", status_code=201, response_model=MediaReadDTO)
def create_image(image_dto: ImageCreateDTO, session: Session = Depends(get_db)):
    m = Media(alt_text=image_dto.alt_text, extension=image_dto.extension, url=image_dto.url, media_type="image")
    processor = get_processor("image")
    if processor:
        processor.process(m)
    session.add(m)
    session.commit()
    session.refresh(m)
    return MediaReadDTO.from_orm(m)

@router.post("/videos/", status_code=201, response_model=MediaReadDTO)
def create_video(video_dto: VideoCreateDTO, session: Session = Depends(get_db)):
    m = Media(alt_text=video_dto.alt_text, extension=video_dto.extension, url=video_dto.url, media_type="video")
    processor = get_processor("video")
    if processor:
        processor.process(m)
    session.add(m)
    session.commit()
    session.refresh(m)
    return MediaReadDTO.from_orm(m)

@router.get("/media/{media_id}", response_model=MediaReadDTO)
def get_media_by_id(media_id: int, session: Session = Depends(get_db)):
    media = session.get(Media, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return MediaReadDTO.from_orm(media)

@router.put("/media/{media_id}", response_model=MediaReadDTO)
def update_media(media_id: int, media_dto: MediaCreateDTO, session: Session = Depends(get_db)):
    media = session.get(Media, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    for key, value in media_dto.model_dump().items():
        setattr(media, key, value)
    session.add(media)
    session.commit()
    session.refresh(media)
    return MediaReadDTO.from_orm(media)

@router.delete("/media/{media_id}", status_code=204)
def delete_media(media_id: int, session: Session = Depends(get_db)):
    media = session.get(Media, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    session.delete(media)
    session.commit()
    return
