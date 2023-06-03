import numpy as np
from .utils.TIUday import Searcher, CLIPFeatureExtractor, Indexing


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
    CLIP = CLIPFeatureExtractor()
    MODELS = {
        "SEACHER": SEARCHER,
        "EXTRACTOR": CLIP
    }
    return MODELS


def handle_query(query, MODELS):
    text_embedding = MODELS["EXTRACTOR"](query)
    results = MODELS["SEACHER"](np.array(text_embedding).reshape(-1))
    return results
