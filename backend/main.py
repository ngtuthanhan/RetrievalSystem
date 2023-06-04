from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware as CORSMiddleware
import json
from fastapi.staticfiles import StaticFiles
from retriever import extractor, load_model, handle_query, find_nearest
import os 
import numpy as np
import pandas as pd
from googletrans import Translator

# App object
app = FastAPI()

app.mount("/data", StaticFiles(directory="data"))
origins = ["http://localhost:4000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

translator = Translator()

with open('./data/keyframe.json') as file:
    video_list = json.load(file)

if os.path.exists("./retriever/feature.npy"):
    feature = np.load("./retriever/feature.npy")
    index = np.load("./retriever/index.npy")
else:
    feature, index = extractor()
   

MODELS = load_model(feature, index)

def find_dicts_with_keyframe(data_list, keyframes):
    matching_dicts = []
    for keyframe in keyframes:
        for data_dict in data_list:
            if keyframe == data_dict['keyframe']:
                matching_dicts.append(data_dict)
                continue
    return matching_dicts

def find_detail(data_list, keyframe):
    video = keyframe.split('_')[0] + '.gif'
    matching_dicts = []
    for data_dict in data_list:
        if video == data_dict['video']:
            matching_dicts.append(data_dict)
    matching_dicts.sort(key=lambda x: x['frame_position'])
    return matching_dicts


@app.get("/api/video")
async def get_video():
    response = video_list
    return response

@app.post("/api/video/")
async def post_todo(Vietnamese = '', English = ''):
    if Vietnamese != '': 
        English = translator.translate(Vietnamese , src='vi', dest='en').text
    results = handle_query(English, MODELS)
    results = pd.DataFrame(results)
    results_frame = [results[0][i] +"_" + results[1][i] for i in range(len(results))]
    video_ans = find_dicts_with_keyframe(video_list, results_frame)
    return video_ans

@app.get("/api/video/detail/{keyframe}")
async def search_video_by_keyframe(keyframe):
    response = find_detail(video_list, keyframe)
    return response

@app.get("/api/video/knn/{keyframe}")
async def find_nearest_video_by_keyframe(keyframe):
    image = f"./data/keyframe/{keyframe}"
    results = find_nearest(image, MODELS)
    results = pd.DataFrame(results)
    results_frame = [results[0][i] +"_" + results[1][i] for i in range(len(results))]
    video_ans = find_dicts_with_keyframe(video_list, results_frame)
    return video_ans
