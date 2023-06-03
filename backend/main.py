from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware as CORSMiddleware
from database import *
import json
from fastapi.staticfiles import StaticFiles
from retriever import extractor, load_model, handle_query
import os 
import numpy as np
# App object
app = FastAPI()

app.mount("/data", StaticFiles(directory="data"))
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('./data/keyframe.json') as file:
    video_list = json.load(file)

import_database(video_list)

if os.path.exists("./retriever/extract.py"):
    feature = np.load("features.npy")
    index = np.load("index.npy")
else:
    feature, index = extractor()

MODELS = load_model(feature, index)


@app.get("/api/video")
async def get_video():
    response = await fetch_all_video()
    return response

@app.get("/api/video/{keyframe}", response_model = Video)
async def get_video_by_keyframe(keyframe):
    response = await fetch_one_video(keyframe)
    if response:
        return response
    raise HTTPException(404, f"There is no Video item with this id {keyframe}")

@app.post("/api/video/", response_model = Video)
async def post_todo(video: Video):
    response = await create_video(video.dict())
    if response:
        return response
    raise HTTPException(400, f"Bad request")

@app.put("/api/video/{keyframe}", response_model = Video)
async def put_todo(keyframe: str, video: dict):
    response = await update_video(keyframe, video)
    if response:
        return response
    raise HTTPException(404, f"There is no Video item with this id {keyframe}")

@app.delete("/api/video/{keyframe}", response_model = Video)
async def delete_video(keyframe):
    response = await remove_video(keyframe)
    if response:
        return "Sucessfully deleted Video item"
    raise HTTPException(404, f"There is no Video item with this id  {keyframe}")