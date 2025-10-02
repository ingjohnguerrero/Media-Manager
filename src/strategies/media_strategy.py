from typing import Callable, Dict, Protocol
from dataclasses import dataclass

# A small strategy interface for processing media objects
class MediaProcessor(Protocol):
    def process(self, media) -> None:
        """Process the media object (side effects allowed)."""
        ...

# simple registry to map media_type -> processor
_registry: Dict[str, MediaProcessor] = {}

def register(media_type: str, processor: MediaProcessor) -> None:
    _registry[media_type] = processor

def get_processor(media_type: str) -> MediaProcessor:
    return _registry.get(media_type)

# Example concrete processors
@dataclass
class ImageProcessor:
    def process(self, media) -> None:
        # placeholder: in a real app this might generate thumbnails, validate dimensions, etc.
        # keep it side-effect free for tests (no writes)
        media._processed_by = "image_processor"

@dataclass
class VideoProcessor:
    def process(self, media) -> None:
        # placeholder: in a real app this might extract metadata, generate previews, etc.
        media._processed_by = "video_processor"

# Register default processors
register("image", ImageProcessor())
register("video", VideoProcessor())
register("media", ImageProcessor())

