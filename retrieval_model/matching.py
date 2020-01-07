import gensim
import csv
from fse.inputs import IndexedList
from fse.models import SIF
import math
import numpy as np
from sklearn.preprocessing import normalize,scale,MinMaxScaler
from sklearn.neighbors import KDTree
import logging
import pandas as pd


class MatchingModel():

    def __init__(self, file_path, model_path,rewrite=True):
        self.corpus = []
        self.concepts = []
        self.sens = []
        self.w2v_model = None
        self.se = None
        self.file_path = file_path
        self.model_path = model_path
        self.rewrite_mode = rewrite

        self._read()
        self._train()

    def _read(self):
        print('loading model...')
        self.w2v_model = gensim.models.KeyedVectors.load_word2vec_format(self.model_path, binary=True)
        print('loading data...')
        with open(self.file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                self.corpus.append(row[0].split())
                self.concepts.append(row[1])
        self.concepts = [c.split() for c in list(set(self.concepts))]
        if self.rewrite_mode == True:
            # for procedure data set, the following 2 file paths should be replaced
            self.con_dic = dict(pd.read_csv('top50-con-dic.csv'))
            self.dic = dict(pd.read_csv('top50-dic.csv'))
            for key, value in self.con_dic.items():
                self.con_dic[key] = np.array(value)
            for key, value in self.con_dic.items():
                self.dic[key] = np.array(value)
            length = len(self.con_dic)
            X = np.ndarray(shape=(length, 200))
            self.words = []
            for key, i in zip(self.con_dic.keys(), range(length)):
                self.words.append(key)
                X[i] = self.con_dic[key]  # shape --> (length, 200)
            self.tree = KDTree(X)




    def _train(self):
        self.sens = IndexedList(self.concepts)
        print('training SIF...')
        self.se = SIF(self.w2v_model)
        self.se.train(self.sens)

    def query(self, query_sen, topk=25):
        new_sen = query_sen

        if self.rewrite_mode == True:
            new_sen = []
            for w in query_sen:
                if w in self.dic and w not in self.con_dic:
                    q_emb = self.dic[w].reshape(1, 200)
                    dist, ind = self.tree.query(q_emb, k=1)
                    if dist[0][0] < 3.6:
                        # experiments shows that rewriting within a distance of 3.6 performs better than no-rewriting
                        index = ind.tolist()[0]
                        new_sen.append(self.words[index[0]])
                    else:
                        new_sen.append(w)
                else:
                    new_sen.append(w)

        cands = self.se.sv.similar_by_sentence(new_sen, model=self.se, topn=topk, indexable=self.sens.items)
        most_sim = [(x[0], x[2]) for x in cands]
        return most_sim














