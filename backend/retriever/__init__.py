import numpy as np
from .utils.TIUday import Searcher, CLIPTextExtractor, CLIPImageExtractor, Indexing


def extractor():
    extractor = Indexing("./data/keyframe/")
    feature, index = extractor.get_all_features
    with open('./retriever/feature.npy','wb') as f:
        np.save(f,feature)
    with open('./retriever/index.npy','wb') as f:
        np.save(f,index)
    return feature, index

def load_model(features, index):
    SEARCHER = Searcher(index=index, features=features)
    CLIPTEXT = CLIPTextExtractor()
    CLIPIMAGE = CLIPImageExtractor()
    MODELS = {
        "SEACHER": SEARCHER,
        "TEXT": CLIPTEXT,
        "IMAGE": CLIPIMAGE,
    }
    return MODELS

def handle_query(query, MODELS):
    text_embedding = MODELS["TEXT"](query)
    results = MODELS["SEACHER"](text_embedding.reshape(-1))
    return results

def find_nearest(image, MODELS):
    image_embedding = MODELS["IMAGE"](image)
    results = MODELS["SEACHER"](image_embedding.reshape(-1))
    return results
