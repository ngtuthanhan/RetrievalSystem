import pandas as pd 
import numpy as np 
import os
from os import listdir
from os.path import isfile,join
import json
import glob
import scann
import torch
from transformers import CLIPModel, CLIPProcessor
from tqdm import tqdm
from PIL import Image
class Searcher:
    def __init__(self, index, features, num_neighbors = 50, distance_measure = 'dot_product'):
        self.index = index
        self.searcher = scann.scann_ops_pybind.builder(
                                features,
                                num_neighbors,
                                distance_measure).score_brute_force(1).build()
        
    def __call__(self,text_embedding):
        neighbors, distances = self.searcher.search(text_embedding, final_num_neighbors = 50)
        # print(self.index[neighbors])
        return self.index[neighbors]

        
class CLIPFeatureExtractor:
    def __init__(self):
        model_name = "openai/clip-vit-base-patch16"
        self.model = CLIPModel.from_pretrained(model_name)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)

    def __call__(self, text):
        inputs = self.processor(text=text, return_tensors="pt")
        inputs = inputs.to(self.device)
        text_features = self.model.get_text_features(**inputs)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        text_features = text_features.tolist()
        return text_features

class Indexing:
    def __init__(self,root_data):
        self.root_data = root_data
        self.all_data = glob.glob(root_data + '*')

    @property
    def get_all_features(self):
        features = np.empty([0,512],dtype = float)
        index = []
        for image in tqdm(self.all_data):
            video, frame = image.split('_')[-2].split('/')[-1], image.split('_')[-1]
            model_name = "openai/clip-vit-base-patch16"
            model = CLIPModel.from_pretrained(model_name)
            processor = CLIPProcessor.from_pretrained(model_name)
            image = Image.open(image)
            inputs = processor(images=image, return_tensors="pt")
            image_features = model.get_image_features(**inputs)
            features = np.concatenate((features,image_features.detach().numpy()),axis = 0)
            index.append(list((video,frame)))
            with open('./retriever/feature.npy','wb') as f:
                np.save(f, features)
            with open('./retriever/index.npy','wb') as f:
                np.save(f,index)
        return features, np.array(index)
    
        