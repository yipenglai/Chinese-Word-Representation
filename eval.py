"""Evaluate learned word representation on word similarity task"""
import sys
import os
import logging
import argparse
import numpy as np
from fasttext import load_model
from scipy.stats import spearmanr
from tqdm import tqdm
import pandas as pd

from convert_subchar import convert_radical as radical
from convert_subchar import convert_wubi as wubi

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    parser = argparse.ArgumentParser(description='Evaluate word representations')
    parser.add_argument('--input', type=str, default='wordsim-296.txt', help='Evaluation data path')
    parser.add_argument('--model_path', type=str, default='model.bin', help='Trained model path')
    parser.add_argument('--subchar_type', type=str, default='character', help='character/wubi/radical')
    parser.add_argument('--output', type=str, default='result.txt',help='Path to save the words pairs and their similarities')
    args = parser.parse_args()

    logging.info('Start evaluation for {} data..'.format(args.subchar_type))
    model = load_model(args.model_path)
    eval_data = open(args.input, 'r')
    human_score = []
    result_list = [] # store (w1, w2, similarity) for error analysis

    for line in tqdm(eval_data):
        word1, word2, human = line.split()
        if args.subchar_type == 'wubi':
            w1, w2 = wubi(word1), wubi(word2)
        elif args.subchar_type == 'radical':
            w1, w2 = radical(word1), radical(word2)
        else:
            w1, w2 = word1, word2
        
        emb1, emb2 = model[w1], model[w2]
        pred = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        human_score.append(human)
        result_list.append((word1, word2, pred))

    result = pd.DataFrame(result_list, columns =['Word_1', 'Word_2', 'Pred_Score']) 
    result.to_csv(args.output, sep='\t')
    pred_score = [i[-1] for i in result_list]
    corr = spearmanr(human_score, pred_score)
    logging.info('Finish evaluation on dataset {}. Score = {}'.format(args.input,corr))
    eval_data.close()
    logging.info('Done')

if __name__ == '__main__':
    main()
