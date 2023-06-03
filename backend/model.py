from pydantic import BaseModel

class Video(BaseModel):
    video: str
    keyframe: str
    url: str
    frame_id: str
    frame_position: int
