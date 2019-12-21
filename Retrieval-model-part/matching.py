import gensim
import csv
from fse.inputs import IndexedList
from fse.models import SIF
import math
import numpy as np
from sklearn.preprocessing import normalize,scale,MinMaxScaler
import logging

class MatchingModel():
    def __init__(self,file_path,model_path):
        self.corpus = []
        self.concepts = []
        self.sens = []
        self.w2v_model = None
        self.se = None
        self.file_path = file_path
        self.model_path = model_path

        self._read()
        self._train()

    def _read(self):
        print('loading model...')
        self.w2v_model = gensim.models.KeyedVectors.load_word2vec_format(self.model_path,binary=True)
        print('loading data...')
        with open(self.file_path,'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                self.corpus.append(row[0].split())
                self.concepts.append(row[1])
        self.concepts =[c.split() for c in list(set(self.concepts))]


    def _train(self):
        self.sens = IndexedList(self.concepts)
        print('training SIF...')
        self.se = SIF(self.w2v_model)
        self.se.train(self.sens)

    def query(self,query_sen,topk=25):
        cands = self.se.sv.similar_by_sentence(query_sen,model=self.se,topn=topk,indexable=self.sens.items)
        most_sim = [(x[0],x[2]) for x in cands]
        return most_sim














