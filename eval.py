"""Evaluate learned word representation on word similarity task"""
import sys
import os
import logging
import argparse
import numpy as np
from fasttext import load_model
from scipy.stats import spearmanr
from tqdm import tqdm

from convert_subchar import convert_radical as radical
from convert_subchar import convert_wubi as wubi

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    parser = argparse.ArgumentParser(description='Evaluate word representations')
    parser.add_argument('--input', type=str, default='wordsim-296.txt', help='Evaluation data path')
    parser.add_argument('--model_path', type=str, default='model.bin', help='Trained model path')
    parser.add_argument('--subchar_type', type=str, default='character', help='character/wubi/radical')
    args = parser.parse_args()

    logging.info('Start evaluation for {} data..'.format(args.subchar_type))
    model = load_model(args.model_path)
    eval_data = open(args.input, 'r')
    pred_score = []
    human_score = []
    for line in tqdm(eval_data):
        w1, w2, human = line.split()
        if args.subchar_type == 'wubi':
            w1, w2 = wubi(w1), wubi(w2)
        if args.subchar_type == 'radical':
            w1, w2 = radical(w1), radical(w2)
        
        emb1, emb2 = model[w1], model[w2]
        pred = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        human_score.append(human)
        pred_score.append(pred)
    corr = spearmanr(human_score, pred_score)
    logging.info('Finish evaluation. Score = {}'.format(corr))
    eval_data.close()
    logging.info('Done')

if __name__ == '__main__':
    main()
